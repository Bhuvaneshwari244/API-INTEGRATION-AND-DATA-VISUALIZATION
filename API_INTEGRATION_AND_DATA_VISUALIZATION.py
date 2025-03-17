import requests
import matplotlib.pyplot as plt
import seaborn as sns

# OpenWeatherMap API Key (Replace with your actual API key)
API_KEY = "7e89a2a66ecafbdc486d2570dd341789"  # Keep your actual API key
CITY = "Delhi,IN"  # Change city to any Indian city
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

# Fetch Weather Data
def fetch_weather_data(city):
    if not API_KEY or API_KEY == "your_actual_api_key_here":
        print("\n❌ ERROR: API key is missing! Please update the API_KEY variable.")
        return None

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()

        if "list" not in data:
            print(f"\n❌ API Error: {data.get('message', 'Unknown error')}")
            return None
        
        return data

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request Error: {e}")
        return None

# Parse Data
def extract_weather_info(data):
    if not data:
        print("\n❌ No data available to extract.")
        return [], [], [], []
    
    dates, temperatures, humidity, wind_speeds = [], [], [], []
    for entry in data["list"]:
        dates.append(entry["dt_txt"])
        temperatures.append(entry["main"]["temp"])
        humidity.append(entry["main"]["humidity"])
        wind_speeds.append(entry["wind"]["speed"])
    
    return dates, temperatures, humidity, wind_speeds

# Visualization
def plot_weather(dates, temperatures, humidity, wind_speeds):
    if not dates:
        print("\n❌ No data available to plot.")
        return
    
    plt.figure(figsize=(12, 8))
    
    # Temperature Plot
    plt.subplot(3, 1, 1)
    sns.lineplot(x=dates, y=temperatures, marker="o", color="red")
    plt.xticks(rotation=45)
    plt.title("Temperature Over Time (°C)")
    plt.ylabel("Temp (°C)")
    
    # Humidity Plot
    plt.subplot(3, 1, 2)
    sns.lineplot(x=dates, y=humidity, marker="s", color="blue")
    plt.xticks(rotation=45)
    plt.title("Humidity Over Time (%)")
    plt.ylabel("Humidity (%)")
    
    # Wind Speed Plot
    plt.subplot(3, 1, 3)
    sns.lineplot(x=dates, y=wind_speeds, marker="d", color="green")
    plt.xticks(rotation=45)
    plt.title("Wind Speed Over Time (m/s)")
    plt.ylabel("Wind Speed (m/s)")
    
    plt.tight_layout()
    plt.show()

# Main Execution
if __name__ == "__main__":
    print(f"\n🌍 Fetching weather data for: {CITY}...")
    weather_data = fetch_weather_data(CITY)
    
    if weather_data:
        print("\n✅ Successfully fetched weather data!")
        dates, temps, hum, wind = extract_weather_info(weather_data)
        plot_weather(dates, temps, hum, wind)
    else:
        print("\n❌ Failed to fetch weather data. Please check your API key and city name.")

    print("\n📌 Script execution completed. Press Enter to exit...")
    input()  # Ensures the window stays open
