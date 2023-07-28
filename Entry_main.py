import cv2
import time
from datetime import datetime
import pandas as pd
import pyttsx3
from pyfirmata import Arduino, SERVO
from time import sleep

port = 'COM3'
pin = 9
board = Arduino(port)

board.digital[pin].mode = SERVO

def rotateServo(pin, angle):
    board.digital[pin].write(angle)
    sleep(0.015)

engine = pyttsx3.init()
def speak(text):  #fn to convert text to speech
    engine.say(text)
    engine.runAndWait()
cap = cv2.VideoCapture(0)
# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()
system_ids = ['2020002043','2020002044','2020002045','2020002046','2020002047', '2020002048']
l=[]
x=0
while True:
    _, img = cap.read()
    data, bbox, _ = detector.detectAndDecode(img)
    if data:

        name , system_id = data.split(',')
        name = name.replace('Name ', '')
        system_id = system_id.replace('System ID ', '')
        if system_id in system_ids:
            while x < 3:
                system_ids.remove(system_id)
                print('Valid')
                speak("Valid qr code")
                date = datetime.now().strftime('%d/%m/%Y')
                time1 = datetime.now().strftime('%H:%M:%S')
                l.append((name, system_id, date, time1))
                for i in range(0,90):
                    rotateServo(pin, i)
                time.sleep(2)
                speak("Closing door")
                for i in range(90,1,-1):
                    rotateServo(pin, i)
                break
            else:
                print('No space')
                speak("No space Inside")
            x = x+1
        
        else:
            print('Invalid')
            speak("Invalid qr code. The door will remain closed")
        
        time.sleep(5)
    df = pd.DataFrame(l, columns=['Name', 'System Id', 'Access data', 'Access time'])
    df.to_csv('login_data.csv', index=False)
