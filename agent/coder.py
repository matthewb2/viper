import google.genai as genai
from openai import OpenAI
from pathlib import Path  # 경로 처리를 위해 추가
import os
from dotenv import load_dotenv
# 외부 프롬프트 파일에서 지침을 가져옵니다.
from .prompts import CODING_INSTRUCTIONS 

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class OpenAICoder: # 이름은 유지해도 되고 GroqCoder로 바꾸셔도 됩니다.
    def __init__(self, model_name="llama-3.3-70b-versatile"): # Groq의 고성능 모델
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            raise ValueError(".env 파일에서 GROQ_API_KEY를 확인하세요.")

        # Groq 서버 주소로 설정하는 것이 핵심!
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1" 
        )
        self.model_id = model_name
        self.system_prompt = CODING_INSTRUCTIONS

    def send_message(self, message, context_files=None):
        messages = [{"role": "system", "content": self.system_prompt}]
        context_str = ""
        if context_files:
            for path, content in context_files.items():
                context_str += f"FILE: {path}\n```\n{content}\n```\n"
        
        user_content = f"{context_str}\n[사용자 요청]\n{message}"
        messages.append({"role": "user", "content": user_content})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                temperature=0.5
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[Groq API 에러] {str(e)}"
class GrokCoder: # 클래스명은 유지하거나 GrokCoder로 변경 가능합니다.
    def __init__(self, model_name="grok-4-latest"): 
        # xAI API 설정
        self.client = OpenAI(
            api_key=os.getenv("XAI_API_KEY"),
            base_url="https://api.x.ai/v1",
        )
        self.model_id = model_name
        self.system_prompt = CODING_INSTRUCTIONS

    def send_message(self, message, context_files=None):
        # 1. 프롬프트 구성
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]
        
        # 2. 파일 컨텍스트 추가
        context_str = ""
        if context_files:
            context_str += "\n[현재 프로젝트 파일 목록 및 내용]\n"
            for path, content in context_files.items():
                context_str += f"FILE: {path}\n```\n{content}\n```\n"
        
        # 3. 사용자 요청 결합
        user_content = f"{context_str}\n[사용자 요청]\n{message}"
        messages.append({"role": "user", "content": user_content})
        
        try:
            # 4. Grok 모델 호출
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                temperature=0.7 # 에이전트의 창의성과 정확성 균형
            )
            return response.choices[0].message.content
            
        except Exception as e:
            return f"[Grok API 에러] 호출 중 오류가 발생했습니다: {str(e)}"
            
class GeminiCoder:
    def __init__(self, model_name="gemini-2.5-flash"):
        # 최신 SDK Client 객체 생성
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model_id = model_name
        # 시스템 지침을 클래스 속성으로 저장하여 재사용
        self.system_prompt = CODING_INSTRUCTIONS

    def send_message(self, message, context_files=None):
        # 1. 시스템 기본 지침 배치
        prompt_parts = [self.system_prompt]
        
        # 2. 파일 컨텍스트 추가
        if context_files:
            prompt_parts.append("\n[현재 프로젝트 파일 목록 및 내용]")
            for path, content in context_files.items():
                prompt_parts.append(f"FILE: {path}\n```\n{content}\n```")
        
        # 3. 사용자 요청 추가
        prompt_parts.append(f"\n[사용자 요청]\n{message}")
        
        # 4. 모델 호출
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents="\n".join(prompt_parts)
            )
            return response.text
        except Exception as e:
            return f"[시스템 에러] 모델 호출 중 오류가 발생했습니다: {str(e)}"