import os
import sys
from pathlib import Path
import logging
import json

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
from src.core.openai_provider import OpenAIProvider


def main():
    # Cấu hình logging để ghi vào file log_chatbot.txt và console
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[
            logging.FileHandler("log_chatbot.txt", encoding="utf-8", mode="w"),
            logging.StreamHandler(),
        ],
    )

    # Load environment
    load_dotenv()
    api_key = os.getenv("NVIDIA_API_KEY")
    base_url = os.getenv("NVIDIA_BASE_URL")

    # Khởi tạo LLM cho chatbot baseline
    llm = OpenAIProvider(api_key=api_key, base_url=base_url)

    system_prompt = (
        "Bạn là trợ lý du lịch, trả lời ngắn gọn, thực tế, ưu tiên dữ liệu rõ ràng và không tự bịa khi thiếu thông tin."
    )

    # Test cases
    with open("testcases/travel_agent_questions.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    test_cases = [sample["question"] for sample in data]

    logging.info("=" * 70)
    logging.info("TESTING CHATBOT BASELINE - TRAVEL ADVISOR")
    logging.info("=" * 70)

    for i, question in enumerate(test_cases, 1):
        logging.info(f"\n[TEST {i}] User: {question}")
        logging.info("-" * 70)

        response = llm.generate(question, system_prompt=system_prompt)
        answer = response.get("content", "")

        logging.info(f"Chatbot: {answer}")
        logging.info(f"Provider: {response.get('provider', 'unknown')}")
        logging.info(f"Latency (ms): {response.get('latency_ms', 0)}")
        logging.info(f"Tokens: {response.get('usage', {}).get('total_tokens', 0)}")
        logging.info("=" * 70)


if __name__ == "__main__":
    main()