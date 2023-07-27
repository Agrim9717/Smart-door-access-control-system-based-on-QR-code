import cv2
import csv
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
detector = cv2.QRCodeDetector()
l=[]
students=[]

with open("login_data.csv","r") as file:
    reader=csv.reader(file)
    for row in reader:
        students.append((row[1]))

while True:
    _, img = cap.read()
    data, bbox, _ = detector.detectAndDecode(img)
    if data:


        name , system_id = data.split(',')
        name = name.replace('Name ', '')
        system_id = system_id.replace('System ID ', '')
    

        if system_id in students:
            students.remove(system_id)
            print('Valid')
            speak("Valid qr code")
            date1 = datetime.now().strftime('%d/%m/%Y')
            time2 = datetime.now().strftime('%H:%M:%S')
            l.append((name, system_id, date1, time2))
            for i in range(0,90):
                rotateServo(pin, i)
            time.sleep(2)
            speak("Closing door")
            for i in range(90,1,-1):
                rotateServo(pin, i)

        else:
            print('Invalid')
            speak("Invalid qr code. The door will remain closed")
        time.sleep(5)
    df = pd.DataFrame(l, columns=['Name', 'System Id', 'Exit date', 'Exit time'])
    df.to_csv('final_data.csv', index=False)
