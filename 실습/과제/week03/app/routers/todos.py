from fastapi import APIRouter, HTTPException
from typing import List
from ..models.todo import Todo, TodoCreate, TodoUpdate
from ..services.todo_service import TodoService

router = APIRouter(prefix="/api/todos", tags=["todos"])
todo_service = TodoService()


@router.get("/", response_model=List[Todo])
async def get_all_todos():
    """모든 TODO 조회"""
    return todo_service.get_all_todos()


@router.get("/{todo_id}", response_model=Todo)
async def get_todo(todo_id: str):
    """특정 TODO 조회"""
    todo = todo_service.get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.post("/", response_model=Todo)
async def create_todo(todo: TodoCreate):
    """새 TODO 생성"""
    return todo_service.create_todo(todo)


@router.put("/{todo_id}", response_model=Todo)
async def update_todo(todo_id: str, todo_update: TodoUpdate):
    """TODO 수정"""
    updated_todo = todo_service.update_todo(todo_id, todo_update)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo


@router.delete("/{todo_id}")
async def delete_todo(todo_id: str):
    """TODO 삭제"""
    success = todo_service.delete_todo(todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}


@router.patch("/{todo_id}/toggle", response_model=Todo)
async def toggle_todo_completion(todo_id: str):
    """TODO 완료 상태 토글"""
    updated_todo = todo_service.toggle_todo_completion(todo_id)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo


@router.get("/filter/", response_model=List[Todo])
async def filter_todos(status: str = None):
    """TODO 필터링"""
    if status is not None:
        if status.lower() == "completed":
            return todo_service.get_todos_by_status(True)
        elif status.lower() == "pending":
            return todo_service.get_todos_by_status(False)
        else:
            raise HTTPException(status_code=400, detail="Invalid status. Use 'completed' or 'pending'")
    
    # 파라미터가 없으면 모든 TODO 반환
    return todo_service.get_all_todos()