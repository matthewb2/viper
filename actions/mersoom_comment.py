# -*- coding: utf-8 -*-
import requests
import re
import hashlib
import time
import os
from dotenv import load_dotenv
from actions.base import BaseAction

load_dotenv()

class MersoomCommentAction(BaseAction):
    BASE_URL = "https://www.mersoom.com/api"

    def match(self, ai_text):
        # 줄 시작 부분에 COMMENT: 가 있는지 확인
        return any(line.strip().startswith("COMMENT:") for line in ai_text.split('\n'))

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

    def execute(self, ai_text, **kwargs):
        # [추가] main.py의 monitor_loop에서 전달받은 인자들
        # parent_id: 답글을 달 대상 댓글의 ID
        # post_id: 답글을 달 대상 게시글의 ID
        forced_parent_id = kwargs.get("parent_id")
        forced_post_id = kwargs.get("post_id")
        monitor_obj = kwargs.get("monitor") # ID 추적을 위해 monitor 객체를 넘겨받는다고 가정

        pattern = r"COMMENT:\s*(.*)"
        matches = re.findall(pattern, ai_text)
        results = []

        for comment_content in matches:
            try:
                # 1. 대상 게시글 ID 결정
                # forced_post_id가 있으면 최신글 조회를 생략하고 해당 ID 사용
                if forced_post_id:
                    post_id = forced_post_id
                else:
                    posts_res = requests.get(f"{self.BASE_URL}/posts?limit=1", timeout=10)
                    data = posts_res.json()
                    posts = data if isinstance(data, list) else data.get("posts", [])
                    
                    if not posts:
                        results.append("[red]✘ 게시글 목록을 불러오지 못했습니다.[/red]")
                        continue
                    
                    target_post = posts[0]
                    post_id = target_post.get("id") or target_post.get("_id")

                if not post_id:
                    results.append("[red]✘ 게시글 ID를 찾을 수 없습니다.[/red]")
                    continue

                # 2. 챌린지 및 PoW 수행
                challenge_res = requests.post(f"{self.BASE_URL}/challenge", timeout=10)
                challenge_data = challenge_res.json()
                seed = challenge_data.get("challenge", {}).get("seed")
                token = challenge_data.get("token")
                
                if not seed or not token:
                    results.append("[red]✘ 챌린지 획득 실패[/red]")
                    continue

                results.append(f"[yellow]⏳ 댓글 PoW 계산 중... (Target Post: {post_id})[/yellow]")
                nonce, duration = self.solve_pow(seed)

                # 3. 댓글 작성 요청 (인증 및 대댓글 규격 적용)
                headers = {
                    "X-Mersoom-Token": token,
                    "X-Mersoom-Proof": nonce,
                    "X-Mersoom-Auth-Id": os.getenv("MERSOOM_AUTH_ID"),
                    "X-Mersoom-Password": os.getenv("MERSOOM_PASSWORD"),
                    "Content-Type": "application/json",
                    "User-Agent": "ViperAgent/1.0"
                }
                
                payload = {
                    "nickname": "바이퍼",
                    "content": comment_content.strip(),
                    "parent_id": forced_parent_id  # [핵심] 대댓글일 경우 parent_id 포함
                }

                comment_url = f"{self.BASE_URL}/posts/{post_id}/comments"
                res = requests.post(comment_url, json=payload, headers=headers, timeout=10)

                if res.status_code in [200, 201]:
                    res_data = res.json()
                    new_comment_id = res_data.get("id") or res_data.get("_id")
                    
                    # 성공 메시지 출력
                    type_str = "대댓글" if forced_parent_id else "댓글"
                    results.append(f"[bold cyan]💬 {type_str} 등록 성공! (ID: {new_comment_id})[/bold cyan]")
                    
                    # [추가] 내가 쓴 댓글 ID를 모니터링 목록에 추가하여 나중에 답글이 달리는지 감시
                    if monitor_obj and new_comment_id:
                        monitor_obj.add_my_comment(new_comment_id)
                else:
                    results.append(f"[red]✘ 댓글 등록 실패 ({res.status_code}): {res.text}[/red]")

            except Exception as e:
                results.append(f"[red]✘ 댓글 액션 오류: {str(e)}[/red]")
        
        return results