import sqlite3
from .constants import DB_PATH

CREATE_ORDERS = '''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_code TEXT,
    delivery_date TEXT,
    sage_sale_no TEXT,
    sage_buy_no TEXT,
    pdf_path TEXT,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    excel_path TEXT,
    ahk_path TEXT
);
'''

CREATE_LINES = '''
CREATE TABLE IF NOT EXISTS order_lines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER REFERENCES orders(id),
    article TEXT,
    units REAL,
    description TEXT,
    version TEXT
);
'''

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(CREATE_ORDERS)
    cur.execute(CREATE_LINES)
    conn.commit()
    conn.close()

def save_to_db(order_code, delivery_date, sage_sale_no, sage_buy_no, lines, pdf_path=None, excel_path=None, ahk_path=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO orders(order_code, delivery_date, sage_sale_no, sage_buy_no, pdf_path, excel_path, ahk_path) VALUES(?,?,?,?,?,?,?)',
        (order_code, delivery_date, sage_sale_no, sage_buy_no, pdf_path, excel_path, ahk_path)
    )
    order_id = cur.lastrowid
    for art, units, desc, ver in lines:
        cur.execute(
            'INSERT INTO order_lines(order_id, article, units, description, version) VALUES(?,?,?,?,?)',
            (order_id, art, units, desc, ver)
        )
    conn.commit()
    conn.close()
    return order_id
