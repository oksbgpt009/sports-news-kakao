"""PC에서 실행: 카카오 refresh token 발급 → GitHub Secret 자동 등록
(값은 붙여넣지 않고 클립보드에서 읽음. 화면에 표시되지 않음.
 gh 로그인이 안 돼 있으면 토큰을 출력하니 직접 등록)"""
import subprocess
import tkinter

import requests

REDIRECT_URI = "https://localhost"


def ask(name, optional=False):
    # 터미널마다 붙여넣기 방식이 달라 실패하는 일이 있어, 복사만 하면 클립보드에서 직접 읽음
    hint = " (사용 안 하면 아무것도 복사하지 말고 n 입력 후 엔터)" if optional else ""
    if input(f"{name} 을(를) 복사한 뒤 엔터{hint}: ").strip().lower() == "n" and optional:
        return ""
    root = tkinter.Tk()
    root.withdraw()
    value = root.clipboard_get().strip()
    root.destroy()
    if not value or any(c.isspace() for c in value):
        raise SystemExit(f"클립보드에 {name} 값이 없습니다. 다시 복사한 뒤 처음부터 실행하세요.")
    print(f"  → {len(value)}자 읽음")
    return value


rest_api_key = ask("카카오 REST API 키")
client_secret = ask("Client Secret", optional=True)

print("\n아래 주소를 브라우저에서 열고 로그인/동의하세요:")
print(
    "https://kauth.kakao.com/oauth/authorize"
    f"?client_id={rest_api_key}&redirect_uri={REDIRECT_URI}"
    "&response_type=code&scope=talk_message"
)
print("\n이동된 주소창의 'code=' 뒤 값을 복사하세요. (페이지가 안 열려도 정상)")
code = ask("code")

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
token = resp.json()["refresh_token"]
# 손으로 복사하다 틀리는 일이 없도록 gh 로 바로 등록 (이 폴더의 GitHub 저장소 기준)
try:
    subprocess.run(["gh", "secret", "set", "KAKAO_REFRESH_TOKEN", "--body", token], check=True)
    print("\nKAKAO_REFRESH_TOKEN 을 GitHub Secret 에 등록했습니다.")
except (OSError, subprocess.CalledProcessError):
    print("\n자동 등록 실패. 아래 값을 GitHub Secret KAKAO_REFRESH_TOKEN 에 직접 등록하세요:")
    print(token)
