import re
from logging.handlers import RotatingFileHandler
import logging
import PyPDF2
from .constants import LOG_FILE

logger = logging.getLogger(__name__)

handler = RotatingFileHandler(
    LOG_FILE, maxBytes=5*1024*1024, backupCount=5
)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class PDFExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def read_pdf(self):
        text = ''
        pages = []
        with open(self.pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for idx, page in enumerate(reader.pages, start=1):
                page_text = page.extract_text() or ''
                pages.append(page_text)
                text += page_text + '\n'
                logger.info('Read page %d', idx)
        return text, pages

    @staticmethod
    def group_records(text):
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        records = []
        header = re.compile(r'^(?:10\d{5}|1C\d+)\s+Uds.?', re.IGNORECASE)
        bounds = [i for i, l in enumerate(lines) if header.match(l)]
        for i, start in enumerate(bounds):
            end = bounds[i+1] if i+1 < len(bounds) else len(lines)
            records.append(' '.join(lines[start:end]))
        return records

    def extract_data(self):
        text, _ = self.read_pdf()
        recs = self.group_records(text)
        pattern = re.compile(
            r'(?P<art>(?:10\d{5}|1C\d+))\s+Uds.?\s+'
            r'(?P<price>[\d.,]+)\s+(?:[\d.,]+\s+)?'
            r'(?P<units>[\d.,]+)\s+(?P<desc>.+?)(?:\s+(?P<ver>[A-Z0-9]+))?\s*$',
            re.IGNORECASE
        )
        extracted = []
        for r in recs:
            m = pattern.search(r)
            if m:
                art = m.group('art')
                units = m.group('units')
                desc = m.group('desc').strip().rstrip('.')
                ver = (m.group('ver') or 'NC').upper()
                extracted.append((art, units, desc, ver))
        mdate = re.search(r'(?:Data|Fecha) de entrega[:\s]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text)
        delivery_date = mdate.group(1) if mdate else ''
        return delivery_date, extracted
