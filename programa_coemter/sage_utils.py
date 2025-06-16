import threading
import time
import psutil
import pyautogui
import win32gui
import win32process


def sage_ready(window_title=r"Sage 200 | Advanced Edition") -> bool:
    """Check if Sage window is present and unlocked."""
    if win32gui.GetForegroundWindow() == 0:
        return False
    hwnd = win32gui.FindWindow(None, window_title)
    if not hwnd:
        def cb(h, results):
            if window_title in win32gui.GetWindowText(h):
                results.append(h)
        res = []
        win32gui.EnumWindows(cb, res)
        if res:
            hwnd = res[0]
        else:
            return False
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    return psutil.pid_exists(pid)


def keep_awake(stop_event: threading.Event) -> threading.Thread:
    """Press Shift every 60s until stop_event is set."""
    def _loop():
        while not stop_event.is_set():
            pyautogui.press('shift')
            for _ in range(60):
                if stop_event.is_set():
                    break
                time.sleep(1)
    t = threading.Thread(target=_loop, daemon=True)
    t.start()
    return t
