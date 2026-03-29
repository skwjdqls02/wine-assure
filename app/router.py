from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.data_base import get_db
from app.model import User
from app.schemas import user_create, user_login, user_response, token
from app.auth import hash_password, verify_password, create_access_token, decode_token

router  = APIRouter()
limiter = Limiter(key_func=get_remote_address)
oauth2  = OAuth2PasswordBearer(tokenUrl="/login")


# 회원가입
@router.post("/register", status_code=201)
def register(user_in: user_create, db: Session = Depends(get_db)):

    # 이메일 중복 확인
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="이미 사용 중인 이메일입니다.")

    # 닉네임 중복 확인
    if db.query(User).filter(User.nickname == user_in.nickname).first():
        raise HTTPException(status_code=400, detail="이미 사용 중인 닉네임입니다.")

    # 전화번호 중복 확인
    if db.query(User).filter(User.phone == user_in.phone).first():
        raise HTTPException(status_code=400, detail="이미 사용 중인 전화번호입니다.")

    # 유저 생성
    user = User(
        email=user_in.email,
        password=hash_password(user_in.password),  # 비밀번호 해싱
        phone=user_in.phone,
        real_name=user_in.real_name,
        nickname=user_in.nickname,
        birth_date=user_in.birth_date
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message" : "회원 가입에 완료 되었습니다."}


# 로그인 (Rate Limit: 분당 5회)
@router.post("/login", response_model=token)
@limiter.limit("5/minute")
def login(request: Request, user_in: user_login, db: Session = Depends(get_db)):

    # 이메일로 유저 조회
    user = db.query(User).filter(User.email == user_in.email).first()

    # 유저 없거나 비밀번호 틀리면 동일한 오류 반환 (보안상 중요!)
    if not user or not verify_password(user_in.password, user.password):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 틀렸습니다.")

    # 토큰 발급
    return {
        "access_token": create_access_token({"sub": str(user.id)}),
        "token_type": "bearer"
    }


# 내 정보 조회 (토큰 필요)
@router.get("/profile", response_model=user_response)
def get_me(token: str = Depends(oauth2), db: Session = Depends(get_db)):

    # 토큰 검증
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")

    # 유저 조회
    user = db.get(User, int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=404, detail="존재하지 않는 유저입니다.")

    return user