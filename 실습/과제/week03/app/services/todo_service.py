import json
import os
import uuid
from datetime import datetime
from typing import List, Optional
from ..models.todo import Todo, TodoCreate, TodoUpdate


class TodoService:
    def __init__(self, data_file: str = "data/todos.json"):
        self.data_file = data_file
        self.ensure_data_file_exists()

    def ensure_data_file_exists(self):
        """데이터 파일이 존재하지 않으면 생성"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def load_todos(self) -> List[dict]:
        """JSON 파일에서 TODO 데이터 로드"""
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_todos(self, todos: List[dict]):
        """TODO 데이터를 JSON 파일에 저장"""
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(todos, f, ensure_ascii=False, indent=2, default=str)

    def get_all_todos(self) -> List[Todo]:
        """모든 TODO 조회"""
        todos_data = self.load_todos()
        return [Todo(**todo) for todo in todos_data]

    def get_todo_by_id(self, todo_id: str) -> Optional[Todo]:
        """ID로 특정 TODO 조회"""
        todos_data = self.load_todos()
        for todo in todos_data:
            if todo["id"] == todo_id:
                return Todo(**todo)
        return None

    def create_todo(self, todo_data: TodoCreate) -> Todo:
        """새 TODO 생성"""
        todos = self.load_todos()
        
        new_todo = {
            "id": str(uuid.uuid4()),
            "title": todo_data.title,
            "description": todo_data.description,
            "due_date": todo_data.due_date.isoformat() if todo_data.due_date else None,
            "due_time": todo_data.due_time,
            "completed": False,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        todos.append(new_todo)
        self.save_todos(todos)
        
        return Todo(**new_todo)

    def update_todo(self, todo_id: str, todo_update: TodoUpdate) -> Optional[Todo]:
        """TODO 수정"""
        todos = self.load_todos()
        
        for i, todo in enumerate(todos):
            if todo["id"] == todo_id:
                # 업데이트할 필드들만 수정
                if todo_update.title is not None:
                    todo["title"] = todo_update.title
                if todo_update.description is not None:
                    todo["description"] = todo_update.description
                if todo_update.due_date is not None:
                    todo["due_date"] = todo_update.due_date.isoformat()
                if todo_update.due_time is not None:
                    todo["due_time"] = todo_update.due_time
                if todo_update.completed is not None:
                    todo["completed"] = todo_update.completed
                
                todo["updated_at"] = datetime.now().isoformat()
                todos[i] = todo
                self.save_todos(todos)
                
                return Todo(**todo)
        
        return None

    def delete_todo(self, todo_id: str) -> bool:
        """TODO 삭제"""
        todos = self.load_todos()
        original_length = len(todos)
        
        todos = [todo for todo in todos if todo["id"] != todo_id]
        
        if len(todos) < original_length:
            self.save_todos(todos)
            return True
        
        return False

    def toggle_todo_completion(self, todo_id: str) -> Optional[Todo]:
        """TODO 완료 상태 토글"""
        todos = self.load_todos()
        
        for i, todo in enumerate(todos):
            if todo["id"] == todo_id:
                todo["completed"] = not todo["completed"]
                todo["updated_at"] = datetime.now().isoformat()
                todos[i] = todo
                self.save_todos(todos)
                
                return Todo(**todo)
        
        return None

    def get_todos_by_status(self, completed: bool) -> List[Todo]:
        """완료 상태별 TODO 조회"""
        todos_data = self.load_todos()
        filtered_todos = [todo for todo in todos_data if todo["completed"] == completed]
        return [Todo(**todo) for todo in filtered_todos]