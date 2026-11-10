"""
Model A: Temporal 1D Convolutional Neural Network for Isolated ISL Recognition.
Processes temporal landmark sequences (batch, 30, 282) using dilated/multiscale 1D convolutions.
"""

from typing import Dict, Optional, Tuple
import torch
import torch.nn as nn
import torch.nn.functional as F


class TemporalCNNClassifier(nn.Module):
    """Temporal CNN for sequence-based gesture classification."""

    def __init__(
        self,
        in_features: int = 282,
        num_classes: int = 67,
        dropout: float = 0.3,
    ) -> None:
        super().__init__()
        self.in_features = in_features
        self.num_classes = num_classes

        # Temporal 1D Conv Blocks over (batch, channels, time)
        self.conv1 = nn.Sequential(
            nn.Conv1d(in_features, 128, kernel_size=5, padding=2),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(dropout * 0.5),
        )

        self.conv2 = nn.Sequential(
            nn.Conv1d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2),  # 30 -> 15
        )

        self.conv3 = nn.Sequential(
            nn.Conv1d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(dropout * 0.5),
        )

        self.conv4 = nn.Sequential(
            nn.Conv1d(256, 256, kernel_size=3, padding=1),
            nn.BatchNorm1d(256),
            nn.ReLU(),
        )

        self.global_pool = nn.AdaptiveAvgPool1d(1)

        # Classification Head
        self.classifier = nn.Sequential(
            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
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
        # Transpose (batch, time, channels) -> (batch, channels, time)
        x_conv = x.transpose(1, 2)

        feat1 = self.conv1(x_conv)
        feat2 = self.conv2(feat1)
        feat3 = self.conv3(feat2)
        feat4 = self.conv4(feat3)

        pooled = self.global_pool(feat4).squeeze(-1)  # (batch, 256)
        logits = self.classifier(pooled)             # (batch, num_classes)
        probs = F.softmax(logits, dim=-1)

        return logits, probs
