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
        "현재 한국 표준시(KST, Asia/Seoul) 날짜와 시각을 조회합니다. "
        "최신 시각이나 타임스탬프가 필요할 때 호출하세요."
    ),
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
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

