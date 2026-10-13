"""최초 1회만 PC에서 실행: 카카오 refresh token 발급
(입력값은 화면에 표시되지 않음. 출력된 토큰은 GitHub Secret에 등록 후 창을 닫으세요)"""
from getpass import getpass

import requests

REDIRECT_URI = "https://localhost"

rest_api_key = getpass("카카오 REST API 키: ").strip()
client_secret = getpass("Client Secret (사용 안 하면 엔터): ").strip()

print("\n아래 주소를 브라우저에서 열고 로그인/동의하세요:")
print(
    "https://kauth.kakao.com/oauth/authorize"
    f"?client_id={rest_api_key}&redirect_uri={REDIRECT_URI}"
    "&response_type=code&scope=talk_message"
)
print("\n이동된 주소창의 'code=' 뒤 값을 복사하세요. (페이지가 안 열려도 정상)")
code = getpass("code: ").strip()

data = {
    "grant_type": "authorization_code",
    "client_id": rest_api_key,
    "redirect_uri": REDIRECT_URI,
    "code": code,
}
if client_secret:
    data["client_secret"] = client_secret
resp = requests.post("https://kauth.kakao.com/oauth/token", data=data, timeout=10)
if not resp.ok:
    raise SystemExit(f"카카오 토큰 발급 실패: {resp.status_code} {resp.text}")
print("\nKAKAO_REFRESH_TOKEN (GitHub Secret에 등록):")
print(resp.json()["refresh_token"])
