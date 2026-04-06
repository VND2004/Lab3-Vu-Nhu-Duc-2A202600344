# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Vũ Như Đức
- **Student ID**: 2A202600344
- **Date**: 2026-04-06

---

## I. Technical Contribution

*Describe your specific contribution to the codebase.*

- **Modules Implemented**: Xây dựng kịch bản cho `run_chatbot.py` làm Baseline và tập dữ liệu `testcases/travel_agent_questions.json`.
- **Code Highlights**: Tách biệt rõ ràng đối chiếu Chatbot chay so với hệ Agent thực qua script. Tổ chức format Telemetry Baseline để phân tích chỉ số:
  ```python
  logging.info(f"Latency (ms): {response.get('latency_ms', 0)}")
  logging.info(f"Tokens: {response.get('usage', {}).get('total_tokens', 0)}")
  ```
- **Documentation**: Vai trò của Chatbot baseline là tạo nên một điểm neo (metric anchor) tối thiểu. Để chứng minh sức mạnh của Agent, ta cần chứng cứ cho thấy Chatbot gặp thất bại nặng nề với các truy vấn logic từ test cases chuẩn tôi đã soạn thảo.

---

## II. Debugging Case Study

*Analyze a specific failure event you encountered during the lab using the logging system.*

- **Problem Description**: Lỗi "Ảo giác" khi bị hỏi về số lượng và điều kiện thời tiết/giá cả thực tế (Test 1).
- **Log Source**: `log_chatbot.txt` cho thấy Chatbot trả lời rất dõng dạc về lượng mưa và nhiệt độ ở Đà Nẵng: *"Đà Nẵng: 28-34°C, Thể hiện 20% chi phí bù..."*
- **Diagnosis**: Không có kết nối tới dữ liệu thời gian thực (Internet/DB). Mô hình buộc phải bám víu vào trọng số trong quá khứ hoặc "sinh bừa" (Hallucination) để làm hài lòng người dùng.
- **Solution**: Đã cung cấp mẫu thất bại điển hình này vào `Trace_Quality.md` để nhóm lấy động lực cấu hình V1/V2 Agent dựa vào Tool, chấm dứt ảo giác dữ liệu thời gian thực.

---

## III. Personal Insights: Chatbot vs ReAct

*Reflect on the reasoning capability difference.*

1.  **Reasoning**: Chatbot không có luồng Thought, nó có kiến trúc End-to-End. Nhập prompt -> Trả ra kết quả. Nên tốc độ siêu thanh (chưa tới 1 giây so với 4-5 giây của Agent) nhưng kèm theo sự không chính xác thi thoảng.
2.  **Reliability**: Chatbot Baseline ưu việt hoàn toàn so với Agent ở các tác vụ "Không yêu cầu Tool". Ở những tác vụ này, Agent làm phức tạp hóa vấn đề.
3.  **Observation**: Sự thiếu hụt feedback loop khiến Chatbot Baseline mắc một tật xấu "tự tin vào quá trình sinh văn bản định dạng". Sai một ly đi một dặm do sinh thẳng câu chữ. Không có cơ chế nhận biết bản thân đang bịa đặt.

---

## IV. Future Improvements

*How would you scale this for a production-level AI agent system?*

- **Scalability**: Xây dựng một Input Router mạnh mẽ: Đọc câu hỏi người dùng, quyết định câu này phân luồng cho Chatbot Baseline xử lý (câu đơn giản) hay đẩy sang ReAct Agent nặng nề (câu yêu cầu data chuẩn).
- **Safety**: Xây dựng cơ chế Check-Grounding. So khớp kết quả của LLM đầu ra với nguồn tham khảo xem có đạt độ tương đồng cao không rồi mới hiển thị.
- **Performance**: Nhanh chóng đưa vào logic Cache ngữ nghĩa truy vấn (Redis + Vector) đối với cả Chatbot và Agent để tối ưu chi phí API cực đoan của ReAct.
