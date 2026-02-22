import sys
import os

# 현재 디렉토리를 경로에 추가하여 패키지 인식을 확실히 합니다.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.coder import GeminiCoder
from core_io.file_handler import FileHandler # io -> core_io
from core_io.executor import ShellExecutor  # 이 줄이 반드시 있어야 합니다!
from rich.console import Console
from rich.markdown import Markdown

def main():
    console = Console()
    coder = GeminiCoder()
    handler = FileHandler()

    console.print("[bold green]Gemini AI Agent 가동 중... (Python 3.12.11)[/bold green]")
    
    while True:
        try:
            user_input = console.input("\n[bold blue]>>> [/bold blue]")
            
            if user_input.lower() in ['exit', 'quit']:
                break
            
            if user_input.startswith("/add "):
                parts = user_input.split(" ", 1)
                if len(parts) > 1:
                    filename = parts[1]
                    if handler.add_file(filename):
                        console.print(f"[yellow]{filename} 추가됨[/yellow]")
                    else:
                        console.print(f"[red]파일 없음: {filename}[/red]")
                continue
            # main.py 내부의 send_message 호출 부분 수정
            try:
                with console.status("[bold white]Gemini가 분석 중...[/bold white]"):
                    context = handler.get_all_contexts()
                    response = coder.send_message(user_input, context_files=context)
                    console.print(Markdown(response))

                    edit_results = handler.apply_edits(response)
                    for res in edit_results:
                        console.print(res)

                    exec_results = ShellExecutor.execute(response)
                    for res in exec_results:
                        console.print(res)
            except Exception as e:
                if "429" in str(e):
                    console.print("[red]API 할당량을 초과했습니다. 잠시 후 다시 시도해주세요 (약 1분).[/red]")
                else:
                    console.print(f"[red]에러 발생: {e}[/red]")
                continue # 에러 발생 시 다음 루프로 바로 이동
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()