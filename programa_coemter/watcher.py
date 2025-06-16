import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .constants import PDF_FOLDER

class PDFHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith('.pdf'):
            subprocess.Popen(['python', '-m', 'programa_coemter', '--auto', event.src_path])


def watch_folder():
    observer = Observer()
    handler = PDFHandler()
    observer.schedule(handler, PDF_FOLDER, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
