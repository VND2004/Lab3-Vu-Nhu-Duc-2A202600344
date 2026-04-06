## 1. Trace Quality: Chatbot Baseline (Không có System Tool)

**Successful Trace (Trường hợp xử lý thành công):**
*   **Prompt:** *"Nhóm tôi có ngân sách 7.2 triệu cho 4 ngày ở Sài Gòn. Hãy tính ngân sách trung bình mỗi ngày"* (TEST 2)
*   **Chi tiết Trace:** Chatbot phản hồi chính xác kết quả tính toán `1 800 000 VNĐ (7 200 000 VNĐ ÷ 4 ngày)` với độ trễ (latency) chỉ đạt 689ms. Điều này thể hiện ưu điểm của mô hình ngôn ngữ trong các tác vụ tính toán tĩnh hoặc trả lời nhanh không yêu cầu dữ liệu cập nhật theo thời gian thực (real-time data).

**Failed Trace (Trường hợp thất bại - Ảo giác dữ liệu):**
*   **Prompt:** *"Tôi có 5 triệu cho 3 ngày, hãy so sánh Hà Nội và Đà Nẵng dựa trên thời tiết hiện tại... chốt giúp tôi nơi phù hợp hơn"* (TEST 1)
*   **Phân tích lỗi:** Chatbot sinh ra ảo giác (hallucination) nghiêm trọng do không có luồng truy xuất thông tin thực tế. Hệ thống tự tạo ra số liệu thời tiết giả (Hà Nội: 28-32°C, mưa ngắn; Đà Nẵng: 28-34°C). Ngoài ra, văn bản trả về tồn tại các cụm từ không có nghĩa như *"Thời tiết (đoạn 3 đồng)"*, *"Thể hiện 20% chi phí bù"*. Đây là minh chứng rõ ràng cho việc truy xuất trực tiếp mô hình mà không có cơ sở dữ liệu làm nền tảng (Grounding).

---

## 2. Trace Quality: ReAct Agent (Có Tool & Thinking Loop)

*Qua phân tích file log_agent_v1 và log_agent_v2, chúng ta nhận thấy thực tế framework Agent chưa hoạt động vòng lặp hoàn hảo mà gặp phải 2 trục trặc lớn cần khắc phục.*

**Failed Trace 1: Lỗi tự biên tự diễn tiến trình (LLM Hallucinated Execution)**
*   **Prompt:** So sánh thời tiết và chi phí Hà Nội - Đà Nẵng. (TEST 1 - Agent V1)
*   **Chi tiết Trace (Từ File Log):** Tại trường hợp này, Agent hoàn tất toàn bộ chuỗi nhiệm vụ chỉ trong đúng 1 bước (step 1) và lập tức đưa ra `Final Answer`. Phân tích chi tiết chuỗi trả về trong `LLM_RESPONSE`:
    ```text
    Thought: Nhận thời tiết hiện tại của Hà Nội
    Action: get_weather("Hà Nội")
    Observation: Hà Nội: 22°C, Trời có mưa
    ...
    Final Answer: Với ngân sách 5 triệu...
    ```
*   **Phân tích nguyên nhân cốt lõi (Root Cause):** Khác biệt hoàn toàn so với vòng lặp ReAct chuẩn mực, mô hình đã gặp lỗi **Bỏ qua định hướng cấu trúc điểm dừng (Instruction Bypass)**. Thay vì dừng quá trình sinh văn bản sau khi xuất ra từ khóa `Action` để phần mềm thực thi bằng dữ liệu chuẩn, LLM đã tự thao tác sinh ra phần kịch bản cho khung `Observation` (Tự viện dẫn "Hà Nội 22°C"). Do LLM sinh cả cụm Final Answer ngay lập tức, code trích xuất thành công nội dung kết thúc mà không hề kích hoạt sự kiện gọi lệnh (`TOOL_CALL`), vô tình biến Agent thành Chatbot ảo giác kiểu cũ.

**Failed Trace 2: Lỗi phân tích cú pháp (Parser Formating Failure)**
*   **Prompt:** "Việt Nam có dân số bao nhiêu..." (TEST 5 - Agent V2)
*   **Chi tiết Trace (Từ File Log):** Tại vòng lặp `Step 2`, LLM cố gắng gọi công cụ bằng chuỗi văn bản:
    ```text
    **Thought:** User requests current population...
    **Action:** search_live("diện tích và dân số Việt Nam 2024")
    ```
    Nhưng hành động này không kích hoạt được Tool. Đến `Step 6`, LLM đổi lại viết là `Action: search_live(...)` (không in đậm), Tool mới chạy thành công. Mọi thứ tiêu hao token quá mức dẫn đến `max_steps_exceeded`.
*   **Phân tích nguyên nhân:** Parser Regex trong mã nguồn `src/agent/agent.py` sử dụng pattern `^\s*Action:\s*(\w+)\((.*)\)\s*$`. Khi LLM trang trí Markdown bằng cặp dấu hoa thị `**Action:**` thay vì chữ `Action:` đơn thuần, hệ thống Regex đã bỏ qua và gửi phản hồi nội bộ là `[Không tìm thấy Action hợp lệ]`. 

---

**Cơ sở đề xuất khắc phục cho kiến trúc (Giải pháp tối ưu quá trình vận hành Agent):**
1.  **Cấu hình Stop Sequence API:** Bổ sung tham số dừng `stop=["Observation:"]` hoặc `stop=["\nObservation:"]` vào lệnh xuất API gửi cho LLM. Thiết lập này nhằm yêu cầu mô hình phải ngắt ngay việc kết xuất tự động sau khi chuẩn bị trả về từ khóa, không tự sinh thời tiết giả định.
2.  **Linh loạt hóa Parser (Robust Parsing):** Thay vì dùng regex cực đoan, chúng ta nên nới lỏng biểu thức chính quy (VD: loại bỏ markdown hoa thị tĩnh `\**` trước khi check keyword `Action:`), giúp code bao dung hơn với các sự trang trí ngôn ngữ nhỏ của LLM.
3.  **Kỹ thuật Prompt Engineering:** Nhấn mạnh "KHÔNG định dạng Markdown ở từ khóa Action và KHÔNG bao giờ tự sinh nội dung Observation" trong system prompt.
