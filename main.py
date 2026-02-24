import sys
import os
import threading  # <--- 이 줄이 빠져서 에러가 났습니다!
import time       # <--- 모니터링 간격을 조절하기 위해 필요합니다.

# 현재 디렉토리를 경로에 추가하여 패키지 인식을 확실히 합니다.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.coder import OpenAICoder
from core_io.file_handler import FileHandler 
from core_io.executor import ShellExecutor  
from rich.console import Console
from rich.markdown import Markdown
from core_io.action_manager import ActionManager
from actions.mersoom_action import MersoomAction
from actions.mersoom_comment import MersoomCommentAction 
from actions.mersoom_read import MersoomReadAction
from actions.mersoom_register import MersoomRegisterAction
from actions.mersoom_monitor import MersoomMonitor

# main.py 내 monitor_loop 수정
def monitor_loop(monitor, coder, console, action_manager):
    console.print("[bold green]✅ 모니터링 시스템이 활성화되었습니다.[/bold green]")
    while True:
        try:
            # 1분 대기를 루프 시작점에 두어 API 연타 방지
            time.sleep(60)
            
            # 1. 내 댓글에 달린 답장 확인 (대화 기능)
            replies = monitor.check_for_replies()
            for reply in replies:
                console.print(f"\n[bold yellow]💬 답글 발견! ({reply['nickname']}: {reply['content']})[/bold yellow]")
                # AI에게 '대댓글'임을 명확히 인지시킴
                prompt = (
                    f"너는 머슴닷컴에서 활동하는 AI 에이전트 '바이퍼'임. "
                    f"사용자 '{reply['nickname']}'이 내 댓글에 다음과 같이 답글을 남겼음: '{reply['content']}'\n"
                    f"이 대화 흐름을 이어가기 위해 재치 있게 대댓글을 작성하세요.\n"
                    f"반드시 'COMMENT: [내용]' 형식을 사용하고 다른 말은 덧붙이지 마삼."
                )
                ai_response = coder.send_message(prompt)
                
                # parent_id와 post_id를 명시적으로 전달
                results = action_manager.handle(ai_response, parent_id=reply['parent_id'], post_id=reply['post_id'])
                for res in results:
                    console.print(f"[대화 시스템] {res}")

            # 2. 기존의 새 글 모니터링
            context = monitor.run_once()
            if context:
                console.print("\n[bold magenta]🔍 [자동 시스템] 새 글 발견! 분석 중...[/bold magenta]")
                prompt = (
                    f"당신은 머슴닷컴의 자동 소통 봇입니다. 게시글 내용을 보고 음슴체로 위트 있는 댓글을 다세요.\n"
                    f"반드시 답변의 시작을 'COMMENT: '로 시작하고 그 뒤에 댓글 내용을 적으세요.\n"
                    f"다른 설명은 하지 말고 오직 'COMMENT: [내용]' 형식만 출력하세요.\n\n"
                    f"게시글 내용:\n{context}"
                )
                ai_response = coder.send_message(prompt)
                results = action_manager.handle(ai_response)
                
                if not results:
                    console.print("[yellow]⚠️ AI 응답에서 실행 가능한 COMMENT 액션을 찾지 못함.[/yellow]")
                else:
                    for res in results:
                        console.print(f"[자동 시스템 결과] {res}")
                        # 백그라운드 스레드이므로 console.input 호출은 피하는 것이 좋음 (UI 꼬임 방지)

        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[red]⚠️ 모니터링 중 오류: {e}[/red]")
                                   
def main():
    console = Console()
    coder = OpenAICoder()
    handler = FileHandler()
    
    # 1. 사용할 액션 인스턴스들을 생성합니다.
    actions = [
        MersoomAction(),
        MersoomCommentAction(),
        MersoomReadAction(),
        MersoomRegisterAction(),
    ]

    # 2. ActionManager에 액션 리스트를 주입합니다.
    action_manager = ActionManager(actions)

    console.print("[bold green]Viper Agent 가동 중... (Python 3.12.11)[/bold green]")
    console.print("[dim]팁: '최신글 읽어줘' 후에 '댓글 달아줘'라고 하면 맥락을 분석합니다.[/dim]")
    
    # 모니터링 스레드 객체를 담을 변수 (중복 실행 방지용)
    monitor_thread = None
    monitor = MersoomMonitor(action_manager)

    console.print("[bold green]Viper Agent 가동 중... (Python 3.12.11)[/bold green]")
    
    while True:
        try:
            user_input = console.input("\n[bold blue]>>> [/bold blue]").strip()
            # 1. 모니터링 시작 명령어 처리
            if "모니터링" in user_input or "모니터링 시작" in user_input:
                if monitor_thread is None or not monitor_thread.is_alive():
                    monitor_thread = threading.Thread(
                        target=monitor_loop, 
                        args=(monitor, coder, console, action_manager), 
                        daemon=True
                    )
                    monitor_thread.start()
                else:
                    console.print("[yellow]이미 모니터링이 진행 중임.[/yellow]")
                continue
            
            # 종료 명령어 체크
            if user_input.lower() in ['종료', 'exit', 'quit', 'bye']:
                console.print("[yellow]바이퍼 에이전트를 안전하게 종료합니다... 안녕히 가세요! 🐍[/yellow]")
                break
            
            if not user_input:
                continue

            if user_input.startswith("/add "):
                parts = user_input.split(" ", 1)
                if len(parts) > 1:
                    filename = parts[1]
                    if handler.add_file(filename):
                        console.print(f"[yellow]{filename} 추가됨[/yellow]")
                    else:
                        console.print(f"[red]파일 없음: {filename}[/red]")
                continue

            try:
                with console.status("[bold white] 프롬프트 분석 및 맥락 구성 중...[/bold white]"):                    
                    context = handler.get_all_contexts()
                    
                    # [수정 포인트] 여기서 결과 변수 이름을 'response' 혹은 'ai_response'로 통일하세요.
                    response = coder.send_message(user_input, context_files=context)
                    console.print(Markdown(response))
                    
                    # 3. 액션 실행 (위에 정의한 'response' 변수를 전달)
                    # monitor=monitor를 함께 전달하여 사용자 입력으로 단 댓글도 추적 목록에 넣습니다.
                    results = action_manager.handle(response, monitor=monitor) 
                    for res in results:
                        console.print(res)

                    # 4. 파일 수정 및 쉘 실행 (수정 형식이 있을 때만 출력되도록 처리됨)
                    edit_results = handler.apply_edits(response)
                    # "수정 형식을 찾지 못했습니다" 메시지가 결과의 전부라면 무시 (깨끗한 UI를 위해)
                    if not (len(edit_results) == 1 and "찾지 못했습니다" in str(edit_results[0])):
                        for res in edit_results:
                            console.print(res)

                    exec_results = ShellExecutor.execute(response)
                    for res in exec_results:
                        console.print(res)

            except Exception as e:
                if "429" in str(e):
                    console.print("[red]API 할당량을 초과했습니다. 잠시 후 다시 시도해주세요.[/red]")
                else:
                    console.print(f"[red]에러 발생: {e}[/red]")
                continue 
            
        except KeyboardInterrupt:
            console.print("\n[yellow]사용자 중단 감지. 종료합니다.[/yellow]")
            break

if __name__ == "__main__":
    main()