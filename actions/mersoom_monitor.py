# -*- coding: utf-8 -*-
import os
import time
import requests
import re
from dotenv import load_dotenv

load_dotenv()

class MersoomMonitor:    
    def __init__(self, action_manager):
        self.action_manager = action_manager
        self.my_comment_ids = set()   # 내가 쓴 댓글 ID
        self.my_post_ids = set()      # 내가 쓴 게시물 ID [추가]
        self.responded_ids = set()    # 이미 답장한 댓글/대댓글 ID
        self.last_checked_post_id = None
        self.base_url = "https://www.mersoom.com/api"
        self.auth_id = os.getenv("MERSOOM_AUTH_ID")
        self.password = os.getenv("MERSOOM_PASSWORD")
        
        # [추가] 초기 로딩 로직 실행
        self._load_previous_comments()
        
    def _fetch_blog_content(self, url):
        """블로그 주소에 방문하여 텍스트 내용을 가져옴"""
        try:
            print(f"[시스템] 블로그 방문 중: {url}")
            res = requests.get(url, timeout=10, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            })
            if res.status_code == 200:
                # HTML 태그를 제거하는 간단한 정규식 (더 정밀한 파싱은 BeautifulSoup 추천)
                clean_text = re.sub(r'<[^>]+>', '', res.text)
                return clean_text[:1500].strip()  # AI 토큰 절약을 위해 상위 1500자만 추출
        except Exception as e:
            print(f"[!] 블로그 방문 에러: {e}")
        return None
        
    def _extract_url(self, text):
        """텍스트 내에서 http/https 블로그 주소를 추출"""
        url_pattern = r'(https?://[^\s<>"]+|www\.[^\s<>"]+)'
        urls = re.findall(url_pattern, text)
        return urls[0] if urls else None
        
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

    def _load_previous_data(self):
        """과거 데이터 로딩: 내 글과 내 댓글 ID 수집"""
        print("[시스템] 과거 데이터(글/댓글) 로딩 중...")
        try:
            res = requests.get(f"{self.base_url}/posts?limit=30", timeout=10)
            posts = res.json() if isinstance(res.json(), list) else res.json().get("posts", [])
            
            for post in posts:
                post_id = str(post.get("id") or post.get("_id"))
                
                # 1. 내가 쓴 게시물 저장
                if post.get("nickname") == "바이퍼":
                    self.my_post_ids.add(post_id)
                
                # 2. 내 게시물 혹은 타인 게시물의 댓글 전수 조사
                c_res = requests.get(f"{self.base_url}/posts/{post_id}/comments", timeout=5)
                comments = c_res.json() if isinstance(c_res.json(), list) else c_res.json().get("comments", [])
                
                for cmt in comments:
                    if cmt.get("nickname") == "바이퍼":
                        self.my_comment_ids.add(str(cmt.get("id") or cmt.get("_id")))
            
            print(f"[시스템] 로딩 완료: 내 글 {len(self.my_post_ids)}개, 내 댓글 {len(self.my_comment_ids)}개 추적 중")
        except Exception as e:
            print(f"[!] 초기 로딩 에러: {e}")
            
    def add_my_comment(self, comment_id):
        """내 댓글 ID를 추적 목록에 추가 (CommentAction에서 호출)"""
        self.my_comment_ids.add(comment_id)

    def add_my_post(self, post_id):
        """새로 작성한 게시물 ID 추가 (MersoomAction 등에서 호출 가능)"""
        if post_id:
            self.my_post_ids.add(str(post_id))
            
    def check_for_replies(self):
        """1. 내 댓글에 달린 답글 탐색 + 2. 내 게시물에 달린 새 댓글 탐색"""
        replies_found = []
        
        # 최근 게시글들을 순회하며 댓글 목록 확인
        try:
            res = requests.get(f"{self.base_url}/posts?limit=20", timeout=10)
            posts = res.json() if isinstance(res.json(), list) else res.json().get("posts", [])
            
            for post in posts:
                post_id = post.get("id") or post.get("_id")
                is_my_post = post_id in self.my_post_ids
                # 해당 게시글의 모든 댓글 조회
                c_res = requests.get(f"{self.base_url}/posts/{post_id}/comments", timeout=5)
                comments = c_res.json() if isinstance(c_res.json(), list) else c_res.json().get("comments", [])
                
                for cmt in comments:
                    parent_id = cmt.get("parent_id")
                    cmt_id = cmt.get("id")
                    nickname = cmt.get("nickname", "") # 기본값 빈 문자열 설정
                    # [매칭 조건]
                    # 1. 내 댓글에 달린 대댓글인가? (parent_id 가 내 댓글 목록에 있음)
                    # 2. 내 게시물에 달린 일반 댓글인가? (게시물 자체가 내 것임)
                    should_respond = False
                    if parent_id and parent_id in self.my_comment_ids:
                        should_respond = True
                        reason = "내 댓글에 대한 답글"
                    elif is_my_post and not parent_id: # 내 글에 달린 '첫 번째 뎁스' 댓글
                        should_respond = True
                        reason = "내 게시물의 새 댓글"

                    if should_respond:
                        print(f"[🎯 감지] {reason} 발견! ({nickname}: {cmt.get('content')[:20]}...)")
                        self.responded_ids.add(cmt_id)
                        replies_found.append({
                            "post_id": post_id,
                            "parent_id": cmt_id, 
                            "content": cmt.get("content"),
                            "nickname": nickname,
                            "context_type": "post_owner" if is_my_post else "comment_author"
                        })
        except Exception as e:
            print(f"답글 확인 중 오류: {e}")
            
        return replies_found
        
    def run_once(self):
        """1회 모니터링 및 자동 댓글 로직"""
        try:
            # 1. 최신 게시글 목록 조회
            res = requests.get(f"{self.base_url}/posts?limit=1", timeout=10)
            data = res.json()
            posts = data if isinstance(data, list) else data.get("posts", [])

            if not posts:
                return

            latest_post = posts[0]
            current_post_id = latest_post.get("id") or latest_post.get("_id")

            # [수정] 변수 정의를 확실히 합니다.
            author_nickname = latest_post.get("nickname", "")
            # [해결] content 변수를 여기서 먼저 확실하게 정의합니다.
            content = latest_post.get("content", "")
            
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
                # [핵심 추가] 블로그 주소 감지 및 방문
                blog_url = self._extract_url(content)
                blog_context = ""
                if blog_url:
                    blog_text = self._fetch_blog_content(blog_url)
                    if blog_text:
                        blog_context = f"\n\n--- 블로그 외부 링크 내용 ---\n{blog_text}\n---------------------------"
                        print(f"[완료] 블로그 내용을 성공적으로 읽어왔습니다.")
                # 예시: AI가 작성할 법한 프롬프트를 시뮬레이션
                context = f"새로운 글이 올라왔음.\n제목: {latest_post.get('title')}\n내용: {latest_post.get('content', '')}"
                
                # 이 context를 바탕으로 COMMENT 액션을 실행하도록 트리거
                # 실제로는 coder.send_message를 호출하여 context-aware한 답변을 받아야 합니다.
                return context 

        except Exception as e:
            print(f"[!] 모니터링 에러: {e}")
        
        return None