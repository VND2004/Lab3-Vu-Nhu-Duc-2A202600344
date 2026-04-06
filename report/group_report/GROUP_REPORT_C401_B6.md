# Báo cáo Nhóm: Lab 3 - Hệ thống Agentic Cấp độ Production

- **Tên Nhóm**: C401-B6
- **Thành viên Nhóm**: 
Trần Anh Tú - 2A202600291 \
Hoàng Văn Bắc - 2A202600076 \
Vũ Phúc Thành - 2A202600345 \
Lương Hữu Thành - 2A202600114 \
Nguyễn Tiến Thắng - 2A202600220 \
Vũ Như Đức - 2A202600344 \
Nguyễn Như Giáp - 2A202600192 \
- **Ngày Triển khai**: 2026-04-06

---

## 1. Tóm tắt Điều hành (Executive Summary)

*Tổng quan ngắn gọn về mục tiêu của agent và tỷ lệ thành công so với chatbot cơ bản.*

- **Tỷ lệ Thành công**: Chatbot (100% nhưng ảo giác dữ liệu thời tiết), Agent V1 (100%), Agent V2 (80% - gặp lỗi vòng lặp ở Test 5).
- **Kết quả Chính**: Agent V1 hoạt động ổn định nhất với các công cụ cơ bản (`get_weather`, `calculate`, `search_knowledge`), giải quyết tốt các truy vấn nhiều bước. Khi nâng cấp lên Agent V2 với công cụ `search_live` (tìm kiếm internet trực tiếp), chất lượng câu trả lời phong phú hơn, tuy nhiên lại gặp rủi ro vòng lặp vô hạn (max_steps_exceeded) khi kết quả trả về quá tải dung lượng.

---

## 2. Kiến trúc Hệ thống & Công cụ

### 2.1 Triển khai Vòng lặp ReAct
Vòng lặp ReAct tuân theo mô hình Thought-Action-Observation (Suy nghĩ-Hành động-Quan sát), trong đó agent tạo ra một bước suy luận (Thought), lựa chọn và thực thi một công cụ (Action), sau đó đưa kết quả của công cụ (Observation) vào bước suy luận tiếp theo. Quá trình lặp lại này tiếp tục cho đến khi đạt được câu trả lời cuối cùng.

### 2.2 Định nghĩa Công cụ (Sự tiến hóa của Tool Registry)
| Phiên bản | Tên Công cụ      | Định dạng Đầu vào | Trường hợp Sử dụng                                      |
| :--- | :--------------- | :----------- | :------------------------------------------- |
| **V1/V2** | `get_weather`    | `string`     | Lấy thông tin thời tiết hiện tại cho một thành phố cụ thể.   |
| **V1/V2** | `calculate`      | `string`     | Thực hiện các phép tính toán học.           |
| **V1** | `search_knowledge`| `string`     | Tìm kiếm thông tin cụ thể trong cơ sở kiến thức nội bộ. |
| **V2** | `search_live` | `string`     | (Mới) Tìm kiếm trực tiếp trên internet để lấy dữ liệu thực tế (thay thế search_knowledge). |

### 2.3 LLM Provider Được Sử dụng
- **Chính**: OpenAI GPT-OSS-20B
- **Phụ (Dự phòng)**: Không có

---

## 3. Telemetry & Dashboard Hiệu suất

*So sánh các chỉ số đo lường (Telemetry) thu thập được giữa Chatbot, Agent V1 và Agent V2.*

- **Độ trễ Tối đa trong một truy vấn (P99)**: Chatbot (~9.5s) | Agent V1 (~3.9s) | Agent V2 (>10s cho các tác vụ nhiều bước).
- **Số lượng Token Tiêu thụ**: Agent V2 tiêu thụ nhiều token nhất (lên tới ~4322 tokens ở Test 5) do sử dụng `search_live` trả về lượng văn bản rất lớn. Agent V1 tối ưu với ~1200 tokens/test. Chatbot tốn cực ít (~800 tokens) nhưng dễ sinh ra ảo giác.
- **Tổng Chi phí bộ Thử nghiệm**: Agent V2 tốn kém nhất (~$0.15 ước tính), trong khi Agent V1 có mức phí tối ưu (~$0.06). Dữ liệu này cho thấy Agent V1 đạt hiệu quả về chi phí - hiệu năng tốt nhất so với 2 hệ thống còn lại.

---

## 4. Chất lượng Trace & Phân tích Nguyên nhân Gốc rễ (Trace Quality & RCA)

### 4.1 Trace Quality: Chatbot Baseline (Không có System Tool)

**Successful Trace (Trường hợp xử lý thành công):**
*   **Prompt:** *"Nhóm tôi có ngân sách 7.2 triệu cho 4 ngày ở Sài Gòn. Hãy tính ngân sách trung bình mỗi ngày"* (TEST 2)
*   **Chi tiết Trace:** Chatbot phản hồi chính xác kết quả tính toán `1 800 000 VNĐ (7 200 000 VNĐ ÷ 4 ngày)` với độ trễ (latency) chỉ đạt 689ms.

**Failed Trace (Trường hợp thất bại - Ảo giác dữ liệu):**
*   **Prompt:** *"Tôi có 5 triệu cho 3 ngày, hãy so sánh..."* (TEST 1)
*   **Phân tích lỗi:** Chatbot sinh ra ảo giác (hallucination) nghiêm trọng do không có luồng truy xuất thông tin thực tế. Hệ thống tự tạo ra số liệu thời tiết giả (Hà Nội: 28-32°C, mưa ngắn; Đà Nẵng: 28-34°C).

### 4.2 Trace Quality: ReAct Agent (Có Tool & Thinking Loop)

*Qua phân tích file log_agent_v1 và log_agent_v2, framework Agent chưa hoạt động vòng lặp hoàn hảo mà gặp phải 2 trục trặc lớn cần khắc phục.*

**Failed Trace 1: Lỗi tự biên tự diễn tiến trình (LLM Hallucinated Execution)**
*   **Prompt:** So sánh thời tiết và chi phí Hà Nội - Đà Nẵng. (TEST 1 - Agent V1)
*   **Chi tiết Trace:** Agent hoàn tất nhiệm vụ chỉ trong đúng 1 bước và lập tức đưa ra `Final Answer`. Thay vì dừng lại ở `Action` để chạy code, LLM tự thao tác sinh ra phần kịch bản cho khung `Observation` (Tự viện dẫn "Hà Nội 22°C").
*   **Root Cause:** Lỗi Bỏ qua định hướng cấu trúc điểm dừng (Instruction Bypass). Code trích xuất Final Answer mà không kích hoạt sự kiện gọi lệnh (`TOOL_CALL`).

**Failed Trace 2: Lỗi phân tích cú pháp (Parser Formatting Failure)**
*   **Prompt:** "Việt Nam có dân số bao nhiêu..." (TEST 5 - Agent V2)
*   **Chi tiết Trace:** Tại `Step 2`, LLM gửi về `**Action:** search_live(...)`. Lệnh này bị bỏ qua gây vòng lặp rác liên tục.
*   **Root Cause:** Parser Regex trong `src/agent/agent.py` dùng mẫu `^\s*Action:\s*...`. Việc LLM tự động trang trí Markdown (`**Action:**`) làm Regex bị hỏng, trả về `[Không tìm thấy Action hợp lệ]`. Hậu quả sinh ra vòng lặp vô hạn `max_steps_exceeded`.

**Giải pháp Xử lý (Fixes):**
1. Cấu hình Stop Sequence API (`stop=["Observation:"]`).
2. Tối ưu lại biểu thức chính quy Regex trong trình phân tích cú pháp để chịu lỗi tốt hơn với markdown.

---

## 5. Lưu đồ & Bài học Kinh nghiệm (Flowchart & Insight)

### 5.1 Lưu đồ Logic Cốt lõi (Visual Logic Diagram)

```mermaid
flowchart TD
    US[User Input] --> ModelChoice{Execute As?}
    
    %% Chatbot Flow
    subgraph Baseline Chatbot (src/chatbot.py)
    ModelChoice -->|Chatbot| CB1[Build System & User Prompts]
    CB1 --> CB2[Call LLM API]
    CB2 --> CB3[Stream Output]
    CB3 --> CB4[Print Content & Reasoning]
    end
    
    %% ReAct Agent Flow
    subgraph ReAct Agent (src/agent/agent.py)
    ModelChoice -->|Agent| RE1[Log AGENT_START & Init Context]
    RE1 --> RE2{while steps < max_steps?}
    RE2 -->|Yes| RE3[Call LLM generate]
    RE3 --> RE4{Has 'Final Answer:'?}
    
    RE4 -->|Yes| RE5[Extract Answer & Log AGENT_END]
    
    RE4 -->|No| RE6{Has 'Action:'?}
    RE6 -->|Yes| RE7[Extract Tool Name & Args]
    RE7 --> RE8[Execute Tool]
    RE8 --> RE9[Get Observation]
    RE9 --> RE10[Append Observation to Context]
    RE10 --> RE2
    
    RE6 -->|No| RE11[Append Invalid Action Observation]
    RE11 --> RE2
    
    RE2 -->|No| RE12[Log max_steps_exceeded & Return Error]
    end

    %% Telemetry Subsystem
    subgraph Telemetry & Metrics
    RE1 -.-> TM1[(Logger)]
    RE3 -.-> TM1
    RE7 -.-> TM1
    RE8 -.-> TM1
    RE5 -.-> TM1
    RE12 -.-> TM1
    RE3 -.-> TM2[(Tracker: Usage & Latency)]
    end
```

### 5.2 Bài học Kinh nghiệm chung (Group Insights)

- **Chatbot Cơ bản** (`src/chatbot.py`) quá thiếu thông tin tương tác với bên ngoài, khiến nó ảo giác một lượng lớn dữ liệu đo lường.
- **ReAct Loop** (`src/agent/agent.py`) hoạt động tốt nhưng khả năng trích xuất (parsing logic) của mã nguồn mang tính sống còn. Lỗi định dạng nhẹ của LLM cũng có thể làm crash toàn bộ vòng lặp.
- **Việc đo lường (Telemetry Logs)** tạo ra sự khác biệt khổng lồ. Nhờ hook vào từng step (`TOOL_CALL`, `LLM_RESPONSE`), nhóm mới tìm ra chuẩn xác lỗi Regex Parser ở Test 5 và hiện tượng Agent "tự biên tự diễn" (Bypass) ở Test 1.

---

## 6. Nghiên cứu Thực nghiệm & Đánh giá (Evaluation & Analysis)

### Đánh giá sự khác biệt: Chatbot vs Agent V1 vs Agent V2
- **Chatbot Base**: Chỉ đáng để hỏi đáp đơn giản. Hoàn toàn dựa vào bộ nhớ (tự "bịa" dữ liệu thời tiết thực tế).
- **Agent V1**: Tốn chi phí và thời gian gọi LLM (từ 1 tới nhiều step), đôi khi gặp lỗi bypass tool (Test 1), nhưng về cơ bản mang lại lý luận Thought-Action rõ ràng, độ tin cậy vượt xa chatbot.
- **Agent V2**: Nâng cấp công cụ `search_live` cho trải nghiệm sinh động. Outputs ở Test 4 trình bày báo cáo markdown với thông tin du lịch khá chuẩn. Việc cập nhật trực tiếp tạo ra sự đột phá về chất lượng, trừ những lúc rủi ro vào loop parser.

| Trường hợp Test | Chatbot | Agent V1 | Agent V2 |
| :------------------- | :-------------- | :---------------- | :-------- |
| So sánh Du lịch, Chi phí | Cung cấp thông tin cũ, tỷ lệ ảo giác 100% về thời tiết trực tiếp | Khá an toàn nhưng dữ liệu phụ thuộc kho nội bộ | Trình bày markdown xuất sắc, số liệu thực 2024 |
| Tính Toán Chi phí Cơ bản | Chính xác | Chính xác | Phân tích sâu, kèm nhắc nhở budget |
| Số liệu tĩnh (Dân số/Diện tích) | Thông tin cũ (98 triệu) | Lấy qua knowledge | Thất bại (Loop / Parser Regex Error) |

---
