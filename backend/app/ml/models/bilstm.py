"""
Model B: Bidirectional Long Short-Term Memory (BiLSTM) for Isolated ISL Recognition.
Captures forward and backward temporal dynamics across the 30-frame landmark sequence.
"""

from typing import Dict, Optional, Tuple
import torch
import torch.nn as nn
import torch.nn.functional as F


class BiLSTMClassifier(nn.Module):
    """Bidirectional LSTM with temporal pooling for sequence gesture classification."""

    def __init__(
        self,
        in_features: int = 282,
        hidden_size: int = 128,
        num_layers: int = 2,
        num_classes: int = 67,
        dropout: float = 0.3,
    ) -> None:
        super().__init__()
        self.in_features = in_features
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_classes = num_classes

        # Linear projection to smooth spatial dimensions before recurrence
        self.proj = nn.Sequential(
            nn.Linear(in_features, hidden_size),
            nn.LayerNorm(hidden_size),
            nn.ReLU(),
            nn.Dropout(dropout * 0.5),
        )

        # Bidirectional LSTM layers
        self.lstm = nn.LSTM(
            input_size=hidden_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )

        # Classifier head operating on concatenated mean and max pooled temporal tokens
        pooled_dim = hidden_size * 2 * 2  # bidirectional (2) * [mean, max] (2) = 512
        self.classifier = nn.Sequential(
            nn.Linear(pooled_dim, 128),
            nn.LayerNorm(128),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(128, num_classes),
        )

    def forward(
        self, x: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Forward pass.
        
        Args:
            x: Tensor of shape (batch, seq_len, in_features)
        Returns:
            logits: (batch, num_classes)
            probs: (batch, num_classes)
        """
        projected = self.proj(x)  # (batch, seq_len, hidden_size)
        lstm_out, _ = self.lstm(projected)  # (batch, seq_len, hidden_size * 2)

        # Concat temporal mean and temporal max pooling for richer gesture representation
        mean_pooled = torch.mean(lstm_out, dim=1)
        max_pooled, _ = torch.max(lstm_out, dim=1)
        pooled = torch.cat([mean_pooled, max_pooled], dim=-1)  # (batch, 512)

        logits = self.classifier(pooled)
        probs = F.softmax(logits, dim=-1)

        return logits, probs
