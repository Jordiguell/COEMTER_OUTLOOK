import os
import subprocess
from .pdf_extractor import PDFExtractor
from .db import save_to_db
from .constants import PDF_FOLDER
from .lantek import generate_ahk


def process_pdf(pdf_path):
    extractor = PDFExtractor(pdf_path)
    delivery_date, lines = extractor.extract_data()
    order_code = os.path.splitext(os.path.basename(pdf_path))[0]
    file_list = "\n".join(f"{a};{u};{d};{v}" for a,u,d,v in lines)
    ahk_path = generate_ahk(order_code, file_list)
    save_to_db(order_code, delivery_date, None, None, lines, pdf_path=pdf_path, ahk_path=ahk_path)
    return order_code, delivery_date, ahk_path


def run_auto(pdf_path):
    order_code, delivery_date, ahk_path = process_pdf(pdf_path)
    print(f"Processed {order_code} delivery {delivery_date}")
    print(f"AHK: {ahk_path}")
    return order_code
