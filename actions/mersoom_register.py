# -*- coding: utf-8 -*-
import requests
import re
import hashlib
import time
from actions.base import BaseAction

class MersoomRegisterAction(BaseAction):
    BASE_URL = "https://www.mersoom.com/api"

    def match(self, ai_text):
        # AI가 "REGISTER: 아이디 | 비밀번호" 형식으로 답변하면 실행
        return any(line.strip().startswith("REGISTER:") for line in ai_text.split('\n'))

    def solve_pow(self, seed):
        nonce = 0
        seed_str = str(seed)
        while True:
            target = f"{seed_str}{nonce}"
            hash_result = hashlib.sha256(target.encode('utf-8')).hexdigest()
            if hash_result.startswith("0000"):
                return str(nonce)
            nonce += 1

    def execute(self, ai_text, **kwargs): # 여기에 **kwargs만 넣어주면 됩니다.
        # 형식: REGISTER: viperbot | viperpass123
        pattern = r"REGISTER:\s*(.*)\|\s*(.*)"
        matches = re.findall(pattern, ai_text)
        results = []

        for auth_id, password in matches:
            auth_id = auth_id.strip()
            password = password.strip()
            
            try:
                # 1. PoW 챌린지 획득
                challenge_res = requests.post(f"{self.BASE_URL}/challenge", timeout=10)
                challenge_data = challenge_res.json()
                seed = challenge_data.get("challenge", {}).get("seed")
                token = challenge_data.get("token")

                if not seed or not token:
                    results.append("[red]✘ 회원가입을 위한 챌린지 획득 실패[/red]")
                    continue

                results.append(f"[yellow]⏳ 회원가입 PoW 계산 중... (ID: {auth_id})[/yellow]")
                nonce = self.solve_pow(seed)

                # 2. 회원가입 요청 (4.2 API 규격 준수)
                headers = {
                    "X-Mersoom-Token": token,
                    "X-Mersoom-Proof": nonce,
                    "Content-Type": "application/json",
                    "User-Agent": "ViperAgent/1.0"
                }
                
                payload = {
                    "auth_id": auth_id,
                    "password": password
                }

                res = requests.post(f"{self.BASE_URL}/auth/register", json=payload, headers=headers, timeout=10)

                if res.status_code in [200, 201]:
                    results.append(f"[bold green]🎉 머슴넷 회원가입 성공![/bold green]")
                    results.append(f"[cyan]아이디: {auth_id}[/cyan]")
                    results.append(f"[dim]이제 이 계정으로 글을 써서 포인트를 모을 수 있습니다.[/dim]")
                    # 주의: 보안을 위해 비밀번호는 로그에 남기지 않거나 별도 관리 권장
                else:
                    results.append(f"[red]✘ 가입 실패 ({res.status_code}): {res.text}[/red]")

            except Exception as e:
                results.append(f"[red]✘ 가입 액션 오류: {str(e)}[/red]")
        
        return results