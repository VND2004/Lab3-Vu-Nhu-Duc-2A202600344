def get_weather(city: str) -> str:
    """
    Lấy thông tin thời tiết (giả lập).
    
    Args:
        city: Tên thành phố
    
    Returns:
        Thông tin thời tiết
    """
    # Dữ liệu giả lập
    weather_data = {
        "hanoi": "Hà Nội: 28°C, Trời nắng",
        "hà nội": "Hà Nội: 28°C, Trời nắng",
        "saigon": "Sài Gòn: 32°C, Có mây",
        "sài gòn": "Sài Gòn: 32°C, Có mây",
        "danang": "Đà Nẵng: 30°C, Mưa nhẹ",
        "đà nẵng": "Đà Nẵng: 30°C, Mưa nhẹ",
        "hochiminh": "Hồ Chí Minh: 32°C, Có mây",
        "hồ chí minh": "Hồ Chí Minh: 32°C, Có mây",
    }
    
    city_lower = city.lower().strip()
    
    # Tìm exact match trước
    if city_lower in weather_data:
        return weather_data[city_lower]
    
    # Tìm partial match
    for key, value in weather_data.items():
        if key in city_lower or city_lower in key:
            return value
    
    return f"Không có dữ liệu thời tiết cho: {city}"
