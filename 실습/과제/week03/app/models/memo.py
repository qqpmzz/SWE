from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MemoBase(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = []


class MemoCreate(MemoBase):
    pass


class MemoUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None


class Memo(MemoBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True