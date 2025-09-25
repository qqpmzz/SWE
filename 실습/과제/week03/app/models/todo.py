from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    due_time: Optional[str] = None


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    due_time: Optional[str] = None
    completed: Optional[bool] = None


class Todo(TodoBase):
    id: str
    completed: bool = False
    created_at: datetime
    updated_at: datetime
    
    @property
    def is_overdue(self) -> bool:
        if not self.due_date:
            return False
        
        now = datetime.now()
        due_datetime = datetime.combine(self.due_date, datetime.min.time())
        
        if self.due_time:
            try:
                time_parts = self.due_time.split(':')
                due_datetime = due_datetime.replace(
                    hour=int(time_parts[0]), 
                    minute=int(time_parts[1]) if len(time_parts) > 1 else 0
                )
            except (ValueError, IndexError):
                pass
        
        return now > due_datetime and not self.completed
    
    @property
    def time_remaining(self) -> Optional[str]:
        if not self.due_date or self.completed:
            return None
        
        now = datetime.now()
        due_datetime = datetime.combine(self.due_date, datetime.min.time())
        
        if self.due_time:
            try:
                time_parts = self.due_time.split(':')
                due_datetime = due_datetime.replace(
                    hour=int(time_parts[0]), 
                    minute=int(time_parts[1]) if len(time_parts) > 1 else 0
                )
            except (ValueError, IndexError):
                pass
        
        if now > due_datetime:
            return "만료됨"
        
        diff = due_datetime - now
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        if days > 0:
            return f"{days}일 {hours}시간 남음"
        elif hours > 0:
            return f"{hours}시간 {minutes}분 남음"
        else:
            return f"{minutes}분 남음"

    class Config:
        from_attributes = True