from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .routers import memos, todos, pages

app = FastAPI(
    title="메모장 + TODO 리스트",
    description="FastAPI를 사용한 메모장과 TODO 리스트 통합 애플리케이션",
    version="1.0.0"
)

# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="static"), name="static")

# 라우터 등록
app.include_router(pages.router)
app.include_router(memos.router)
app.include_router(todos.router)

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy", "message": "메모장 + TODO 리스트 서비스가 정상 작동 중입니다."}