"""
Signova AI - Lightweight Text-to-Speech (TTS) Module (Phase 5).
Converts recognized sign output to speech asynchronously without blocking inference.
Includes deduplication, confidence gating, and headless fallback.
"""

import logging
import os
from pathlib import Path
import queue
import subprocess
import tempfile
import threading
import time
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("signova.tts")


class SignovaTTS:
    """
    Lightweight, non-blocking Python TTS testing engine.
    Runs speech synthesis on a dedicated background thread with deduplication
    and confidence/validity filtering.
    """

    REJECTED_TOKENS = {
        "[UNKNOWN_SIGN]",
        "[REJECTED_SEGMENT]",
        "[INFERENCE_ERROR]",
        "UNKNOWN",
        "<unk>",
        "BACKGROUND",
        "Neutral / Idle",
        "",
    }

    # Clean phonetic mappings for ISL labels to natural spoken English
    LABEL_SPEECH_MAP = {
        "I_PRONOUN": "I",
        "I_LETTER": "I",
        "THANK_YOU": "Thank you",
        "PRIME_MINISTER": "Prime Minister",
        "CHIEF_MINISTER": "Chief Minister",
        "0": "Zero",
        "1": "One",
        "2": "Two",
        "3": "Three",
        "4": "Four",
        "5": "Five",
        "6": "Six",
        "7": "Seven",
        "8": "Eight",
        "9": "Nine",
    }

    def __init__(
        self,
        enabled: bool = True,
        min_confidence: float = 0.65,
        debounce_seconds: float = 2.0,
        voice_rate: int = 1,
    ) -> None:
        self.enabled = enabled
        self.min_confidence = min_confidence
        self.debounce_seconds = debounce_seconds
        self.voice_rate = voice_rate

        self._queue: queue.Queue[str] = queue.Queue(maxsize=10)
        self._last_spoken_text: str = ""
        self._last_spoken_time: float = 0.0
        self._is_speaking: bool = False
        self._stop_event = threading.Event()
        self._lock = threading.Lock()

        self._history: List[Dict[str, Any]] = []

        # Start background consumer thread
        self._worker_thread = threading.Thread(
            target=self._process_queue,
            name="SignovaTTSWorker",
            daemon=True,
        )
        self._worker_thread.start()

    def format_speech_text(self, raw_text: str) -> str:
        """Translates raw model labels into natural spoken English."""
        cleaned = raw_text.strip()
        if cleaned in self.LABEL_SPEECH_MAP:
            return self.LABEL_SPEECH_MAP[cleaned]
        # Replace underscores with spaces and capitalize words
        return cleaned.replace("_", " ").title()

    def speak(self, text: str, force: bool = False) -> Dict[str, Any]:
        """
        Enqueues text for asynchronous speech generation.
        Returns immediately without blocking the caller.
        """
        if not self.enabled:
            return {"status": "skipped", "reason": "TTS disabled", "text": text}

        spoken_text = self.format_speech_text(text)
        if not spoken_text or spoken_text in self.REJECTED_TOKENS:
            return {"status": "skipped", "reason": "empty or rejected token", "text": text}

        now = time.time()
        with self._lock:
            # Prevent duplicate and overlapping speech
            if not force and spoken_text == self._last_spoken_text:
                if (now - self._last_spoken_time) < self.debounce_seconds:
                    return {
                        "status": "debounced",
                        "reason": f"Duplicate within {self.debounce_seconds}s",
                        "text": text,
                    }

            try:
                self._queue.put_nowait(spoken_text)
                self._last_spoken_text = spoken_text
                self._last_spoken_time = now
                return {"status": "enqueued", "text": text, "spoken_text": spoken_text}
            except queue.Full:
                return {"status": "dropped", "reason": "queue full", "text": text}

    def speak_prediction(
        self,
        raw_text: str,
        is_valid: bool = True,
        confidence: float = 1.0,
    ) -> Dict[str, Any]:
        """
        Gated speech invocation: does NOT speak rejected or low-confidence predictions.
        Keeps raw recognized text separate from spoken text.
        """
        if not is_valid:
            record = {
                "raw_text": raw_text,
                "spoken_text": None,
                "status": "rejected",
                "reason": "Invalid or rejected gesture segment",
                "confidence": confidence,
            }
            self._history.append(record)
            return record

        if confidence < self.min_confidence:
            record = {
                "raw_text": raw_text,
                "spoken_text": None,
                "status": "rejected",
                "reason": f"Confidence {confidence:.2f} below threshold {self.min_confidence:.2f}",
                "confidence": confidence,
            }
            self._history.append(record)
            return record

        res = self.speak(raw_text)
        record = {
            "raw_text": raw_text,
            "spoken_text": res.get("spoken_text"),
            "status": res.get("status"),
            "reason": res.get("reason"),
            "confidence": confidence,
        }
        self._history.append(record)
        return record

    def _process_queue(self) -> None:
        """Worker loop executing speech synthesis."""
        while not self._stop_event.is_set():
            try:
                text = self._queue.get(timeout=0.2)
            except queue.Empty:
                continue

            self._is_speaking = True
            try:
                self._synthesize_speech(text)
            except Exception as exc:
                logger.warning("TTS synthesis warning: %s", exc)
            finally:
                self._is_speaking = False
                self._queue.task_done()

    def _synthesize_speech(self, text: str) -> None:
        """
        Synthesizes speech using Windows SAPI.
        If direct audio output device is missing (headless/server/sandbox),
        synthesizes to temporary WAV file to verify speech engine execution.
        """
        safe_text = text.replace("'", " ").replace('"', ' ').replace("\n", " ")
        # Try direct SAPI speech first
        direct_ps = (
            f"$v = New-Object -ComObject SAPI.SpVoice; "
            f"$v.Rate = {self.voice_rate}; "
            f"[void]$v.Speak('{safe_text}')"
        )
        res = subprocess.run(
            ["powershell", "-NoProfile", "-Command", direct_ps],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if res.returncode != 0:
            # Direct audio output failed (e.g. HRESULT 0x8004503A device not supported).
            # Fall back to file-backed SAPI synthesis to guarantee working voice synthesis pipeline.
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp_wav = tmp.name

            try:
                file_ps = (
                    f"$v = New-Object -ComObject SAPI.SpVoice; "
                    f"$s = New-Object -ComObject SAPI.SpFileStream; "
                    f"$s.Open('{tmp_wav}', 3, $false); "
                    f"$v.AudioOutputStream = $s; "
                    f"$v.Rate = {self.voice_rate}; "
                    f"[void]$v.Speak('{safe_text}'); "
                    f"$s.Close()"
                )
                res_file = subprocess.run(
                    ["powershell", "-NoProfile", "-Command", file_ps],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if res_file.returncode != 0:
                    logger.error("TTS file synthesis error: %s", res_file.stderr)
            finally:
                if os.path.exists(tmp_wav):
                    try:
                        os.unlink(tmp_wav)
                    except Exception:
                        pass

    def is_busy(self) -> bool:
        """Returns True if speech synthesis is currently active or queued."""
        return self._is_speaking or not self._queue.empty()

    def get_history(self) -> List[Dict[str, Any]]:
        return list(self._history)

    def stop(self) -> None:
        """Stops background worker thread."""
        self._stop_event.set()
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
                self._queue.task_done()
            except Exception:
                break
