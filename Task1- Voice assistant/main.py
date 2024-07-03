import pyttsx3 as p
import speech_recognition as sr
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests

# Initialize text-to-speech engine
engine = p.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech from the microphone
def recognize_speech_from_mic():
    r = sr.Recognizer()
    retry_count = 3
    
    for _ in range(retry_count):
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)  # Reduced from 5 to 1 second
            print("Listening...")
            try:
                audio = r.listen(source, timeout=5)  # Reduced timeout from 10 to 5 seconds
                print("Audio captured, recognizing...")
                text = r.recognize_google(audio)
                print(f"Recognized: {text}")
                return text.lower()  # Convert recognized text to lowercase
            except sr.WaitTimeoutError:
                print("Listening timed out while waiting for phrase to start")
                continue
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                continue
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                continue
    
    print("Failed to recognize speech after retries")
    return None

# Function to get the current time and date
def get_current_time_and_date():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    current_date = now.strftime("%Y-%m-%d")
    return current_time, current_date

# Function to get weather updates
def get_weather(city):
    api_key = "c0de0c8b5b2970b04b88b1d8192e4dd7"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    
    response = requests.get(complete_url)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        weather_desc = data['weather'][0]['description']
        temp = main['temp']
        humidity = main['humidity']
        weather_info = f"The current temperature in {city} is {temp} degrees Celsius with {weather_desc}. The humidity level is {humidity} percent."
        return weather_info
    else:
        return "I couldn't fetch the weather information at the moment. Please try again later."

# Function to interact with Wikipedia using Selenium
class Inflow:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def get_info(self, query):
        self.query = query
        self.driver.get("https://www.wikipedia.org")

        try:
            # Wait until the search input is visible
            search = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.ID, "searchInput"))
            )
            search.click()
            search.send_keys(query)

            # Wait until the search button is clickable
            enter = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="search-form"]/fieldset/button'))
            )
            enter.click()

            # Wait for the page to load
            time.sleep(5)  # Adjust delay as needed

            # Extract and read the first paragraph
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            paragraphs = soup.find_all('p')
            if paragraphs:
                intro_text = paragraphs[0].get_text()
                print(f"Intro: {intro_text}")
                speak(intro_text)
            else:
                speak("I couldn't find any information on this topic.")

        except Exception as e:
            print(f"Error: {e}")

# Main script execution
if __name__ == "__main__":
    speak("Hi there. I am your voice assistant. How are you?")

    while True:
        text = recognize_speech_from_mic()

        if text:
            if "exit" in text or "quit" in text:
                speak("Goodbye!")
                break
            elif "what about you" in text:
                speak("I am having a good day. How can I help you?")
            elif "time" in text or "date" in text:
                current_time, current_date = get_current_time_and_date()
                speak(f"The current time is {current_time} and the date is {current_date}.")
            elif "weather" in text:
                speak("For which city do you need the weather update?")
                city = recognize_speech_from_mic()
                if city:
                    weather_info = get_weather(city)
                    speak(weather_info)
                else:
                    speak("I'm sorry, I couldn't understand the city name. Can you please repeat?")
            elif "information" in text or "info" in text:
                speak("On what topic do you need information?")
                topic = recognize_speech_from_mic()

                if topic:
                    assist = Inflow()
                    assist.get_info(topic)
                else:
                    speak("I'm sorry, I couldn't understand the topic. Can you please repeat?")
            else:
                speak("What can I do for you?")

        else:
            speak("I'm sorry, I couldn't understand you. Can you please repeat?")
