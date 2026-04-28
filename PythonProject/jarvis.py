import re
import requests
import speech_recognition as sr
import webbrowser
import pyautogui
import datetime
import pyttsx3

# ================== CONFIG ==================
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# SAFE MODEL (works for almost all users)
MODEL = "openai/gpt-3.5-turbo"

USER_NAME = "Tirth"

# ================== UTIL ==================
def clean_text(text):
    text = re.sub(r'[^\x00-\x7F]+', '', text)
    text = re.sub(r'\[.*?\]', '', text)
    return text.strip()

# ================== TTS ==================
def speak(text):
    text = clean_text(text)
    if not text:
        return

    engine = pyttsx3.init(driverName="sapi5")
    engine.setProperty("rate", 160)
    engine.setProperty("volume", 1.0)

    voices = engine.getProperty("voices")
    if voices:
        engine.setProperty("voice", voices[0].id)

    engine.say(text)
    engine.runAndWait()
    engine.stop()

# ================== STT ==================
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print(f"🗣 You said: {text}")
        return text
    except:
        return ""

# ================== CHAT ==================
def chat(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "Jarvis Assistant"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": f"You are Jarvis, assistant for {USER_NAME}."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

    except requests.exceptions.HTTPError:
        return f"API ERROR: {r.text}"
    except Exception as e:
        return f"ERROR: {e}"

# ================== TOOLS ==================
def tool_open_url(site):
    if not site.startswith("http"):
        site = "https://" + site
    webbrowser.open(site)
    return f"Opening {site}"

def tool_time():
    return "The time is " + datetime.datetime.now().strftime("%H:%M:%S")

# ================== MAIN ==================
print("\n=== JARVIS RUNNING (FULLY WORKING) ===")
speak(f"Hello {USER_NAME}. Jarvis is now online.")

while True:
    try:
        user = listen()
        if not user:
            continue

        u = user.lower()

        if u.startswith("open "):
            reply = tool_open_url(user[5:])
        elif "time" in u:
            reply = tool_time()
        else:
            reply = chat(user)

        print(f"🤖 Jarvis: {reply}")
        speak(reply)

    except KeyboardInterrupt:
        speak("Goodbye. Have a nice day.")
        break
