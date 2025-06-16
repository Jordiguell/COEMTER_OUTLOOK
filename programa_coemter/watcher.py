import time
import subprocess
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .constants import PDF_FOLDER, WATCHER_RETRY_DELAY, WATCHER_MAX_RETRY

attempts = {}


def _process(path):
    cmd = ['python', '-m', 'programa_coemter', '--auto', path]
    proc = subprocess.run(cmd)
    if proc.returncode != 0:
        n = attempts.get(path, 0) + 1
        if n < WATCHER_MAX_RETRY:
            attempts[path] = n
            threading.Timer(WATCHER_RETRY_DELAY, _process, args=[path]).start()


class PDFHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith('.pdf'):
            attempts[event.src_path] = 0
            _process(event.src_path)


def watch_folder(stop_event=None):
    observer = Observer()
    handler = PDFHandler()
    observer.schedule(handler, PDF_FOLDER, recursive=False)
    observer.start()
    try:
        while stop_event is None or not stop_event.is_set():
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
