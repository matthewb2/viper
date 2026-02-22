import google.genai as genai
import os
from dotenv import load_dotenv
from .prompts import CODING_INSTRUCTIONS

load_dotenv()

class GeminiCoder:
    def __init__(self, model_name="gemini-2.5-flash"): # 2026년 기준 최신 모델 사용 권장
        # 최신 SDK는 Client 객체를 생성하여 사용합니다.
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_id = model_name
        self.chat_history = []

# agent/coder.py

    def send_message(self, message, context_files=None):
        # 시스템 역할을 아주 강력하게 부여합니다.
        system_prompt = f"""당신은 사용자의 컴퓨터 시스템과 직접 연결된 자동화 에이전트입니다.
친절한 설명은 필요 없습니다. 사용자의 요청을 수행하기 위해 반드시 아래의 '규칙'에 맞는 텍스트만 출력하세요.

규칙 1 (파일 수정): 
반드시 아래 형식을 지키세요. 공백이나 기호가 하나라도 틀리면 시스템이 인식하지 못합니다.
FILE: 경로/파일명
<<<< SEARCH
기존 코드 내용 (비어있을 경우 아무것도 적지 마세요)
====
새로운 코드 내용
>>>> REPLACE

규칙 2 (명령 실행):
수정 후 실행이 필요하다면 반드시 아래 형식을 답변 끝에 포함하세요.
RUN: 실행할 명령어

응답 예시:
FILE: test_code.py
<<<< SEARCH
====
print("안녕 바이퍼")
>>>> REPLACE
RUN: python test_code.py
"""
        
        prompt_parts = [system_prompt]
        
        if context_files:
            prompt_parts.append("\n[현재 프로젝트 파일 목록 및 내용]")
            for path, content in context_files.items():
                prompt_parts.append(f"FILE: {path}\n```\n{content}\n```")
        
        prompt_parts.append(f"\n[사용자 요청]\n{message}")
        
        # 실제 모델 전송
        response = self.client.models.generate_content(
            model=self.model_id,
            contents="\n".join(prompt_parts)
        )
        return response.text