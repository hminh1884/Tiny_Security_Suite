import subprocess

class FirewallService:
    @staticmethod
    def get_status() -> str:
        p = subprocess.run(["netsh", "advfirewall", "show", "allprofiles"], capture_output=True, text=True, shell=True)
        return (p.stdout or "").strip()

    @staticmethod
    def add_block_rule(rule_name: str, port: str):
        cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=block protocol=TCP localport={port}'
        subprocess.run(cmd, check=True, shell=True)