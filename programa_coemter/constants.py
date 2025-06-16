import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_FOLDER = os.path.join(BASE_DIR, '..', 'pdfs')
DWG_ROOT = os.path.join(BASE_DIR, '..', 'dwg')
TEMP_FOLDER = os.path.join(BASE_DIR, '..', 'temp', 'dwg_selection')
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'pdf_extractor.log')
DB_PATH = os.path.join(BASE_DIR, 'orders.db')
SLEEP_SHORT = 0.6
SLEEP_MEDIUM = 0.8
SLEEP_LONG = 1
SLEEP_EXTRA_LONG = 2
