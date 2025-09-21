import os
from typing import Callable

CHUNK_SIZE = 1024 * 1024  # 1 MiB chunks

def _write_pattern(path: str, size_bytes: int, pattern: bytes, on_progress: Callable[[float], None] | None = None):
    written = 0
    with open(path, "r+b" if os.path.exists(path) else "w+b") as f:
        while written < size_bytes:
            to_write = min(CHUNK_SIZE, size_bytes - written)
            if len(pattern) == 1:
                buf = pattern * to_write
            else:
                # pattern already the right size
                buf = pattern[:to_write]
                if len(buf) < to_write:
                    # repeat pattern when smaller than chunk
                    times = (to_write // len(pattern)) + 1
                    buf = (pattern * times)[:to_write]
            f.write(buf)
            written += to_write
        f.flush()
        os.fsync(f.fileno())
    if on_progress:
        on_progress(1.0)

def _write_random(path: str, size_bytes: int, on_progress: Callable[[float], None] | None = None):
    import os as _os
    written = 0
    with open(path, "r+b" if os.path.exists(path) else "w+b") as f:
        while written < size_bytes:
            to_write = min(CHUNK_SIZE, size_bytes - written)
            buf = _os.urandom(to_write)
            f.write(buf)
            written += to_write
            if on_progress:
                on_progress(min(0.9999, written / size_bytes))
        f.flush()
        os.fsync(f.fileno())

def run_wipe(method: str, device_uid: str, wipe_id: int, size_mb: int = 32, on_progress: Callable[[float], None] | None = None):
    """
    Execute wipe over a virtual device file using the requested method.
    - DoD 5220.22-M: 0x00, 0xFF, random
    - NIST: random, 0x00
    - Quick Zero Fill (fallback): 0x00
    """
    # Ensure target directory exists
    base_dir = "/app/data/wipes"
    os.makedirs(base_dir, exist_ok=True)
    path = os.path.join(base_dir, f"{device_uid}-{wipe_id}.img")

    size_bytes = size_mb * 1024 * 1024
    method_norm = method.strip().lower()

    # Map to passes
    if method_norm == "dod 5220.22-m":
        passes = [
            ("zeros", lambda: _write_pattern(path, size_bytes, b"\x00", None)),
            ("ones", lambda: _write_pattern(path, size_bytes, b"\xFF", None)),
            ("random", lambda: _write_random(path, size_bytes, None)),
        ]
    elif method_norm == "nist":
        passes = [
            ("random", lambda: _write_random(path, size_bytes, None)),
            ("zeros", lambda: _write_pattern(path, size_bytes, b"\x00", None)),
        ]
    else:
        # Fallback quick zero fill
        passes = [
            ("zeros", lambda: _write_pattern(path, size_bytes, b"\x00", None)),
        ]

    # Run passes; coarse pass-level progress reporting if provided
    total = len(passes)
    for i, (_label, fn) in enumerate(passes, start=1):
        fn()
        if on_progress:
            on_progress(i / total)

    # Optional lightweight verification: ensure file size matches target
    actual_size = os.path.getsize(path)
    if actual_size != size_bytes:
        raise RuntimeError(f"Verification failed: size {actual_size} != expected {size_bytes}")

    return path