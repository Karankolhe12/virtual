from flask import Flask, render_template, jsonify, request
import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import wikipedia
import os

app = Flask(__name__)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening')
        r.pause_threshold = 0.7
        audio = r.listen(source)
        try:
            print("Recognizing")
            Query = r.recognize_google(audio, language='en-in')
            print("the command is printed=", Query)
        except Exception as e:
            print(e)
            print("Say that again sir")
            return "None"
        return Query

def speak(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(audio)
    engine.runAndWait()

def tellDay():
    day = datetime.datetime.today().weekday() + 1
    Day_dict = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        speak("The day is " + day_of_the_week)
        return day_of_the_week

def tellTime():
    time = str(datetime.datetime.now())
    hour = time[11:13]
    min = time[14:16]
    speak("The time is " + hour + " Hours and " + min + " Minutes")
    return f"{hour} Hours and {min} Minutes"

def wish_mi():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning, Karan")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon, Karan")
    else:
        speak("Good evening, sir")
    speak("My name is Google Assistant. How can I help you?")

def Hello():
    wish_mi()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_assistant')
def start_assistant():
    Hello()
    query = takeCommand().lower()
    response = process_query(query)
    return jsonify(response)

def process_query(query):
    if "open geeksforgeeks" in query:
        speak("Opening GeeksforGeeks")
        response = {"response": "Opened GeeksforGeeks", "url": "https://www.geeksforgeeks.com"}
    elif "open google" in query:
        speak("Opening Google")
        response = {"response": "Opened Google", "url": "https://www.google.com"}
    elif "which day it is" in query:
        day = tellDay()
        response = {"response": f"Today is {day}"}
    elif "tell me the time" in query:
        time = tellTime()
        response = {"response": f"The time is {time}"}
    elif "bye" in query:
        speak("Bye. Check Out GFG for more exciting things")
        response = {"response": "Goodbye"}
    elif "from wikipedia" in query:
        speak("Checking the wikipedia")
        query = query.replace("wikipedia", "")
        result = wikipedia.summary(query, sentences=4)
        speak("According to wikipedia")
        speak(result)
        response = {"response": result}
    elif "tell me your name" in query:
        speak("I am Karan Kolhe. Your desktop Assistant")
        response = {"response": "I am Karan Kolhe. Your desktop Assistant"}
    elif "play game" in query or "game" in query:
        speak("Two games are present in our program. Please choose one: Snake or Ping Pong")
        response = {"response": "Two games are present in our program. Please choose one: Snake or Ping Pong"}
    else:
        response = {"response": "I did not understand that"}
    return response

@app.route('/play_game', methods=['POST'])
def play_game():
    data = request.get_json()
    game_choice = data.get('game_choice')
    
    if game_choice == "snake":
        os.system('python snake.py')
        return jsonify({"response": "Started Snake game"})
    elif game_choice == "ping pong":
        os.system('python ping_pong.py')
        return jsonify({"response": "Started Ping Pong game"})
    else:
        return jsonify({"response": "Invalid game choice"})

if __name__ == '__main__':
    app.run(debug=True)
