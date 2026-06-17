import requests
import speech_recognition as sr
import pyttsx3
import webbrowser
import subprocess
import datetime
import psutil
import os

# -------------------------
# DeepSeek API Key
# -------------------------
DEEPSEEK_API_KEY = "YOUR_DEEPSEEK_API_KEY"

# -------------------------
# Voice Engine
# -------------------------
engine = pyttsx3.init()
engine.setProperty('rate', 180)

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# -------------------------
# Speech Recognition
# -------------------------
def listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)

        try:
            audio = r.listen(source, timeout=5)
            command = r.recognize_google(audio)

            print("You:", command)
            return command.lower()

        except:
            return ""

# -------------------------
# DeepSeek Chat
# -------------------------
def ask_deepseek(prompt):

    url = "https://api.deepseek.com/chat/completions"

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content":
                "You are Jarvis, an AI desktop assistant. "
                "You can speak English, Hindi, Chinese, Russian, Japanese and Spanish."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=data
        )

        answer = response.json()['choices'][0]['message']['content']

        return answer

    except Exception as e:
        return str(e)

# -------------------------
# PC Commands
# -------------------------
def execute(command):

    if "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
        return True

    elif "open google" in command:
        webbrowser.open("https://google.com")
        speak("Opening Google")
        return True

    elif "open notepad" in command:
        subprocess.Popen("notepad.exe")
        speak("Opening Notepad")
        return True

    elif "open calculator" in command:
        subprocess.Popen("calc.exe")
        speak("Opening Calculator")
        return True

    elif "time" in command:

        now = datetime.datetime.now().strftime("%I:%M %p")

        speak(f"Current time is {now}")
        return True

    elif "cpu" in command:

        cpu = psutil.cpu_percent()

        speak(f"CPU usage is {cpu} percent")
        return True

    elif "memory" in command:

        mem = psutil.virtual_memory().percent

        speak(f"Memory usage is {mem} percent")
        return True

    elif "shutdown computer" in command:

        speak("Shutdown cancelled for safety.")
        return True

    return False

# -------------------------
# Main Loop
# -------------------------
def main():

    speak("Hello. I am Jarvis.")

    while True:

        command = listen()

        if not command:
            continue

        if "exit" in command:
            speak("Goodbye")
            break

        executed = execute(command)

        if not executed:

            answer = ask_deepseek(command)

            print("\n")
            print(answer)
            print("\n")

            speak(answer)

if __name__ == "__main__":
    main()