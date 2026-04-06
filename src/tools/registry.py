from src.tools.calculator import calculate
from src.tools.search import search_knowledge
from src.tools.weather import get_weather

# Registry chứa tất cả tools
TOOLS = [
    {
        "name": "calculate",
        "description": "Tính toán biểu thức toán học. Input: biểu thức dạng string (vd: '2+2', '10*5')",
        "function": calculate
    },
    {
        "name": "search_knowledge",
        "description": "Tìm kiếm thông tin trong knowledge base. Input: câu hỏi dạng string",
        "function": search_knowledge
    },
    {
        "name": "get_weather",
        "description": "Lấy thông tin thời tiết của thành phố. Input: tên thành phố",
        "function": get_weather
    }
]

def get_tool_by_name(name: str):
    """Lấy tool function theo tên"""
    for tool in TOOLS:
        if tool["name"] == name:
            return tool["function"]
    return None
