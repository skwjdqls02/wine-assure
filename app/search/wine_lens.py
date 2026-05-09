from fastapi import APIRouter, UploadFile, File, HTTPException
from serpapi import GoogleSearch
import os
import base64
import httpx

router = APIRouter()

@router.post("/wine/search")
async def wine_search(file: UploadFile = File(...)):

    # 1. 이미지 base64 변환
    image_data = await file.read()
    base64_image = base64.b64encode(image_data).decode("utf-8")

    # 2. imgBB에 업로드
    async with httpx.AsyncClient() as client:
        imgbb_response = await client.post(
            "https://api.imgbb.com/1/upload",
            data={
                "key": os.getenv("IMGBB_API_KEY"),
                "image": base64_image,
                "expiration": 60  # 60초 후 자동 삭제!
            }
        )

    imgbb_data = imgbb_response.json()
    if not imgbb_data.get("success"):
        raise HTTPException(status_code=500, detail="이미지 업로드 실패")

    image_url = imgbb_data["data"]["url"]

    # 3. SerpApi Google Lens 호출
    search = GoogleSearch({
        "engine": "google_lens",
        "url": image_url,
        "api_key": os.getenv("SERPAPI_KEY")
    })
    result = search.get_dict()

    visual_matches = result.get("visual_matches", [])
    wines = []
    for match in visual_matches[:5]:
        wines.append({
            "title": match.get("title", ""),
            "link": match.get("link", ""),
            "thumbnail": match.get("thumbnail", "")
        })

    return {"results": wines}