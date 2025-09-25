import json
import os
import uuid
from datetime import datetime
from typing import List, Optional
from ..models.memo import Memo, MemoCreate, MemoUpdate


class MemoService:
    def __init__(self, data_file: str = "data/memos.json"):
        self.data_file = data_file
        self.ensure_data_file_exists()

    def ensure_data_file_exists(self):
        """데이터 파일이 존재하지 않으면 생성"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def load_memos(self) -> List[dict]:
        """JSON 파일에서 메모 데이터 로드"""
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_memos(self, memos: List[dict]):
        """메모 데이터를 JSON 파일에 저장"""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(memos, f, ensure_ascii=False, indent=2, default=str)

    def get_all_memos(self) -> List[Memo]:
        """모든 메모 조회"""
        memos_data = self.load_memos()
        return [Memo(**memo) for memo in memos_data]

    def get_memo_by_id(self, memo_id: str) -> Optional[Memo]:
        """ID로 특정 메모 조회"""
        memos_data = self.load_memos()
        for memo in memos_data:
            if memo["id"] == memo_id:
                return Memo(**memo)
        return None

    def create_memo(self, memo_data: MemoCreate) -> Memo:
        """새 메모 생성"""
        memos = self.load_memos()
        
        new_memo = {
            "id": str(uuid.uuid4()),
            "title": memo_data.title,
            "content": memo_data.content,
            "tags": memo_data.tags or [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        memos.append(new_memo)
        self.save_memos(memos)
        
        return Memo(**new_memo)

    def update_memo(self, memo_id: str, memo_update: MemoUpdate) -> Optional[Memo]:
        """메모 수정"""
        memos = self.load_memos()
        
        for i, memo in enumerate(memos):
            if memo["id"] == memo_id:
                # 업데이트할 필드들만 수정
                if memo_update.title is not None:
                    memo["title"] = memo_update.title
                if memo_update.content is not None:
                    memo["content"] = memo_update.content
                if memo_update.tags is not None:
                    memo["tags"] = memo_update.tags
                
                memo["updated_at"] = datetime.now().isoformat()
                memos[i] = memo
                self.save_memos(memos)
                
                return Memo(**memo)
        
        return None

    def delete_memo(self, memo_id: str) -> bool:
        """메모 삭제"""
        memos = self.load_memos()
        original_length = len(memos)
        
        memos = [memo for memo in memos if memo["id"] != memo_id]
        
        if len(memos) < original_length:
            self.save_memos(memos)
            return True
        
        return False

    def search_memos(self, query: str) -> List[Memo]:
        """메모 검색 (제목과 내용에서 검색)"""
        memos_data = self.load_memos()
        query = query.lower()
        
        matching_memos = []
        for memo in memos_data:
            if (query in memo["title"].lower() or 
                query in memo["content"].lower() or
                any(query in tag.lower() for tag in memo.get("tags", []))):
                matching_memos.append(Memo(**memo))
        
        return matching_memos