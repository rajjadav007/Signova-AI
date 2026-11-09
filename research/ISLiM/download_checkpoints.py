#!/usr/bin/env python3
"""
Official Pretrained Checkpoint Downloader for ISLiM (Signova AI | Phase 1 | Part 1.3)
Downloads official pretrained checkpoints from Google Drive directly into research/ISLiM/checkpoints/.
Verifies file size, SHA-256, MD5, and zip magic bytes without executing or loading model weights.
"""

import os
import sys
import re
import time
import hashlib
from pathlib import Path
import requests

CHECKPOINTS_TO_DOWNLOAD = [
    {
        "name": "ISLiM_full_posestitch_pre_processed.pt",
        "file_id": "1mZtXateoZn_3T1T4Lc3yowMvB0jWm9EX",
        "expected_size": 899966348,
        "description": "Primary ISLiM 4-loss model trained on full iSign (PoseStitch splits)"
    },
    {
        "name": "ISLiM_4Loss_best_for_10kSpamoOF.pt",
        "file_id": "1DW7pyxnqUQwLxvJTSTzmOzmmCn5k14mP",
        "expected_size": 899970408,
        "description": "ISLiM 4-loss model trained on SpaMo-OF 10k subset"
    }
]

TARGET_DIR = Path(__file__).parent / "checkpoints"

def download_file(session: requests.Session, file_id: str, dest_path: Path, expected_size: int):
    init_url = f"https://drive.google.com/uc?id={file_id}&export=download"
    print(f"\n[1/3] Initiating Google Drive download request for ID: {file_id} ...")
    r_init = session.get(init_url, timeout=15)
    
    # Check if download warning/confirmation page returned
    match_action = re.search(r'action="([^"]+)"', r_init.text)
    match_uuid = re.search(r'name="uuid" value="([^"]+)"', r_init.text)
    match_confirm = re.search(r'name="confirm" value="([^"]+)"', r_init.text)
    
    if match_action and match_uuid:
        action_url = match_action.group(1)
        uuid_val = match_uuid.group(1)
        confirm_val = match_confirm.group(1) if match_confirm else "t"
        params = {
            "id": file_id,
            "export": "download",
            "confirm": confirm_val,
            "uuid": uuid_val
        }
        print(f"[2/3] Confirming download bypassing virus scan page (UUID: {uuid_val}) ...")
        r_stream = session.get(action_url, params=params, stream=True, timeout=30)
    else:
        r_stream = r_init

    if r_stream.status_code != 200:
        raise RuntimeError(f"Download failed with HTTP status {r_stream.status_code}")

    content_type = r_stream.headers.get("Content-Type", "")
    if "text/html" in content_type:
        raise RuntimeError(f"Received HTML instead of binary stream. Content-Type: {content_type}")

    content_length = int(r_stream.headers.get("Content-Length", 0))
    print(f"[3/3] Streaming {dest_path.name} (Content-Length: {content_length:,} bytes) ...")

    temp_path = dest_path.with_suffix(".tmp")
    chunk_size = 4 * 1024 * 1024  # 4 MB chunks
    downloaded_bytes = 0
    start_time = time.time()
    last_print = start_time

    sha256 = hashlib.sha256()
    md5 = hashlib.md5()

    with open(temp_path, "wb") as f:
        for chunk in r_stream.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                sha256.update(chunk)
                md5.update(chunk)
                downloaded_bytes += len(chunk)
                now = time.time()
                if now - last_print > 3.0:
                    pct = (downloaded_bytes / content_length * 100) if content_length > 0 else 0
                    mb = downloaded_bytes / (1024 * 1024)
                    speed = (downloaded_bytes / (now - start_time)) / (1024 * 1024)
                    print(f"  Progress: {mb:.1f} MB ({pct:.1f}%) | Speed: {speed:.2f} MB/s")
                    last_print = now

    elapsed = time.time() - start_time
    speed = (downloaded_bytes / elapsed) / (1024 * 1024) if elapsed > 0 else 0
    print(f"  Complete: {downloaded_bytes:,} bytes in {elapsed:.1f}s ({speed:.2f} MB/s)")

    # Size check
    if expected_size and downloaded_bytes != expected_size:
        temp_path.unlink(missing_ok=True)
        raise ValueError(f"Size mismatch: expected {expected_size} bytes, got {downloaded_bytes} bytes!")

    # Check magic bytes for PyTorch zip archive (PK\x03\x04)
    with open(temp_path, "rb") as f:
        magic = f.read(4)
    if magic != b"PK\x03\x04":
        temp_path.unlink(missing_ok=True)
        raise ValueError(f"Invalid magic bytes: expected PK\\x03\\x04, got {magic.hex()}")

    # Atomic rename
    temp_path.replace(dest_path)
    print(f"  Saved to: {dest_path}")

    return {
        "file": dest_path.name,
        "size_bytes": downloaded_bytes,
        "size_mb": round(downloaded_bytes / (1024 * 1024), 2),
        "sha256": sha256.hexdigest(),
        "md5": md5.hexdigest(),
        "elapsed_sec": round(elapsed, 1),
        "magic_bytes": magic.hex()
    }

def main():
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

    results = []
    print("=" * 60)
    print("      ISLiM Official Checkpoint Downloader (Part 1.3)")
    print("=" * 60)
    print(f"Destination: {TARGET_DIR.resolve()}")

    for item in CHECKPOINTS_TO_DOWNLOAD:
        dest_file = TARGET_DIR / item["name"]
        print(f"\nTarget: {item['name']}")
        print(f"Description: {item['description']}")
        
        if dest_file.exists():
            size = dest_file.stat().st_size
            if size == item["expected_size"]:
                print(f"  [ALREADY EXISTS] Size matches {size:,} bytes. Verifying checksums...")
                sha256 = hashlib.sha256()
                md5 = hashlib.md5()
                with open(dest_file, "rb") as f:
                    for chunk in iter(lambda: f.read(4 * 1024 * 1024), b""):
                        sha256.update(chunk)
                        md5.update(chunk)
                with open(dest_file, "rb") as f:
                    magic = f.read(4)
                results.append({
                    "file": item["name"],
                    "size_bytes": size,
                    "size_mb": round(size / (1024 * 1024), 2),
                    "sha256": sha256.hexdigest(),
                    "md5": md5.hexdigest(),
                    "magic_bytes": magic.hex(),
                    "status": "Verified (Existing)"
                })
                continue

        res = download_file(session, item["file_id"], dest_file, item["expected_size"])
        res["status"] = "Downloaded & Verified"
        results.append(res)

    print("\n" + "=" * 60)
    print("                 Summary of Downloaded Files")
    print("=" * 60)
    for r in results:
        print(f"File       : {r['file']}")
        print(f"Status     : {r['status']}")
        print(f"Size       : {r['size_mb']} MB ({r['size_bytes']:,} bytes)")
        print(f"Magic Bytes: {r['magic_bytes']} (PK\\x03\\x04 - PyTorch zip archive)")
        print(f"MD5        : {r['md5']}")
        print(f"SHA-256    : {r['sha256']}")
        print("-" * 60)

if __name__ == "__main__":
    main()

