import subprocess
from pathlib import Path

class FolderService:
    @staticmethod
    def hide_folder(path: str):
        subprocess.run(["attrib", "+h", "+s", str(Path(path))], check=True, shell=True)

    @staticmethod
    def unhide_folder(path: str):
        subprocess.run(["attrib", "-h", "-s", str(Path(path))], check=True, shell=True)