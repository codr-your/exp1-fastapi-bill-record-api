# 需求澄清清单｜FastAPI简易记账接口
## 业务目标
实现简易记账HTTP服务，存储使用SQLite；完成流水新增、筛选分页查询、时间段收支汇总统计。

## 输入输出定义
1. POST /records 新增流水
- 请求字段：
  amount：金额，必须>0；
  type：只能【收入 / 支出】；
  category：分类，字符串；
  record_date：日期，格式 YYYY‑MM‑DD；
- 返回：完整新增记录（含自增id）
- 非法参数：返回4xx（422）结构化错误信息

2. GET /records 查询流水
- 查询参数（可选筛选）：type、category、start_date、end_date
- 分页参数：page（页码从1开始），page_size每页条数
- 返回：total总条数、page、page_size、data记录数组

3. GET /summary 收支汇总
- 必填查询参数：start_date、end_date
- 返回字段：income_total收入合计、expense_total支出合计、balance结余=收入‑支出

## 边界条件
1. amount ≤ 0：校验失败拒绝创建
2. type不是【收入/支出】：校验失败
3. record_date日期格式不符合YYYY‑MM‑DD：校验失败
4. 查询区间无数据：收入、支出返回0，结余为0
5. 非法查询参数，返回422，返回结构化错误体，服务不能崩溃
6. 并发写入场景：保证数据写入不发生错乱（SQLite文件锁机制）

## 验收标准
1. 服务可以本地一键启动；访问/docs接口文档可以调试
2. 全部接口功能符合需求，统计结果数值正确
3. 参数校验生效，错误请求返回4xx状态码
4. pytest测试脚本运行通过，包含正常用例，至少2个边界异常用例
5. 并发写入数据一致性有方案说明