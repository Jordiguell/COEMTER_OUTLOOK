import os
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .pdf_extractor import PDFExtractor
from .db import save_to_db
from .lantek import generate_ahk

class CoemterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Programa Coemter')
        self.create_widgets()
        self.lines = []
        self.order_code = ''
        self.delivery_date = ''

    def create_widgets(self):
        frm = ttk.Frame(self.root, padding=10)
        frm.pack(fill='both', expand=True)
        self.txt = tk.Text(frm, width=80, height=20)
        self.txt.pack()
        btn = ttk.Button(frm, text='Obrir PDF', command=self.open_pdf)
        btn.pack(pady=5)
        self.btn_save = ttk.Button(frm, text='Guardar', command=self.save, state='disabled')
        self.btn_save.pack(pady=5)

    def open_pdf(self):
        path = filedialog.askopenfilename(filetypes=[('PDF','*.pdf')])
        if not path:
            return
        self.order_code = os.path.splitext(os.path.basename(path))[0]
        extractor = PDFExtractor(path)
        self.delivery_date, self.lines = extractor.extract_data()
        self.txt.delete('1.0', tk.END)
        for art,u,d,v in self.lines:
            self.txt.insert(tk.END, f"{art} {u} {d} {v}\n")
        self.pdf_path = path
        self.btn_save['state'] = 'normal'

    def save(self):
        file_list = "\n".join(f"{a};{u};{d};{v}" for a,u,d,v in self.lines)
        ahk_path = generate_ahk(self.order_code, file_list)
        save_to_db(self.order_code, self.delivery_date, None, None, self.lines, pdf_path=self.pdf_path, ahk_path=ahk_path)
        messagebox.showinfo('Info', f'Dades guardades. Script: {ahk_path}')


def crear_interficie():
    root = tk.Tk()
    app = CoemterGUI(root)
    return root
