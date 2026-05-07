from pydantic import BaseModel, EmailStr, field_validator #데이터 검증 라이브러리
from datetime import date

class user_create(BaseModel):
    email: EmailStr
    password: str
    phone : str
    real_name: str
    nickname:str
    birth_date: date
    
    @field_validator("password")
    def password_length(cls, v):
        if len(v) > 72:
            raise ValueError("비밀번호가 72자 이하여야합니다.")
        if len(v) < 8:
            raise ValueError("비밀번호는 8자 이상이여야합니다.")
        return v
    
class user_login(BaseModel):
    email: EmailStr
    password: str

class user_response(BaseModel):
    email: str
    phone: str
    real_name: str
    nickname: str
    birth_date: date
    
    class config: #user db 값 바로 연결 꼭 매칭되는 이름이랑 같아야함.
        from_attributes = True
        
class token(BaseModel):
    access_token: str
    token_type: str