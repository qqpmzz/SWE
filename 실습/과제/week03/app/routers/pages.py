from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from ..services.memo_service import MemoService
from ..services.todo_service import TodoService

router = APIRouter()
templates = Jinja2Templates(directory="templates")
memo_service = MemoService()
todo_service = TodoService()


@router.get("/")
async def dashboard(request: Request):
    """메인 대시보드 페이지"""
    # 모든 메모와 모든 TODO 가져오기
    all_memos = memo_service.get_all_memos()
    all_todos = todo_service.get_all_todos()
    
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "recent_memos": all_memos, 
            "pending_todos": all_todos
        }
    )