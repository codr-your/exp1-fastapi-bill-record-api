import sqlite3
from contextlib import contextmanager
from pathlib import Path

# 始终指向项目根目录下的 bookkeeping.db，与运行目录无关
DB_FILE = Path(__file__).resolve().parent.parent / "bookkeeping.db"


@contextmanager
def get_db_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    with get_db_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            record_date TEXT NOT NULL
        )
        """)
        conn.commit()


def reset_db():
    """清空 records 表，供测试前重置数据用。"""
    init_db()  # 确保表存在
    with get_db_conn() as conn:
        conn.execute("DELETE FROM records")
        conn.commit()


if __name__ == "__main__":
    init_db()