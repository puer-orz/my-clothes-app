import requests
import json
import random

def get_client_ip():
    """尝试从 Streamlit 上下文获取真实客户端 IP"""
    try:
        import streamlit as st
        # 检查是否支持 st.context (Streamlit >= 1.37)
        if hasattr(st, 'context'):
            headers = st.context.headers
            # 尝试常见代理/负载均衡透传的真实 IP 头部
            for header in ["X-Forwarded-For", "X-Real-Ip", "CF-Connecting-IP"]:
                ip = headers.get(header)
                if ip:
                    # 可能包含多个IP（经过多个代理），取第一个非内网的，通常第一个就是真实客户端IP
                    return ip.split(',')[0].strip()
    except Exception as e:
        print(f"Failed to get client IP from context: {e}")
    return None

def get_current_location_data():
    """
    通过 IP 获取当前位置的详细信息 (包含经纬度)
    尝试多个免费的 IP 定位 API，提高成功率
    """
    client_ip = get_client_ip()
    ip_path = f"/{client_ip}" if client_ip else ""
    ip_param = f"?ip={client_ip}" if client_ip else ""

    # 方案 1: ipapi.co (备用，通常比 ip-api.com 准，特别是防代理)
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        url = f'https://ipapi.co{ip_path}/json/'
        response = requests.get(url, headers=headers, timeout=3)
        data = response.json()
        if 'city' in data and data['city']:
            return {
                "city": data['city'],
                "country": data.get('country_name', 'CN'),
                "lat": data.get('latitude'),
                "lon": data.get('longitude'),
                "display": f"{data['city']}, {data.get('country_name', 'CN')}"
            }
    except Exception as e:
        print(f"ipapi.co fallback: {e}")
        
    # 方案 2: ip-api (最快，支持显式传递 IP)
    try:
        url = f'http://ip-api.com/json{ip_path}?lang=zh-CN'
        response = requests.get(url, timeout=3)
        data = response.json()
        if data['status'] == 'success' and data.get('city'):
            return {
                "city": data['city'],
                "country": data['country'],
                "lat": data['lat'],
                "lon": data['lon'],
                "display": f"{data['city']}, {data['country']}"
            }
    except Exception as e:
        print(f"ip-api fallback: {e}")

    # 方案 3: ip.useragentinfo.com (备用 2，纯国内库)
    try:
        url = f'https://ip.useragentinfo.com/json{ip_param}'
        response = requests.get(url, timeout=3)
        data = response.json()
        if 'city' in data and data['city']:
            city = data['city'].replace('市', '')
            return {
                "city": city,
                "country": data.get('country', '中国'),
                "lat": None,
                "lon": None,
                "display": f"{city}, {data.get('country', '中国')}"
            }
    except Exception as e:
        print(f"useragentinfo fallback: {e}")

    return None

def get_current_location():
    """通过 IP 获取当前城市 (兼容旧接口)"""
    data = get_current_location_data()
    if data:
        return data['display']
    return "未知地点" # 不再硬编码北京，让 AI 去猜或者前端提示用户
    """
    从 Open-Meteo 获取实时天气 (无需 Key，免费，快速)
    """
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "weather_code"],
            "timezone": "auto"
        }
        
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        current = data['current']
        
        # WMO Weather interpretation codes (WW)
        weather_code = current['weather_code']
        weather_desc = "未知"
        
        # 简单映射
        if weather_code == 0: weather_desc = "晴"
        elif weather_code in [1, 2, 3]: weather_desc = "多云"
        elif weather_code in [45, 48]: weather_desc = "雾"
        elif weather_code in [51, 53, 55]: weather_desc = "毛毛雨"
        elif weather_code in [61, 63, 65]: weather_desc = "雨"
        elif weather_code in [71, 73, 75]: weather_desc = "雪"
        elif weather_code >= 95: weather_desc = "雷雨"
        
        return {
            "description": weather_desc,
            "temp": current['temperature_2m'],
            "humidity": current['relative_humidity_2m'],
            "feels_like": current['apparent_temperature'],
            "raw": f"天气: {weather_desc}, 温度: {current['temperature_2m']}°C, 体感: {current['apparent_temperature']}°C, 湿度: {current['relative_humidity_2m']}%"
        }
    except Exception as e:
        print(f"Open-Meteo Error: {e}")
        return None

def get_current_location():
    """通过 IP 获取当前城市 (兼容旧接口)"""
    data = get_current_location_data()
    if data:
        return data['display']
    return "未知地点" # 不再硬编码北京，让 AI 去猜或者前端提示用户

def get_weather_from_open_meteo(lat, lon):
    """
    从 Open-Meteo 获取实时天气 (无需 Key，免费，快速)
    """
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "weather_code"],
            "timezone": "auto"
        }
        
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        
        current = data['current']
        
        # WMO Weather interpretation codes (WW)
        weather_code = current['weather_code']
        weather_desc = "未知"
        
        # 简单映射
        if weather_code == 0: weather_desc = "晴"
        elif weather_code in [1, 2, 3]: weather_desc = "多云"
        elif weather_code in [45, 48]: weather_desc = "雾"
        elif weather_code in [51, 53, 55]: weather_desc = "毛毛雨"
        elif weather_code in [61, 63, 65]: weather_desc = "雨"
        elif weather_code in [71, 73, 75]: weather_desc = "雪"
        elif weather_code >= 95: weather_desc = "雷雨"
        
        return {
            "description": weather_desc,
            "temp": current['temperature_2m'],
            "humidity": current['relative_humidity_2m'],
            "feels_like": current['apparent_temperature'],
            "raw": f"天气: {weather_desc}, 温度: {current['temperature_2m']}°C, 体感: {current['apparent_temperature']}°C, 湿度: {current['relative_humidity_2m']}%"
        }
    except Exception as e:
        print(f"Open-Meteo Error: {e}")
        return None

def get_weather_info(city=None):
    """
    (已弃用，请使用 get_weather_from_ai)
    获取天气信息。
    如果 city 为空，wttr.in 会根据 IP 自动定位。
    """
    try:
        # 使用 format=j1 获取详细 JSON 数据
        url = "https://wttr.in"
        if city:
            url += f"/{city}"
        url += "?format=j1"
        
        response = requests.get(url, timeout=5)
        data = response.json()
        
        current = data['current_condition'][0]
        weather_desc = current['lang_zh'][0]['value']
        temp = current['temp_C']
        humidity = current['humidity']
        feels_like = current['FeelsLikeC']
        
        return {
            "description": weather_desc,
            "temp": temp,
            "humidity": humidity,
            "feels_like": feels_like,
            "raw": f"天气: {weather_desc}, 温度: {temp}°C, 体感: {feels_like}°C, 湿度: {humidity}%"
        }
    except Exception as e:
        print(f"Weather API Error: {e}")
        # Fallback: 返回一个合理的默认天气（晴天，适宜温度），保证演示效果
        # 在真实生产环境中，这里可以切换到备用 API 或让用户手动输入
        
        # 随机一点点变化，让用户感觉不是死数据
        mock_temps = [20, 22, 24, 25, 26]
        mock_temp = random.choice(mock_temps)
        
        return {
            "description": "晴 (模拟数据)",
            "temp": str(mock_temp),
            "humidity": "45",
            "feels_like": str(mock_temp + 2),
            "raw": f"天气: 晴 (网络超时，使用模拟数据), 温度: {mock_temp}°C",
            "error": str(e),
            "is_mock": True
        }
