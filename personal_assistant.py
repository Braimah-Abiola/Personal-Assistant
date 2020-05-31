# Required Modules for Personal Assistant
import time
import os
import speech_recognition as sr
from gtts import gTTS
from time import ctime
import requests, json
import sys
import re
import webbrowser
import subprocess
import urllib.request
import urllib.parse
import json
import wikipedia
import random
from time import strftime

# Listen Function
def listen():
    """Takes audio input from the microphone and transcribes it into text"""

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('I am waiting for input ....')
        audio = r.listen(source)
    data = ''

    try:
        data = r.recognize_google(audio)
        print('You said: ' + data)
   
    except sr.UnknownValueError:
        info = ('Didnt understand what you just said')
        respond(info)
    
    except sr.RequestError as e:
        error = ('Request failed; {0}'.format(e))
        respond(error)
    
    return data

# Respond Function
def respond(audioString):
    """Takes string input and converts it to an audio file"""

    print(audioString)
    tts = gTTS(text = audioString, lang = 'en')
    tts.save('response.mp3')
    os.system('mpg321 response.mp3')

def digital_assistant(data):

    # Variables
    help =  """
            You can use these commands and I'll help you out
            1. Open reddit subreddit : Opens the subreddit in default browser.
            2. Open xyz.com : replace xyz with any website name
            3. Send email/email : Follow up questions such as recipient name, content will be asked in order
            4. What is the weather in {cityname} : Tells you the current weather 
            5. Hey Bhyte : Activates the assistant
            6. Play me a video : Plays you a song in VLC media player
            7. Change wallpaper : Changes the desktop wallpaper
            8. News for today : reads top news for today
            9. time : current system time
            10. Top stories from google news (RSS feeds)
            11. Tell me about xyz : Tells you about xyz
            12. Where is {location} : Tells you where the {location} is 
            13. Joke : Cracks a joke 
            """

    master = "I was created by Braimah Abiola"

    # Activation "Hey Bhyte"
    if 'hey bhye' in data:
        listening = True
        respond(help) # Create help variable with help message
    
    # Creator
    if 'who created you' or 'who is your master' in data:
        listening = True
        respond(master)

    # Greetings
    if 'hello' in data:
        listening = True
        day_time = int(strftime('%H'))
        if day_time < 12: # Morning time
            respond("Hello Abiola, Good Morning!")
        elif 12 <= day_time < 18: # Afternoon time
            respond("Hello Abiola, Good Afternoon!")
        else:
            respond("Hello Abiola, Good Evening!") # Night time
    if 'how are you' in data:
        listening = True
        respond('I am well')
    
    # Tell the time
    if 'what time is it' in data:
        listening = True
        respond(f'The time is {ctime()}')

    # General Conversation
    if 'your name' in data:
        listening = True
        respond('my name is Bhyte')

    # Joke
    if 'joke' in data:
        listening = True
        res = requests.get('https://icanhazdadjoke.com/', headers = {"Accept": "application/json"})
        
        if res.status_code == requests.codes.ok:
            respond(str(res.json()['joke']))
        else:
            respond('oops! I ran out of jokes')
    
    # Google Maps Query
    if 'where is' in data: 
        listening = True
        data = data.split('')
        location_url = 'https://www.google.com/maps/place/' + str(data[2])
        respond("Hold on Abiola, I'm going to show you where " + data[2] +  " is.")
        maps_arg = '/usr/bin/open -a "Application/Google Chrome.app" ' + location_url
        os.system(maps_arg)
   
    # Weather Query
    if 'what is the weather in' in data:
        listening = True
        api_key = "YOUR API_KEY" # Add API key here (openweathermap.org)
        weather_url = "http://api.openweathermap.org/data/2.5/weather?"
        data = data.split('')
        location = str(data[5])
        url = weather_url + "appid=" + api_key + "&q=" + location
        js = requests.get(url).json
        
        if js["cod"] != "404":
            weather = js["main"]
            temp = weather["temp"] 
            hum = weather["humidity"]
            desc = js["weather"][0]["description"]
            resp_string = "The temperature in Kelvin is " + str(temp) + "The humidity is " + str(hum) + " and the weather description is " + str(desc)
            respond(resp_string)
        
        else:
            print('City Not Found')

    # Fetch data about topic from wikipedia
    if 'tell me about' in data:
        listening = True
        reg_ex = re.search('tell me about (.*)', data)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                ny = wikipedia.page(topic)
                response(ny.content[:500].encode('utf-8'))
        except Exception as e:
            respond(e)

    # Open subreddit in the browser
    if 'open reddit' in data:
        listening = True
        reg_ex = re.search('open reddit (.*)', data)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        respond('The Reddit content has been opened for you Abiola!')

    # Launch any system application
    if  'launch' in data:
        listening = True
        reg_ex = re.search('launch (.*)', data)
        if reg_ex:
            appname = reg_ex.group(1)
            appname1 = appname + '.app'
            subprocess.Popen(["open", "-n", "/Applications/" + appname1], stdout = subprocess.PIPE)
            response('I have launched the desired application')
    
    # Latest news feeds
    if 'news for today' in data:
        listening = True
        try:
            news_url = 'https://news.google.com/news/rss'
            Client = urlopen(news_url)
            xml_page = Client.read()
            Client.close()
            soup_page = soup(xml_page, 'xml')
            news_list = soup_page.findAll('item')
            for news in news_list[":15"]:
                respond(news.title.text.encode('utf-8'))
        except Exception as e:
            print(e)

    # Open song in VLC

    
    # Change Desktop Wallpaper


    # Search and play YT vid


    # Terminate the digital assistant
    if 'stop listening' in data:
        listening = False
        print('Listening stoped')
        return listening
    return listening

    # Quit the program
    if 'shutdown' in data:
        listening = True
        respond('Bye bye Abiola. Have a nice day')
        sys.exit()

# The main application
time.sleep(2)
respond('Hi Abiola, What can I do for you?')
listening = True

while listening == True:
    time.sleep(2)
    data = listen()
    listening = digital_assistant(data)





    

    
        
