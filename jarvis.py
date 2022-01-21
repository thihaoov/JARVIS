import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia as wiki
import smtplib
import webbrowser as wb
import os
import pyautogui
import psutil
import pyjokes

engine = pyttsx3.init()

# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[0].id)

# newVoiceRate = 200
# engine.setProperty('rate', newVoiceRate)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time():
    time = datetime.datetime.now().strftime("%I:%H:%S")
    speak("Current time is")
    speak(time)

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    speak("the current date is")
    speak(day)
    speak(month)
    speak(year)

def wishme():
    speak("Welcome back sir!")
    time()
    date()
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour <= 12:
        greet = "Good morning"
    elif hour >= 12 and hour <= 18:
        greet = "good afternoon"
    elif hour >= 18 and hour <= 24:
        greet = "good evening"
    else: greet = "Good night"
    speak(greet)
    speak("Jarvis at your service. How I can help you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening......")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try: 
        print("Recognizing......")
        query = r.recognize_google(audio, 'en-US')
        print(query)
    except Exception as e:
        print(e)
        speak("Say that again please....")
        # takeCommand()
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls() # check connection of server
    server.login("test@gmail.com", "123test") # email and password
    server.sendmail("text@gamil.com", to, content)
    server.close()

def screenshot():
    img = pyautogui.screenshot()
    img.save("/home/thiha/Pictures/ss.png")

def cpu():
    usage = str(psutil.cpu_percent)
    speak("CPU is at "+ usage)

    battery = psutil.sensors_battery
    speak("battery is at"+ str(battery.percent) )

def jokes():
    speak(pyjokes.get_joke())




def main():
    wishme()

    while True:
        query = takeCommand().lower()
        print(query)

        if "time" in query:
            time()

        elif "date" in query:
            date()

        elif "offline" in query:
            quit()

        elif "wikipedia" in query:
            speak("Searching....")
            query = query.replace("wikipedia", "")
            result = wiki.summary(query, sentence = 2)
            speak(result)

        elif "send email" in query:
            try:
                speak("What should I send?")
                content = takeCommand()
                to = "xyz@gmail.com"
                # sendEmail(to, content)
                speak(content)
            except Exception as e:
                speak(e)
                speak("Unable to send the mail")

        elif "search in chrome" in query:
            speak("What should I search?")
            chromePath = "/usr/bin/chromium-browser %s"
            search = takeCommand().lower()
            wb.get(chromePath).open_new_tab(search+".com")

        elif "logout" in query:
            os.system("shutdown - 1")

        elif "shutdown" in query:
            os.system("shutdown /s /t 1")

        elif "restart" in query:
            os.system("shutdown /r /t 1")

        elif "play song" in query:
            songs_dir = "/home/thiha/Music/Songs/"
            songs = os.listdir(songs_dir)
            os.startfile(os.path.join(songs_dir, songs[0]))

        elif "remember that" in query:
            speak("What should I Remember?")
            data = takeCommand()
            speak("You said me to remember" + data)
            remember = open("data.txt", "w")
            remember.write(data)
            remember.close()

        elif "do you know anything" in query:
            remember = open("data.txt","r")
            speak("you said me to remember that "+ remember.read())

        elif "screenshot" in query:
            screenshot()
            speak("Done")

        elif "cpu" in query:
            cpu()

        elif "joke" in query:
            jokes()
        


if __name__=="__main__":
    main()