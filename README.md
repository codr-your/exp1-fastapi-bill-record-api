# FastAPI 简易记账接口

一个基于 FastAPI + SQLite 的轻量级记账系统，支持流水新增、筛选分页查询、时间段收支汇总，参数校验完善，自带 pytest 异步测试。

## 功能特性

- 📝 **新增流水** — 支持收入/支出记录，Pydantic 自动校验金额、类型、日期格式
- 🔍 **筛选查询** — 按类型、分类、日期区间过滤，支持分页
- 📊 **收支汇总** — 指定时间段，一键统计总收入、总支出、结余
- ✅ **参数校验** — amount > 0，type 限定为「收入/支出」，日期强制 ISO 格式，非法请求统一返回 422
- 🧪 **异步测试** — 基于 pytest-asyncio + httpx 覆盖正常/异常边界场景

## 技术栈

| 组件 | 版本 |
|------|------|
| Python | 3.14+ |
| FastAPI | 0.143 |
| Pydantic | 2.x |
| SQLite | 标准库内置 |
| httpx | 0.28 |
| pytest | 9.x + pytest-asyncio 1.x |

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```
### 2. 启动服务
```bash
python -m src.main
```

启动后访问：
- API 地址：http://127.0.0.1:8000/
- Swagger 文档（可交互调试）：http://127.0.0.1:8000/docs

> 首次启动时 lifespan 会自动调用 `init_db()` 创建数据库表。

### 3. 运行测试
```bash
pytest tests/ -v
```









