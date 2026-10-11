from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Optional, List

class RecordCreate(BaseModel):
    amount: float = Field(gt=0, description="金额必须大于0")
    type: str = Field(description="只能是 收入 / 支出")
    category: str
    record_date: str

    @field_validator("type")
    def check_record_type(cls, v):
        if v not in ("收入", "支出"):
            raise ValueError("type只能是【收入】或【支出】")
        return v

    @field_validator("record_date")
    def check_date_format(cls, v):
        # 校验日期格式必须符合 yyyy-MM-dd ISO标准格式
        date.fromisoformat(v)
        return v

class RecordItem(RecordCreate):
    id: int

class RecordPageResp(BaseModel):
    total: int
    page: int
    page_size: int
    data: List[RecordItem]

class SummaryResp(BaseModel):
    income_total: float
    expense_total: float
    balance: float