from tools.calculator import calculate
from tools.text_utils import text_utility
from tools.weather import get_weather
from tools.currency import convert_currency

print("\n--- CALCULATOR ---")
print(calculate("25 * 4 + 10"))

print("\n--- TEXT ---")
print(text_utility("Hello world from my AI agent", "word_count"))

print("\n--- WEATHER ---")
print(get_weather("Mumbai"))

print("\n--- CURRENCY ---")
print(convert_currency(100, "USD", "INR"))