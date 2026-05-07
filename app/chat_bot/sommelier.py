from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI
import os
import re

router = APIRouter()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 요청 스키마
class SommelierRequest(BaseModel):
    message: str

# 응답 스키마
class SommelierResponse(BaseModel):
    reply: str

# 소믈리에 시스템 프롬프트
SYSTEM_PROMPT = """
당신은 세계 최고의 소믈리에입니다.
와인에 대한 모든 질문에 전문적이고 친절하게 답변해주세요.
와인 추천, 음식 페어링, 와인 특징 설명 등을 도와줍니다.
답변은 한국어로 해주세요.
마크다운 문법(**굵게**, # 제목 등)은 절대 사용하지 마세요.
일반 텍스트로만 답변해주세요.
"""

@router.post("/sommelier", response_model=SommelierResponse)
def sommelier(request: SommelierRequest):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": request.message}
        ]
    )
    reply = response.choices[0].message.content
    
    # ** ** 제거 (굵게 표시 마크다운 제거)
    reply = re.sub(r'\*\*(.*?)\*\*', r'\1', reply)
    
    # \n을 실제 줄바꿈으로 변환
    reply = reply.replace('\\n', '\n')
    
    return {"reply": reply}   