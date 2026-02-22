import subprocess
import re

class ShellExecutor:
    @staticmethod
    def execute(ai_text):
        # 텍스트 내 어디에 있든 "RUN: 명령어" 패턴을 찾아냅니다.
        commands = re.findall(r"RUN:\s*([^\n]+)", ai_text)
        results = []
        
        for cmd in commands:
            cmd = cmd.strip()
            # 특수 기호 제거 (Gemini가 붙이는 ▌ 등)
            cmd = cmd.split('▌')[0].strip()
            
            try:
                process = subprocess.run(
                    cmd, shell=True, capture_output=True, text=False
                )
                raw_output = process.stdout if process.returncode == 0 else process.stderr
                try:
                    output = raw_output.decode('cp949')
                except:
                    output = raw_output.decode('utf-8', errors='replace')
                
                results.append(f"\n[명령 실행 결과: {cmd}]\n{output}")
            except Exception as e:
                results.append(f"[red]실행 실패: {e}[/red]")
        return results