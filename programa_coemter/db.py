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
    excel_path TEXT,
    ahk_path TEXT,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''

CREATE_LINES = '''
CREATE TABLE IF NOT EXISTS order_lines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    article TEXT,
    units REAL,
    description TEXT,
    version TEXT
);
'''

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(CREATE_ORDERS)
    cur.execute(CREATE_LINES)
    conn.commit()
    conn.close()

def save_order(order_code, delivery_date, sage_sale, sage_buy, pdf, excel, ahk, lines):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO orders(order_code, delivery_date, sage_sale_no, sage_buy_no, pdf_path, excel_path, ahk_path) '
        'VALUES(?,?,?,?,?,?,?)',
        (order_code, delivery_date, sage_sale, sage_buy, pdf, excel, ahk)
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
