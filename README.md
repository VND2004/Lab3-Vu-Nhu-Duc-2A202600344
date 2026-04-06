# Lab 3: Chatbot vs ReAct Agent (Bản Tiêu Chuẩn Công Nghiệp)

Chào mừng bạn đến với Giai đoạn 3 của khóa học Agentic AI! Bài thực hành (Lab) này tập trung vào việc chuyển đổi từ một LLM Chatbot đơn giản sang một **ReAct Agent** phức tạp có hệ thống giám sát chuẩn công nghiệp.

## 🚀 Hướng Dẫn Bắt Đầu

### 1. Cấu hình Môi trường (Setup Environment)
Sao chép `.env.example` thành `.env` và cung cấp bộ API Keys của bạn (hệ thống hiện đang sử dụng Provider qua chuẩn OpenAI cho **NVIDIA API**):
```bash
cp .env.example .env
```
Vào tệp `.env`, điền thông tin:
```env
NVIDIA_API_KEY="your_api_key_here"
NVIDIA_BASE_URL="https://integrate.api.nvidia.com/v1"
```

### 2. Cài đặt Thư viện (Install Dependencies)
```bash
pip install -r requirements.txt
```

### 3. Cấu trúc Thư mục (Directory Structure)
- `src/agent/`: Mã nguồn cốt lõi về vòng lặp ReAct.
- `src/tools/`: Các tệp registry chứa định nghĩa công cụ V1 và V2.
- `src/telemetry/`: Module theo dõi log và metrics.
- `testcases/`: File chứa tập dữ liệu câu hỏi kiểm thử.
- `loggings/`: Nơi xuất file nội dung log tự động.

## 💻 Cách Chạy Chương Trình (Usage)

Dự án cung cấp 2 chế độ chính: **Chatbot Baseline** và **ReAct Agent** thông qua CLI arguments.

### 1. Chạy Chatbot Baseline
Dùng kịch bản cơ bản nhất (trả lời trực tiếp bằng LLM, không xài Tool).
```bash
# Chạy bộ câu hỏi chuẩn trong testcases
python src/run_chatbot.py

# Tuỳ chỉnh câu hỏi hoặc lưu ra file log khác
python src/run_chatbot.py --question "Hà Nội có bao nhiêu dân?" --log-file loggings/chatbot_test.txt
```

### 2. Chạy ReAct Agent
Sử dụng AI có thể tự gọi Tool để phân tích và ra quyết định.
```bash
# Chạy Agent với bộ Tools V1, tối đa 8 bước
python src/run_agent.py --registry 1 --max-steps 8

# Chạy Agent với bộ Tools V2, chạy 1 câu hỏi tùy chọn
python src/run_agent.py --registry 2 --question "Du lịch Hà Nội với 5 triệu cho 3 ngày thì sao?"

# Chạy Agent với hệ thống System Prompt nâng cấp (chứng minh dự án hỗ trợ nhiều prompt)
python src/run_agent.py --registry 2 --prompt-path "src/prompts/system_prompt_v2.txt"

# Xem toàn bộ tham số linh hoạt hỗ trợ
python src/run_agent.py --help
```
*(Tham số `--registry 1` hoặc `2` tương ứng với `registry.py` và bộ tool enhanced `registry_2.py`. Tham số `--prompt-path` giúp thay đổi file kỹ thuật Prompt Engineering.)*

## 🎯 Mục Tiêu Bài Lab (Objectives)

1. **Chatbot Cơ bản (Baseline)**: Quan sát những điểm hạn chế của một LLM thông thường khi phải đối mặt với yêu cầu suy luận nhiều bước.
2. **Vòng lặp ReAct**: Triển khai chu trình `Thought-Action-Observation` (Suy nghĩ-Hành động-Quan sát) bên trong tệp `src/agent/agent.py`.
3. **Chuyển đổi Provider LLM**: Dễ dàng chuyển đổi giữa OpenAI và Gemini (hoặc NVIDIA API) thông qua việc sử dụng interface `LLMProvider`.
4. **Phân tích Lỗi (Failure Analysis)**: Phân tích log có cấu trúc trong thư mục `loggings/` để tìm ra gốc rễ việc agent hoạt động sai (ví dụ: ảo giác, lỗi phân tích cú pháp Regex).
5. **Chấm điểm & Bonus**: Tuân thủ và đọc kỹ file `SCORING.md` để lấy trọn số tiền điểm cùng các điểm thưởng nâng cao khác.

## 🛠️ Đặc Điểm Cốt Lõi Của Source Code Này
Dự án được thiết kế như một **Bản Mẫu Tiêu chuẩn Sản xuất (Production Prototype)**. Nó bao gồm:
- **Telemetry**: Mỗi tác vụ đều được ghi nhận (log) bằng các sự kiện event rõ ràng hỗ trợ theo dõi thông số chuẩn xác.
- **Provider Pattern Mạnh Mẽ**: Dễ dàng tích hợp với bất kỳ API LLM nào (Gemini, ChatGPT, Deepseek, v.v.).
- **Clean Skeletons**: Tập trung vào tư duy thuật toán cốt lõi — quy trình lập luận của Agent.

---

*Happy Coding! Cùng nhau xây dựng hệ thống Agent chất lượng thật sự.*
