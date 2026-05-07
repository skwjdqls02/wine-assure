from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.db.data_base import Base, engine
from app.db import model
from app.login.router import router as login_router, limiter
from app.chat_bot.sommelier import router as chat_router
# 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Login Server",
    description="회원가입 / 로그인 API + 챗봇",
    version="1.0.0"
)

# Rate Limiter 설정
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# 라우터 등록
app.include_router(login_router)
app.include_router(chat_router)