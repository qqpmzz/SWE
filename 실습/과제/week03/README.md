# 메모장 + TODO 리스트 웹 애플리케이션

## 프로젝트 개요
FastAPI를 기반으로 한 통합 메모장 및 TODO 리스트 웹 애플리케이션입니다. 사용자가 메모를 작성하고 할 일을 관리할 수 있는 직관적인 웹 인터페이스를 제공합니다.

## 주요 기능

### 메모 관리
- **메모 작성**: 제목, 내용, 태그를 포함한 메모 생성
- **메모 편집**: 기존 메모의 수정 및 업데이트  
- **메모 삭제**: 불필요한 메모 제거
- **메모 검색**: 제목, 내용, 태그 기반 실시간 검색
- **태그 시스템**: 메모 분류 및 관리를 위한 태그 기능

### TODO 리스트 관리
- **할 일 추가**: 제목, 설명, 우선순위, 마감일이 포함된 TODO 항목 생성
- **상태 관리**: 할 일 완료/미완료 상태 토글
- **우선순위**: 높음, 보통, 낮음의 3단계 우선순위 설정
- **필터링**: 완료 상태별, 우선순위별 필터링 기능
- **마감일 관리**: 할 일별 마감일 설정 및 관리

### 통합 대시보드
- **최근 메모**: 최신 메모 5개 미리보기
- **미완료 할 일**: 완료되지 않은 TODO 항목들 표시
- **빠른 작업**: 대시보드에서 바로 메모와 할 일 추가 가능

## 기술 스택

### 백엔드
- **FastAPI**: 고성능 웹 프레임워크
- **Pydantic**: 데이터 검증 및 설정 관리
- **Uvicorn**: ASGI 웹 서버

### 프론트엔드
- **HTML5**: 시맨틱 마크업
- **CSS3**: 반응형 디자인 및 모던 스타일링
- **JavaScript**: 동적 UI 및 비동기 통신
- **Jinja2**: 서버사이드 템플릿 엔진

### 데이터 저장
- **JSON 파일**: 간단한 파일 기반 데이터 저장소

## 프로젝트 구조

```
week03/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 애플리케이션 진입점
│   ├── models/
│   │   ├── __init__.py
│   │   ├── memo.py            # 메모 데이터 모델
│   │   └── todo.py            # TODO 데이터 모델
│   ├── services/
│   │   ├── __init__.py
│   │   ├── memo_service.py    # 메모 비즈니스 로직
│   │   └── todo_service.py    # TODO 비즈니스 로직
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── memos.py          # 메모 API 엔드포인트
│   │   ├── todos.py          # TODO API 엔드포인트
│   │   └── pages.py          # 페이지 라우터
│   └── static/
│       ├── css/
│       │   └── style.css     # 메인 스타일시트
│       └── js/
│           └── app.js        # 메인 JavaScript
├── templates/
│   ├── base.html             # 기본 템플릿
│   ├── index.html            # 대시보드 페이지
│   ├── memos.html            # 메모 관리 페이지
│   └── todos.html            # TODO 관리 페이지
├── data/
│   ├── memos.json           # 메모 데이터 저장
│   └── todos.json           # TODO 데이터 저장
├── requirements.txt          # Python 의존성
└── README.md                # 프로젝트 문서
```

## 설치 및 실행

### 1. 필수 조건
- Python 3.8 이상
- pip 패키지 관리자

### 2. 가상환경 준비
이 프로젝트는 SWE 폴더의 가상환경을 사용합니다:

```bash
# SWE 폴더로 이동
cd "c:\Users\qqpmzz\Desktop\GitHub\SWE"

# 가상환경이 없다면 생성
python -m venv venv

# 가상환경에 의존성 설치
venv\Scripts\python.exe -m pip install -r "실습\과제\week03\requirements.txt"
```

### 3. 애플리케이션 실행
week03 프로젝트 디렉토리에서 다음 명령어를 실행하세요:

```bash
# week03 폴더로 이동
cd "c:\Users\qqpmzz\Desktop\GitHub\SWE\실습\과제\week03"

# SWE 폴더의 가상환경 Python으로 서버 실행
..\..\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 웹 브라우저에서 접속
```
http://localhost:8000
```

## 화면 구성

### 대시보드 (/)
- 최근 메모 5개와 미완료 할 일 표시
- 빠른 메모/할 일 추가 모달
- 직관적인 네비게이션 메뉴

### 메모 관리 (/memos)
- 메모 카드 형태의 목록 표시
- 실시간 검색 기능
- 태그별 필터링
- 메모 추가/편집/삭제 모달

### TODO 관리 (/todos)
- 체크박스가 있는 할 일 목록
- 상태별 필터링 (전체/미완료/완료)
- 우선순위별 필터링
- 마감일 표시 및 관리

## API 문서

FastAPI는 자동으로 API 문서를 생성합니다:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 주요 API 엔드포인트

#### 메모 관리
- `GET /api/memos/` - 모든 메모 조회
- `POST /api/memos/` - 새 메모 생성
- `GET /api/memos/{memo_id}` - 특정 메모 조회
- `PUT /api/memos/{memo_id}` - 메모 수정
- `DELETE /api/memos/{memo_id}` - 메모 삭제
- `GET /api/memos/search/?query=검색어` - 메모 검색

#### TODO 관리
- `GET /api/todos/` - 모든 할 일 조회
- `POST /api/todos/` - 새 할 일 생성
- `GET /api/todos/{todo_id}` - 특정 할 일 조회
- `PUT /api/todos/{todo_id}` - 할 일 수정
- `DELETE /api/todos/{todo_id}` - 할 일 삭제
- `PATCH /api/todos/{todo_id}/toggle` - 완료 상태 토글
- `GET /api/todos/filter/?status=pending` - 상태별 필터링
- `GET /api/todos/filter/?priority=high` - 우선순위별 필터링

## 사용법

### 메모 관리
1. **새 메모 작성**: 상단의 "새 메모 추가" 버튼 클릭
2. **메모 검색**: 검색 박스에 키워드 입력하여 실시간 검색
3. **메모 편집**: 메모 카드의 편집 아이콘 클릭
4. **메모 삭제**: 메모 카드의 삭제 아이콘 클릭
5. **태그 활용**: 쉼표로 구분하여 여러 태그 추가 가능

### TODO 관리
1. **할 일 추가**: "새 할 일 추가" 버튼으로 TODO 생성
2. **완료 처리**: 체크박스 클릭으로 완료/미완료 상태 변경
3. **필터링**: 상단의 필터 버튼으로 상태별 보기
4. **우선순위 설정**: 높음/보통/낮음 3단계 우선순위 설정
5. **마감일 관리**: 날짜 선택기로 마감일 설정

### 키보드 단축키
- `Ctrl + N`: 새 메모/할 일 추가
- `Ctrl + F`: 검색창 포커스
- `ESC`: 모달 창 닫기

## 특징

### 반응형 디자인
- 모바일, 태블릿, 데스크톱에서 최적화된 UI
- CSS Grid와 Flexbox를 활용한 유연한 레이아웃

### 사용자 경험
- 직관적인 아이콘과 색상 구성
- 부드러운 애니메이션과 트랜지션
- 실시간 검색 및 필터링

### 데이터 관리
- JSON 파일 기반의 간단한 데이터 저장
- 자동 백업 및 데이터 무결성 보장
- RESTful API 설계 원칙 준수

## 개발 과정

이 프로젝트는 다음 단계를 거쳐 개발되었습니다:

1. **요구사항 분석**: 메모와 TODO 기능의 통합 설계
2. **아키텍처 설계**: MVC 패턴 기반의 구조 설계
3. **백엔드 개발**: FastAPI와 Pydantic을 활용한 API 구현
4. **프론트엔드 개발**: 반응형 웹 인터페이스 구현
5. **테스트 및 최적화**: 사용자 경험 개선 및 성능 최적화

## 개발자 정보

이 프로젝트는 소프트웨어공학 수업의 실습 과제로 개발되었습니다.

## 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.