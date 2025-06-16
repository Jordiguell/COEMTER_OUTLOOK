import os
from threading import Event
from .pdf_extractor import PDFExtractor
from .db import save_order
from .constants import PDF_FOLDER
from .lantek import build_ahk_script
from .sage_utils import sage_ready, keep_awake
import logging
import xlsxwriter

logger = logging.getLogger(__name__)


def exportar_excel(order_code, lines, delivery_date, sale_no, buy_no):
    path = os.path.join(PDF_FOLDER, f"{order_code}_ordenes.xlsx")
    wb = xlsxwriter.Workbook(path)
    ws = wb.add_worksheet()
    ws.write_row(0, 0, ["Article", "Unitats", "Descripcio", "Versio"])
    for row, (a, u, d, v) in enumerate(lines, start=1):
        ws.write_row(row, 0, [a, u, d, v])
    wb.close()
    return path


def enviar_a_sage(lines, delivery_date):
    logger.info("Sending to Sage - placeholder")
    # Placeholder numbers
    return "0", "0"


def process_pdf(pdf_path):
    extractor = PDFExtractor(pdf_path)
    delivery_date, lines = extractor.extract_data()
    order_code = os.path.splitext(os.path.basename(pdf_path))[0]
    sale_no, buy_no = enviar_a_sage(lines, delivery_date)
    file_list = "\n".join(f"{a};{u};{d};{v}" for a, u, d, v in lines)
    ahk_path = build_ahk_script(order_code, file_list)
    excel_path = exportar_excel(order_code, lines, delivery_date, sale_no, buy_no)
    save_order(order_code, delivery_date, sale_no, buy_no, pdf_path, excel_path, ahk_path, lines)
    return order_code


def run_auto(pdf_path):
    if not sage_ready():
        logger.error("Sage not ready")
        return 1
    stop_event = Event()
    keep_awake(stop_event)
    try:
        order_code = process_pdf(pdf_path)
        logger.info("Processed %s", order_code)
        return 0
    finally:
        stop_event.set()
