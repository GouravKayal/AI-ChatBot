import tkinter as tk
from tkinter import ttk
import threading
import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)  # Adjust speech speed
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Use a female voice

# Initialize main window
win = tk.Tk()
win.geometry("350x450")
win.title("Voice Assistant")

# Global flag to control the assistant loop
assistant_running = False

# Label to show recognized commands
command_label = ttk.Label(win, text="Recognized Command: None", font=("Helvetica", 12))
command_label.pack(pady=10)

# Start Button
start_button = ttk.Button(win, text="Start Voice Assistant")
start_button.pack(pady=20)

# Helper Functions
def talk(text):
    """Convert text to speech and display output."""
    print(f"Assistant: {text}")  # Debugging print
    engine.say(text)
    engine.runAndWait()

def wish_me():
    """Greet the user based on the time."""
    hour = datetime.datetime.now().hour
    if hour < 12:
        talk("Good Morning!")
    elif hour < 18:
        talk("Good Afternoon!")
    else:
        talk("Good Evening!")
    talk("Hi, I am Kinker, your voice assistant. How can I help you?")

def take_command():
    """Listen to user commands and return text."""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            command_label.config(text="Listening...")
            start_button.config(text="Listening...")  # Update UI
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=12)
            print("Recognizing...")
            command = recognizer.recognize_google(audio).lower()
            print(f"Recognized Command: {command}")
            command_label.config(text=f"Recognized: {command}")
            start_button.config(text="Start Voice Assistant")  # Reset UI
            return command
    except sr.WaitTimeoutError:
        print("Listening timeout, retrying...")
        talk("I didn't hear anything. Please try again.")
        return take_command()  # Retry listening
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        talk("Sorry, I could not understand that.")
        return ""
    except sr.RequestError:
        print("Network error.")
        talk("I am unable to access the internet. Please check your connection.")
        return ""
    except Exception as e:
        print(f"Error: {e}")
        talk("An error occurred.")
        return ""

def execute_command(command):
    """Execute the voice command."""
    global assistant_running
    if 'play' in command:
        song = command.replace('play', '').strip()
        talk(f"Playing {song}")
        pywhatkit.playonyt(song)
    elif 'search' in command:
        query = command.replace('search', '').strip()
        talk("Searching Wikipedia...")
        try:
            result = wikipedia.summary(query, sentences=2)
            talk(result)
        except wikipedia.DisambiguationError:
            talk("Multiple results found. Please be more specific.")
        except Exception:
            talk("I couldn't find any information on that.")
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"The current time is {time}.")
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'youtube' in command:
        webbrowser.open("https://youtube.com")
    elif 'google' in command:
        webbrowser.open("https://google.com")
    elif 'stackoverflow' in command:
        webbrowser.open("https://stackoverflow.com")
    elif 'exit' in command:
        talk("Goodbye!")
        assistant_running = False  # Stop the assistant loop
        win.quit()
    else:
        talk("Sorry, I didn't understand that.")

def start_voice_assistant():
    """Continuously listen for voice commands."""
    def assistant_loop():
        global assistant_running
        assistant_running = True
        talk("Voice assistant started.")
        while assistant_running:
            command = take_command()
            if command:
                execute_command(command)
    
    threading.Thread(target=assistant_loop, daemon=True).start()

# Bind button to start function
start_button.config(command=start_voice_assistant)

# GUI Elements
ttk.Label(win, text="Voice Commands", font=("Helvetica", 16)).pack(pady=10)
commands = [
    "1. 'Play [song]' to play music on YouTube.",
    "2. 'Search [topic]' to search on Wikipedia.",
    "3. 'Time' to get the current time.",
    "4. 'Joke' to hear a joke.",
    "5. 'YouTube', 'Google', or 'StackOverflow' to open websites.",
    "6. 'Exit' to exit the program.",
]
for cmd in commands:
    ttk.Label(win, text=cmd).pack(anchor='w', padx=20)

# Start greeting
wish_me()

# Start GUI loop
win.mainloop()