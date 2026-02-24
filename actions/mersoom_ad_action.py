# -*- coding: utf-8 -*-
import requests
import re
import hashlib
import time
from actions.base import BaseAction

class MersoomAdAction(BaseAction):
    BASE_URL = "https://www.mersoom.com/api"

    def match(self, ai_text):
        # AI가 "AD: 문구 | 포인트" 형식으로 답변하면 실행
        return any(line.strip().startswith("AD:") for line in ai_text.split('\n'))

    def solve_pow(self, seed):
        nonce = 0
        seed_str = str(seed)
        while True:
            target = f"{seed_str}{nonce}"
            hash_result = hashlib.sha256(target.encode('utf-8')).hexdigest()
            if hash_result.startswith("0000"):
                return str(nonce)
            nonce += 1

    def execute(self, ai_text):
        # 형식: AD: 광고문구 | 100
        pattern = r"AD:\s*(.*)\|\s*(\d+)"
        matches = re.findall(pattern, ai_text)
        results = []

        # 실제 환경에서는 보안을 위해 환경변수나 별도 설정 파일에서 가져오는 것이 좋습니다.
        # 여기서는 문서 예시인 mybot123을 기준으로 작성합니다.
        MY_AUTH_ID = "mybot123"
        MY_PASSWORD = "mysecurepassword"

        for content, points in matches:
            try:
                # 1. PoW 챌린지 획득
                challenge_res = requests.post(f"{self.BASE_URL}/challenge", timeout=10)
                challenge_data = challenge_res.json()
                seed = challenge_data.get("challenge", {}).get("seed")
                token = challenge_data.get("token")

                if not seed or not token:
                    results.append("[red]✘ 광고 등록을 위한 챌린지 획득 실패[/red]")
                    continue

                results.append(f"[yellow]⏳ 광고 PoW 계산 중... (소모 포인트: {points})[/yellow]")
                nonce = self.solve_pow(seed)

                # 2. 광고 등록 요청 (4.7 API 규격 준수)
                headers = {
                    "X-Mersoom-Token": token,
                    "X-Mersoom-Proof": nonce,
                    "X-Mersoom-Auth-Id": MY_AUTH_ID,
                    "X-Mersoom-Password": MY_PASSWORD,
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "content": content.strip(),
                    "points": int(points)
                }

                res = requests.post(f"{self.BASE_URL}/ads", json=payload, headers=headers, timeout=10)

                if res.status_code in [200, 201]:
                    ad_data = res.json()
                    results.append(f"[bold magenta]📢 광고 등록 성공![/bold magenta]")
                    results.append(f"[dim]내용: {content.strip()} / 노출 예정: {ad_data.get('impressions')}회[/dim]")
                else:
                    results.append(f"[red]✘ 광고 등록 거부 ({res.status_code}): {res.text}[/red]")

            except Exception as e:
                results.append(f"[red]✘ 광고 액션 오류: {str(e)}[/red]")
        
        return results