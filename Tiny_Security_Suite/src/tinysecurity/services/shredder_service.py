import os
from pathlib import Path

class ShredderService:
    @staticmethod
    def shred_file(file_path: str, passes: int = 1):
        p = Path(file_path)
        if not p.exists() or not p.is_file():
            raise FileNotFoundError("File không tồn tại.")
        length = p.stat().st_size
        with p.open("r+b") as f:
            for _ in range(max(1, passes)):
                f.seek(0)
                f.write(os.urandom(length))
                f.flush()
                os.fsync(f.fileno())
        p.unlink()