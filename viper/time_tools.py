import json
from datetime import datetime
from zoneinfo import ZoneInfo


def get_current_kst_time() -> str:
    """현재 한국 표준시(KST, Asia/Seoul) 시각을 문자열로 반환합니다."""
    now_kst = datetime.now(ZoneInfo("Asia/Seoul"))
    return now_kst.strftime("%Y-%m-%d %H:%M:%S (KST)")


TIME_TOOL_DECLARATION = {
    "name": "get_current_kst_time",
    "description": (
        "Get the current date and time in Korea Standard Time (KST, Asia/Seoul). "
        "현재 한국 표준시(KST, Asia/Seoul) 날짜와 시각을 조회합니다. "
        "Call this tool whenever the user asks for the current time/date in Korea or "
        "needs an exact KST timestamp for edits. Do not guess the time."
    ),
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False,
    },
}

KST_TIME_TOOL_SCHEMA = [
    {
        "type": "function",
        "function": TIME_TOOL_DECLARATION,
    }
]


def execute_time_tool(tool_name: str, arguments=None) -> str:
    if tool_name == "get_current_kst_time":
        return get_current_kst_time()
    raise ValueError(f"Unknown tool: {tool_name}")


TOOL_REGISTRY = {
    "get_current_kst_time": lambda args=None: get_current_kst_time(),
}
