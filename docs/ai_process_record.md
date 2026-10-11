# AI协作过程记录
## 前置：自己先完成需求澄清清单，再把需求提交给AI
### 任务拆解（人工预先拆分）
1. 搭建FastAPI项目结构，SQLite数据库表设计
2. Pydantic模型编写，参数校验
3. POST /records新增接口
4. GET /records 筛选+分页查询接口
5. GET /summary收支统计接口
6. 编写pytest测试用例，包含正常场景与至少2个异常边界场景
7. 处理错误返回4xx结构化响应

## 关键对话摘要
Prompt1：
> 根据下面需求写FastAPI记账接口，SQLite存储。POST/records新增流水；GET/records支持筛选分页；GET/summary做时间段收支汇总。要求pydantic校验：amount>0；type只能收入/支出；日期YYYY‑MM‑DD，非法参数返回4xx。同时写pytest测试用例，包含正常用例和至少2个边界异常用例。

AI第一版输出问题：
1. SQL where条件直接字符串拼接，存在SQL注入风险
2. 缺少日期格式的强校验
3. 分页逻辑简单，没有处理offset计算

Prompt2：
> 修改代码，把SQL改成参数化查询；增加ISO日期格式校验；完善分页逻辑page从1开始；输出pytest异步测试用例。

AI修改输出后：分页、校验补齐，但统计接口没有处理无数据返回None，会造成返回null。人工修复把空sum处理为0.0。

## 关键代码修改diff
1. ❌AI原始代码：拼接where条件字符串
✅人工修改：使用?占位符参数化查询，防止SQL注入
2. ❌AI原始：没有日期合法性校验
✅人工增加field_validator，调用date.fromisoformat校验日期格式
3. ❌AI原始：SUM无数据返回None
✅业务代码中手动初始化income=0.0 expense=0.0，避免返回null
4. ❌AI测试用例缺少边界场景
✅补充amount=0、非法type两个异常测试case