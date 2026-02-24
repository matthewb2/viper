# -*- coding: utf-8 -*-
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

class MersoomMonitor:
    BASE_URL = "https://mersoom.com/api"
    
    def __init__(self, action_manager):
        self.action_manager = action_manager
        self.last_checked_post_id = None
        self.base_url = "https://www.mersoom.com/api"
        self.my_comment_ids = set() # 내가 쓴 댓글 ID 저장
        self.responded_ids = set()  # 이미 답장한 대댓글 ID 저장
        self.auth_id = os.getenv("MERSOOM_AUTH_ID")
        self.password = os.getenv("MERSOOM_PASSWORD")
        
        # [추가] 초기 로딩 로직 실행
        self._load_previous_comments()
        
    def _load_previous_comments(self):
        """프로그램 시작 시 최근 20개 게시물을 확인하여 내 댓글 ID를 수집함"""
        print("[시스템] 과거 댓글 데이터 로딩 중...")
        try:
            # 최근 게시글 20개 조회
            res = requests.get(f"{self.base_url}/posts?limit=20", timeout=10)
            posts = res.json() if isinstance(res.json(), list) else res.json().get("posts", [])
            
            count = 0
            for post in posts:
                post_id = post.get("id") or post.get("_id")
                c_res = requests.get(f"{self.base_url}/posts/{post_id}/comments", timeout=5)
                comments = c_res.json() if isinstance(c_res.json(), list) else c_res.json().get("comments", [])
                
                for cmt in comments:
                    # 내 닉네임("바이퍼")인 댓글의 ID를 모두 수집
                    if cmt.get("nickname") == "바이퍼":
                        cmt_id = str(cmt.get("id") or cmt.get("_id"))
                        self.my_comment_ids.add(cmt_id)
                        count += 1
            
            print(f"[시스템] 로딩 완료: 과거 댓글 {count}개를 추적 목록에 추가했습니다.")
            
            # 현재 시점의 최신글 ID를 기록하여 중복 알림 방지
            if posts:
                self.last_checked_post_id = str(posts[0].get("id") or posts[0].get("_id"))

        except Exception as e:
            print(f"[!] 초기 로딩 중 오류 발생: {e}")

    def add_my_comment(self, comment_id):
        """내 댓글 ID를 추적 목록에 추가 (CommentAction에서 호출)"""
        self.my_comment_ids.add(comment_id)

    def check_for_replies(self):
        """내 댓글에 달린 새로운 답글이 있는지 확인"""
        replies_found = []
        
        # 최근 게시글들을 순회하며 댓글 목록 확인
        try:
            res = requests.get(f"{self.base_url}/posts?limit=20", timeout=10)
            posts = res.json() if isinstance(res.json(), list) else res.json().get("posts", [])
            
            for post in posts:
                post_id = post.get("id") or post.get("_id")
                # 해당 게시글의 모든 댓글 조회
                c_res = requests.get(f"{self.base_url}/posts/{post_id}/comments", timeout=5)
                comments = c_res.json() if isinstance(c_res.json(), list) else c_res.json().get("comments", [])
                
                for cmt in comments:
                    parent_id = cmt.get("parent_id")
                    cmt_id = cmt.get("id")
                    
                    # 1. 내 댓글에 달린 답글인가? 
                    # 2. 내가 쓴 게 아닌가? (무한 루프 방지)
                    # 3. 이미 답장한 적이 없는가?
                    if parent_id in self.my_comment_ids and \
                       cmt_id not in self.my_comment_ids and \
                       cmt_id not in self.responded_ids:
                        
                        self.responded_ids.add(cmt_id)
                        replies_found.append({
                            "post_id": post_id,
                            "parent_id": cmt_id, # 이제 이 대댓글이 나의 대답의 부모가 됨
                            "content": cmt.get("content"),
                            "nickname": cmt.get("nickname")
                        })
        except Exception as e:
            print(f"답글 확인 중 오류: {e}")
            
        return replies_found
        
    def run_once(self):
        """1회 모니터링 및 자동 댓글 로직"""
        try:
            # 1. 최신 게시글 목록 조회
            res = requests.get(f"{self.BASE_URL}/posts?limit=1", timeout=10)
            data = res.json()
            posts = data if isinstance(data, list) else data.get("posts", [])

            if not posts:
                return

            latest_post = posts[0]
            current_post_id = latest_post.get("id") or latest_post.get("_id")

            # 2. 새로운 글인지 확인
            if self.last_checked_post_id != current_post_id:
                print(f"\n[🔔 알림] 새로운 글 발견: {latest_post.get('title')}")
                self.last_checked_post_id = current_post_id
                
                # [추가] 내가(바이퍼) 쓴 글이라면 무시
                if author_nickname == os.getenv("MERSOOM_USER_NICKNAME"):
                    print(f"[알림] 내가 쓴 글({latest_post.get('title')})이므로 댓글을 달지 않습니다.")
                    return None

                # 3. AI에게 상황을 전달하여 댓글 생성 유도
                # (이 부분은 메인 루프의 AI와 연동되거나, 특정 페르소나를 사용하여 생성합니다)
                # 여기서는 '자동 댓글' 명령어를 action_manager에 직접 주입합니다.
                
                # 예시: AI가 작성할 법한 프롬프트를 시뮬레이션
                context = f"새로운 글이 올라왔음.\n제목: {latest_post.get('title')}\n내용: {latest_post.get('content', '')}"
                
                # 이 context를 바탕으로 COMMENT 액션을 실행하도록 트리거
                # 실제로는 coder.send_message를 호출하여 context-aware한 답변을 받아야 합니다.
                return context 

        except Exception as e:
            print(f"[!] 모니터링 에러: {e}")
        
        return None