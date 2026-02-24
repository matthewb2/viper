from actions.file_action import FileAction
from actions.shell_action import ShellAction
from actions.mersoom_action import MersoomAction

# core_io/action_manager.py

class ActionManager:
    def __init__(self, actions):
        self.actions = actions

    def handle(self, ai_text, **kwargs): # **kwargs 추가
        # 1. 무조건 최상단에서 변수 초기화
        all_results = []
        action_found = False 
        
        # 2. ai_text가 문자열이 아니거나 에러 메시지면 바로 반환
        if not isinstance(ai_text, str) or "[시스템 에러]" in ai_text:
            return all_results

        # 3. 액션 매칭 루프
        for action in self.actions:
            if action.match(ai_text):
                try:
                    res = action.execute(ai_text, **kwargs)
                    all_results.extend(res)
                    action_found = True
                except Exception as e:
                    all_results.append(f"[red]액션 실행 중 오류: {str(e)}[/red]")
        
        # 어떤 액션도 매칭되지 않았고, 실제로 명령 키워드가 들어있을 때만 에러 출력
        if not action_found:
            keywords = ["FILE:", "RUN:", "MERSOOM:"]
            if any(key in ai_text for key in keywords):
                all_results.append("[yellow]시스템: 명령 형식을 인식했으나 실행하지 못했습니다.[/yellow]")        
        # 액션이 하나라도 실행되었다면 위 경고를 띄우지 않고 결과를 반환합니다.             
        return all_results