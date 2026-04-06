import os
import sys
from pathlib import Path
import logging

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
from src.agent.agent import ReActAgent
from src.tools.registry import TOOLS
from src.core.openai_provider import OpenAIProvider
import json

def main():
    # Cấu hình logging để ghi vào file log_agent.txt và console
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[
            logging.FileHandler("log_agent.txt", encoding='utf-8', mode='w'),
            logging.StreamHandler()
        ]
    )
    
    # Load environment
    load_dotenv()
    api_key = os.getenv("NVIDIA_API_KEY")
    base_url = os.getenv("NVIDIA_BASE_URL")
    
    # Khởi tạo LLM
    llm = OpenAIProvider(api_key=api_key, base_url=base_url)
    
    # Khởi tạo Agent với max_steps cao hơn cho câu hỏi phức tạp
    agent = ReActAgent(llm=llm, tools=TOOLS, max_steps=8)
    
    
    # Test cases
    with open("testcases/travel_agent_questions.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    test_cases = [sample["question"] for sample in data]
    
    logging.info("="*70)
    logging.info("TESTING REACT AGENT - TRAVEL ADVISOR")
    logging.info("="*70)
    
    for i, question in enumerate(test_cases, 1):
        logging.info(f"\n[TEST {i}] User: {question}")
        logging.info("-"*70)
        
        answer = agent.run(question)
        
        logging.info(f"Agent: {answer}")
        logging.info("="*70)

if __name__ == "__main__":
    main()
