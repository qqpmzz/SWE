from fastapi import APIRouter, HTTPException
from typing import List
from ..models.memo import Memo, MemoCreate, MemoUpdate
from ..services.memo_service import MemoService

router = APIRouter(prefix="/api/memos", tags=["memos"])
memo_service = MemoService()


@router.get("/", response_model=List[Memo])
async def get_all_memos():
    """모든 메모 조회"""
    return memo_service.get_all_memos()


@router.get("/{memo_id}", response_model=Memo)
async def get_memo(memo_id: str):
    """특정 메모 조회"""
    memo = memo_service.get_memo_by_id(memo_id)
    if not memo:
        raise HTTPException(status_code=404, detail="Memo not found")
    return memo


@router.post("/", response_model=Memo)
async def create_memo(memo: MemoCreate):
    """새 메모 생성"""
    return memo_service.create_memo(memo)


@router.put("/{memo_id}", response_model=Memo)
async def update_memo(memo_id: str, memo_update: MemoUpdate):
    """메모 수정"""
    updated_memo = memo_service.update_memo(memo_id, memo_update)
    if not updated_memo:
        raise HTTPException(status_code=404, detail="Memo not found")
    return updated_memo


@router.delete("/{memo_id}")
async def delete_memo(memo_id: str):
    """메모 삭제"""
    success = memo_service.delete_memo(memo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Memo not found")
    return {"message": "Memo deleted successfully"}


@router.get("/search/", response_model=List[Memo])
async def search_memos(q: str):
    """메모 검색"""
    if not q:
        raise HTTPException(status_code=400, detail="Search query is required")
    return memo_service.search_memos(q)