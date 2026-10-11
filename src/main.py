from fastapi import FastAPI, Query
from contextlib import asynccontextmanager
from .database import init_db, get_db_conn
from .schemas import RecordCreate, RecordPageResp, RecordItem, SummaryResp
from typing import Optional

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时执行（替代原来 startup）
    init_db()
    yield
    # 应用关闭时执行，可以在这里关闭资源，当前项目无需操作
    print("服务已关闭")

app = FastAPI(title="简易记账接口", lifespan=lifespan)

@app.get("/")
async def index():
    return {"message": "FastAPI记账系统服务", "docs": "http://127.0.0.1:8000/docs"}

@app.post("/records", response_model=RecordItem)
def add_record(item: RecordCreate):
    """新增一条记账流水"""
    with get_db_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO records (amount, type, category, record_date)
               VALUES (?, ?, ?, ?)""",
            (item.amount, item.type, item.category, item.record_date)
        )
        conn.commit()
        new_id = cur.lastrowid
        row = cur.execute("SELECT * FROM records WHERE id=?", (new_id,)).fetchone()
        return dict(row)

@app.get("/records", response_model=RecordPageResp)
def get_records(
    record_type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    where_parts = []
    params = []
    if record_type:
        where_parts.append("type = ?")
        params.append(record_type)
    if category:
        where_parts.append("category = ?")
        params.append(category)
    if start_date:
        where_parts.append("record_date >= ?")
        params.append(start_date)
    if end_date:
        where_parts.append("record_date <= ?")
        params.append(end_date)

    where_sql = "WHERE " + " AND ".join(where_parts) if where_parts else ""

    with get_db_conn() as conn:
        cur = conn.cursor()
        count_sql = f"SELECT COUNT(*) AS cnt FROM records {where_sql}"
        total = cur.execute(count_sql, params).fetchone()["cnt"]

        offset = (page - 1) * page_size
        data_sql = f"SELECT * FROM records {where_sql} LIMIT ? OFFSET ?"
        rows = cur.execute(data_sql, params + [page_size, offset]).fetchall()
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "data": [dict(r) for r in rows]
        }

@app.get("/summary", response_model=SummaryResp)
def get_summary(
    start_date: str = Query(...),
    end_date: str = Query(...)
):
    with get_db_conn() as conn:
        cur = conn.cursor()
        sql = """
        SELECT type, SUM(amount) as sum_amt
        FROM records
        WHERE record_date >= ? AND record_date <= ?
        GROUP BY type
        """
        res = cur.execute(sql, (start_date, end_date)).fetchall()
        income = 0.0
        expense = 0.0
        for row in res:
            if row["type"] == "收入":
                income = row["sum_amt"]
            elif row["type"] == "支出":
                expense = row["sum_amt"]
        balance = income - expense
        return {
            "income_total": income,
            "expense_total": expense,
            "balance": balance
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)