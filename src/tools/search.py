def search_knowledge(query: str) -> str:
    """
    Tìm kiếm thông tin trong knowledge base giả lập.
    
    Args:
        query: Câu hỏi cần tìm kiếm
    
    Returns:
        Thông tin tìm được
    """
    # Knowledge base đơn giản
    knowledge = {
        "vietnam capital": "Thủ đô của Việt Nam là Hà Nội",
        "vietnam population": "Dân số Việt Nam khoảng 100 triệu người",
        "python": "Python là ngôn ngữ lập trình cấp cao, dễ học",
        "ai agent": "AI Agent là hệ thống có khả năng suy luận và hành động tự động",
        "react": "ReAct là framework kết hợp Reasoning và Acting cho AI Agent",
        
        # Thông tin du lịch
        "chi phí hà nội": "Chi phí du lịch Hà Nội: 1.2-1.5 triệu/ngày (ăn uống, khách sạn, di chuyển)",
        "chi phí đà nẵng": "Chi phí du lịch Đà Nẵng: 1.5-2 triệu/ngày (ăn uống, khách sạn, di chuyển)",
        "chi phí sài gòn": "Chi phí du lịch Sài Gòn: 1.3-1.8 triệu/ngày (ăn uống, khách sạn, di chuyển)",
        "du lịch hà nội": "Hà Nội nổi tiếng với Hồ Gươm, Văn Miếu, Phố Cổ. Thích hợp mùa thu (Sep-Nov)",
        "du lịch đà nẵng": "Đà Nẵng có biển đẹp, Bà Nà Hills, Cầu Vàng. Thích hợp mùa hè (Apr-Aug)",
        "du lịch sài gòn": "Sài Gòn sôi động với Nhà thờ Đức Bà, Chợ Bến Thành, phố đi bộ Nguyễn Huệ",
    }
    
    query_lower = query.lower()
    for key, value in knowledge.items():
        if key in query_lower:
            return value
    
    return f"Không tìm thấy thông tin về: {query}"
