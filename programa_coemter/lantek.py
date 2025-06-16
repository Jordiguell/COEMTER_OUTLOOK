import os
from .constants import BASE_DIR

SCRIPTS_DIR = os.path.join(BASE_DIR, 'scripts', 'lantek')
os.makedirs(SCRIPTS_DIR, exist_ok=True)

def generate_ahk(order_code, file_list_str):
    """Generate AHK script for Lantek using file list."""
    ahk_path = os.path.join(SCRIPTS_DIR, f"{order_code}.ahk")
    script = f"; Auto generated script\n; files:\n{file_list_str}\n"
    with open(ahk_path, 'w', encoding='utf-8') as fh:
        fh.write(script)
    return ahk_path
