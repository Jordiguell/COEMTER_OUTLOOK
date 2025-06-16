import os
from .constants import SCRIPTS_DIR


def build_ahk_script(order_code: str, file_list: str) -> str:
    """Save AutoHotkey script with the given file list."""
    os.makedirs(SCRIPTS_DIR, exist_ok=True)
    ahk_path = os.path.join(SCRIPTS_DIR, f"{order_code}.ahk")
    script = f"; Auto-generated AHK for {order_code}\n; files:\n{file_list}\n"
    with open(ahk_path, 'w', encoding='utf-8') as fh:
        fh.write(script)
    return ahk_path
