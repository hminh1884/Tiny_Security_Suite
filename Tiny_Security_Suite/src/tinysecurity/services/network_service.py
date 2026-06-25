import subprocess
from pathlib import Path

class NetworkService:
    @staticmethod
    def start_openvpn(config_path: str, exe_path: str = "openvpn"):
        cfg = Path(config_path)
        if not cfg.exists():
            raise FileNotFoundError(f"Không tìm thấy file cấu hình: {cfg}")
        subprocess.Popen([exe_path, "--config", str(cfg)], creationflags=subprocess.CREATE_NEW_CONSOLE)

    @staticmethod
    def launch_tor(tor_exe_path: str):
        p = Path(tor_exe_path)
        if not p.exists():
            raise FileNotFoundError(f"Không tìm thấy Tor Browser: {p}")
        subprocess.Popen([str(p)])