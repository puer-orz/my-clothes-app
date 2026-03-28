from utils.helpers import get_weather_info

print("Fetching weather...")
weather = get_weather_info()
print(f"Result: {weather}")
