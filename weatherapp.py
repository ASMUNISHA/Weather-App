import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests

# Replace with your OpenWeatherMap API key
API_KEY = "a67b7c649f26b83e60f49fbcc3ab4266"

# Global variables for storing weather data, forecast data, and favorite locations
weather_data = None
forecast_data = None
favorite_locations = []

def fetch_weather_data(location):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        print("Error fetching weather data:", str(e))
        return None

def fetch_weather_forecast(location):
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        print("Error fetching weather forecast:", str(e))
        return None

def display_weather_data():
    global weather_data
    if weather_data and 'name' in weather_data and 'sys' in weather_data and 'main' in weather_data and 'weather' in weather_data:
        location_info = f"Weather in {weather_data['name']}, {weather_data['sys']['country']}"
        temperature_info = f"Temperature: {weather_data['main']['temp']}°C"
        humidity_info = f"Humidity: {weather_data['main']['humidity']}%"
        wind_info = f"Wind Speed: {weather_data['wind']['speed']} m/s"
        condition_info = f"Weather Condition: {weather_data['weather'][0]['description']}"
        
        # Update the scrolled text widget
        output_text.delete(1.0, tk.END)  # Clear previous text
        output_text.insert(tk.END, "\n".join([location_info, temperature_info, humidity_info, wind_info, condition_info]))
    else:
        messagebox.showerror("Error", "Error fetching weather data or data structure is incomplete.")

def display_weather_forecast():
    global forecast_data
    if forecast_data and 'list' in forecast_data:
        # Extract and display the forecast data as needed
        forecast_list = forecast_data['list']
        if forecast_list:
            forecast_message = "5-Day Weather Forecast:\n"
            for day in forecast_list[:5]:  # Display forecast for the next 5 days
                temperature = day['main']['temp']
                weather_description = day['weather'][0]['description']
                forecast_message += f"Temperature: {temperature}°C, Weather Condition: {weather_description}\n"
            
            # Update the scrolled text widget
            output_text.delete(1.0, tk.END)  # Clear previous text
            output_text.insert(tk.END, forecast_message)
        else:
            messagebox.showerror("Error", "No forecast data available.")
    else:
        messagebox.showerror("Error", "Error fetching weather forecast or data structure is incomplete.")

def get_weather():
    global weather_data
    location = location_entry.get()
    weather_data = fetch_weather_data(location)
    display_weather_data()

def get_forecast():
    global forecast_data
    location = location_entry.get()
    forecast_data = fetch_weather_forecast(location)
    display_weather_forecast()

def add_to_favorites():
    global favorite_locations
    location = location_entry.get()
    if location not in favorite_locations:
        favorite_locations.append(location)
        messagebox.showinfo("Info", f"{location} added to favorites.")
    else:
        messagebox.showinfo("Info", f"{location} is already in favorites.")

def view_favorites():
    global favorite_locations
    if favorite_locations:
        favorites_message = "\n".join(favorite_locations)
        favorites_window = tk.Toplevel(app)
        favorites_window.title("Favorite Locations")
        favorites_label = scrolledtext.ScrolledText(favorites_window, wrap=tk.WORD, width=40, height=10)
        favorites_label.insert(tk.INSERT, favorites_message)
        favorites_label.pack()
    else:
        messagebox.showinfo("Info", "No favorite locations added yet.")

# Create the main application window
app = tk.Tk()
app.title("Weather App")

# Create and arrange widgets
label = tk.Label(app, text="Enter a location:")
location_entry = tk.Entry(app, width=30)  # Set the width of the input field
get_weather_button = tk.Button(app, text="Get Weather", command=get_weather)
get_forecast_button = tk.Button(app, text="Get Forecast", command=get_forecast)
add_to_favorites_button = tk.Button(app, text="Add to Favorites", command=add_to_favorites)
view_favorites_button = tk.Button(app, text="View Favorites", command=view_favorites)

label.pack(pady=5)  # Add some padding
location_entry.pack(pady=5)  # Add some padding
get_weather_button.pack(pady=5)  # Add some padding
get_forecast_button.pack(pady=5)  # Add some padding
add_to_favorites_button.pack(pady=5)  # Add some padding
view_favorites_button.pack(pady=5)  # Add some padding

# Create a scrolled text widget for output display
output_text = scrolledtext.ScrolledText(app, wrap=tk.WORD, width=40, height=10)
output_text.pack()

# Run the GUI main loop
app.mainloop()