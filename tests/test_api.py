import sys
from pathlib import Path
# 项目根目录加入搜索路径
sys.path.append(str(Path(__file__).parent.parent))

import pytest
import pytest_asyncio
pytestmark = pytest.mark.asyncio
from httpx import AsyncClient, ASGITransport
from src.main import app
from src.database import reset_db


@pytest_asyncio.fixture
async def ac():
    """异步 fixture：正确管理 FastAPI lifespan + ASGITransport
    每个测试前先清空数据库，保证用例之间互不干扰。"""
    reset_db()
    transport = ASGITransport(app=app)
    async with app.router.lifespan_context(app):
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client


async def test_create_normal_record(ac: AsyncClient):
    """正常新增流水【正常用例】"""
    resp = await ac.post("/records", json={
        "amount": 100.5,
        "type": "收入",
        "category": "工资",
        "record_date": "2026-09-01"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["amount"] == 100.5
    assert data["type"] == "收入"


async def test_create_bad_amount_zero(ac: AsyncClient):
    """边界异常用例1：金额等于0，返回422"""
    resp = await ac.post("/records", json={
        "amount": 0,
        "type": "支出",
        "category": "餐饮",
        "record_date": "2026-09-02"
    })
    assert resp.status_code == 422


async def test_create_wrong_type(ac: AsyncClient):
    """边界异常用例2：type传非法值，返回422"""
    resp = await ac.post("/records", json={
        "amount": 50,
        "type": "转账",
        "category": "其它",
        "record_date": "2026-09-03"
    })
    assert resp.status_code == 422


async def test_summary_query(ac: AsyncClient):
    """测试summary汇总统计接口"""
    resp = await ac.get("/summary", params={
        "start_date": "2026-09-01",
        "end_date": "2026-09-30"
    })
    assert resp.status_code == 200
    js = resp.json()
    assert "income_total" in js
    assert "balance" in js