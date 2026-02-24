# -*- coding: utf-8 -*-
import requests
import os
from actions.base import BaseAction

class MersoomReadAction(BaseAction):
    BASE_URL = "https://www.mersoom.com/api"
    # 바이퍼가 읽은 내용을 저장할 임시 파일 경로
    CONTEXT_FILE = "latest_post_context.txt"

    def match(self, ai_text):
        return "READ_POST" in ai_text

    def execute(self, ai_text, **kwargs): # 여기에 **kwargs만 넣어주면 됩니다.
        results = []
        try:
            # 1. 최신 게시글 목록 조회
            res = requests.get(f"{self.BASE_URL}/posts", timeout=10)
            data = res.json()
            posts = data if isinstance(data, list) else data.get("posts", [])

            if not posts:
                return ["[red]✘ 읽어올 게시글이 없습니다.[/red]"]

            # 2. 가장 최신 글 분석
            target = posts[0]
            title = target.get("title", "제목 없음")
            content = target.get("content", "내용 없음")
            author = target.get("author") or target.get("nickname") or "알 수 없음"
            post_id = target.get("id") or target.get("_id")

            # 3. 바이퍼가 인지할 수 있도록 파일에 저장 (컨텍스트 주입용)
            context_msg = f"ID: {post_id}\n작성자: {author}\n제목: {title}\n내용: {content}"
            with open(self.CONTEXT_FILE, "w", encoding="utf-8") as f:
                f.write(context_msg)

            results.append(f"[bold green]📖 최신 글 읽기 완료![/bold green]")
            results.append(f"[cyan]제목: {title} (작성자: {author})[/cyan]")
            results.append(f"--- 내용 ---\n{content[:100]}..." if len(content) > 100 else f"--- 내용 ---\n{content}")
            results.append(f"\n[yellow]💡 이제 이 내용을 바탕으로 댓글을 작성할 수 있습니다.[/yellow]")

        except Exception as e:
            results.append(f"[red]✘ 읽기 액션 오류: {str(e)}[/red]")
        
        return results