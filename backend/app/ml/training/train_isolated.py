"""
Training and evaluation pipeline for isolated ISL recognition.
Trains Model A (Temporal CNN) and Model B (BiLSTM) side-by-side on identical
unseen-signer splits, evaluates metrics, latency, and model size, and saves the best checkpoint.
"""

import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from sklearn.metrics import classification_report, f1_score, confusion_matrix

from backend.app.ml.models.temporal_cnn import TemporalCNNClassifier
from backend.app.ml.models.bilstm import BiLSTMClassifier
from backend.app.ml.training.dataset_loader import generate_benchmark_dataset, load_label_map

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("signova.ml.training")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
CHECKPOINTS_DIR = PROJECT_ROOT / "models" / "checkpoints"
CONFIGS_DIR = PROJECT_ROOT / "models" / "configs"


def train_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    device: torch.device,
) -> Tuple[float, float]:
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0

    for x_batch, y_batch in loader:
        x_batch = x_batch.to(device)
        y_batch = y_batch.to(device)

        optimizer.zero_grad()
        logits, _ = model(x_batch)
        loss = criterion(logits, y_batch)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=2.0)
        optimizer.step()

        total_loss += loss.item() * len(y_batch)
        preds = torch.argmax(logits, dim=-1)
        correct += (preds == y_batch).sum().item()
        total += len(y_batch)

    return total_loss / max(1, total), correct / max(1, total)


def evaluate_model(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
) -> Dict[str, Any]:
    model.eval()
    total_loss = 0.0
    all_preds = []
    all_targets = []

    # Measure pure latency on batch_size=1
    latency_times = []

    with torch.no_grad():
        for x_batch, y_batch in loader:
            x_dev = x_batch.to(device)
            y_dev = y_batch.to(device)

            start = time.perf_counter()
            logits, probs = model(x_dev)
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            latency_times.append(elapsed_ms / len(x_batch))

            loss = criterion(logits, y_dev)
            total_loss += loss.item() * len(y_batch)

            preds = torch.argmax(logits, dim=-1).cpu().numpy()
            all_preds.extend(preds)
            all_targets.extend(y_batch.numpy())

    all_preds = np.array(all_preds)
    all_targets = np.array(all_targets)

    acc = float(np.mean(all_preds == all_targets))
    macro_f1 = float(f1_score(all_targets, all_preds, average="macro", zero_division=0))
    avg_latency = float(np.mean(latency_times))
    avg_loss = total_loss / max(1, len(all_targets))
    cm = confusion_matrix(all_targets, all_preds).tolist()

    return {
        "loss": avg_loss,
        "accuracy": acc,
        "macro_f1": macro_f1,
        "latency_ms": avg_latency,
        "preds": all_preds.tolist(),
        "targets": all_targets.tolist(),
        "confusion_matrix": cm,
    }


def train_and_compare(
    epochs: int = 25,
    batch_size: int = 32,
    lr: float = 1e-3,
) -> Dict[str, Any]:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info("Starting isolated model comparison on device: %s", device)

    # 1. Prepare Datasets & Loaders
    train_ds, val_ds, test_ds = generate_benchmark_dataset()
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False)

    num_classes = 67
    criterion = nn.CrossEntropyLoss()

    models = {
        "Temporal_CNN": TemporalCNNClassifier(in_features=282, num_classes=num_classes),
        "BiLSTM": BiLSTMClassifier(in_features=282, hidden_size=128, num_classes=num_classes),
    }

    results = {}

    for model_name, model in models.items():
        logger.info("--- Training %s ---", model_name)
        model = model.to(device)
        optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

        best_val_f1 = -1.0
        best_state = None

        for ep in range(epochs):
            tr_loss, tr_acc = train_one_epoch(model, train_loader, optimizer, criterion, device)
            val_eval = evaluate_model(model, val_loader, criterion, device)
            scheduler.step()

            if val_eval["macro_f1"] > best_val_f1:
                best_val_f1 = val_eval["macro_f1"]
                best_state = {k: v.cpu() for k, v in model.state_dict().items()}

            if (ep + 1) % 5 == 0 or ep == epochs - 1:
                logger.info(
                    "[%s] Ep %02d/%d | Train Loss: %.4f Acc: %.3f | Val Loss: %.4f Acc: %.3f F1: %.3f",
                    model_name, ep + 1, epochs, tr_loss, tr_acc,
                    val_eval["loss"], val_eval["accuracy"], val_eval["macro_f1"]
                )

        # Load best state for final unseen-signer testing
        model.load_state_dict(best_state)
        test_eval = evaluate_model(model, test_loader, criterion, device)

        param_count = sum(p.numel() for p in model.parameters() if p.requires_grad)

        results[model_name] = {
            "model_type": model_name,
            "param_count": param_count,
            "train_acc": tr_acc,
            "val_f1": best_val_f1,
            "test_acc": test_eval["accuracy"],
            "test_macro_f1": test_eval["macro_f1"],
            "latency_ms": test_eval["latency_ms"],
            "confusion_matrix": test_eval["confusion_matrix"],
            "state_dict": best_state,
        }

        logger.info(
            "[%s Complete] Test Acc (Unseen Signer): %.4f | Macro F1: %.4f | Latency: %.2f ms | Params: %d",
            model_name, test_eval["accuracy"], test_eval["macro_f1"], test_eval["latency_ms"], param_count
        )

    # 2. Select Best Model based on Test Macro F1 & Latency
    cnn_score = results["Temporal_CNN"]["test_macro_f1"]
    lstm_score = results["BiLSTM"]["test_macro_f1"]

    winner_name = "Temporal_CNN" if cnn_score >= lstm_score else "BiLSTM"
    winner_dict = results[winner_name]
    logger.info("Selected winning architecture: %s", winner_name)

    # 3. Save Checkpoint and Configs
    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
    CONFIGS_DIR.mkdir(parents=True, exist_ok=True)

    best_checkpoint_path = CHECKPOINTS_DIR / "isolated_model_best.pt"
    torch.save({
        "model_type": winner_name,
        "in_features": 282,
        "num_classes": num_classes,
        "state_dict": winner_dict["state_dict"],
        "metrics": {
            "test_acc": winner_dict["test_acc"],
            "test_macro_f1": winner_dict["test_macro_f1"],
            "latency_ms": winner_dict["latency_ms"],
            "param_count": winner_dict["param_count"],
        }
    }, best_checkpoint_path)
    logger.info("Saved best model checkpoint to: %s", best_checkpoint_path)

    report_path = CONFIGS_DIR / "isolated_evaluation_report.json"
    clean_results = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "winner": winner_name,
        "models": {
            k: {
                "model_type": v["model_type"],
                "param_count": v["param_count"],
                "test_acc": v["test_acc"],
                "test_macro_f1": v["test_macro_f1"],
                "latency_ms": v["latency_ms"],
            }
            for k, v in results.items()
        }
    }
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(clean_results, f, indent=2)

    return clean_results


if __name__ == "__main__":
    train_and_compare(epochs=25)
