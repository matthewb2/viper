# -*- coding: utf-8 -*-
import requests
import re
import hashlib
from urllib.parse import quote
import time
from pathlib import Path  # 경로 처리를 위해 추가
import os
from dotenv import load_dotenv
from actions.base import BaseAction

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class MersoomAction(BaseAction):
    BASE_URL = "https://www.mersoom.com/api"

    def match(self, ai_text):
        return "MERSOOM:" in ai_text

    def solve_pow(self, seed):
        nonce = 0
        seed_str = str(seed)
        start_time = time.time()
        while True:
            target = f"{seed_str}{nonce}"
            hash_result = hashlib.sha256(target.encode('utf-8')).hexdigest()
            if hash_result.startswith("0000"):
                duration = time.time() - start_time
                return str(nonce), duration
            nonce += 1

    def execute(self, ai_text, **kwargs): # **kwargs 추가!
        pattern = r"MERSOOM:\s*(.*?)\s*\|\s*(.*)"
        matches = re.findall(pattern, ai_text, re.DOTALL)
        results = []
        auth_id = os.getenv("MERSOOM_ID")
        password = os.getenv("MERSOOM_PASSWORD")

        for title, content in matches:
# actions/mersoom_action.py 의 execute 메소드 내부 수정

            try:
                # 1. 챌린지 요청
                challenge_res = requests.post(f"{self.BASE_URL}/challenge", timeout=10)
                challenge_data = challenge_res.json()
                
                # [로그 분석 결과 반영] 
                # challenge 객체 내부에서 seed를 찾고, 최상위에서 token을 찾습니다.
                challenge_obj = challenge_data.get("challenge", {})
                seed = challenge_obj.get("seed")
                token = challenge_data.get("token")

                if not seed or not token:
                    results.append(f"[red]✘ 서버 데이터 구조 불일치: seed={bool(seed)}, token={bool(token)}[/red]")
                    continue

                # 2. 작업 증명(PoW) 수행
                results.append(f"[yellow]⏳ 머슴닷컴 PoW 계산 시작... (Seed: {seed})[/yellow]")
                nonce, duration = self.solve_pow(seed)
                results.append(f"[cyan]✨ PoW 해결! (Nonce: {nonce}, {duration:.2f}s)[/cyan]")

                # 3. 글쓰기 전송
                # X-Mersoom-Token 헤더에 token 값을, X-Mersoom-Proof에 nonce를 넣습니다.
                headers = {
                    "X-Mersoom-Token": token,
                    "X-Mersoom-Proof": nonce,
                    "X-Mersoom-Auth-Id": auth_id, 
                    "X-Mersoom-Password": password, 
                    "User-Agent": "Mersoom-Agent-v1.0.2",
                    "Content-Type": "application/json"
                }
                # 'author' 필드가 에이전트의 이름을 결정하는 핵심 키일 수 있습니다.
                payload = {
                    "title": title.strip(),
                    "content": content.strip(),
                    "nickname": "바이퍼"
                }
                
                post_res = requests.post(f"{self.BASE_URL}/posts", json=payload, headers=headers, timeout=10)
                
                if post_res.status_code in [200, 201]:
                    results.append(f"[bold green]🚀 머슴닷컴 등록 성공! 드디어 연결되었습니다.[/bold green]")
                else:
                    results.append(f"[red]✘ 등록 거부 ({post_res.status_code}): {post_res.text}[/red]")

            except Exception as e:
                results.append(f"[red]✘ 머슴닷컴 액션 실행 중 오류: {str(e)}[/red]")                
        return results