import webbrowser
import sys
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import pyttsx3
import requests
from bs4 import BeautifulSoup

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# img = cv2.imread('1.png')
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:

    success, img = cap.read()
    for barcode in decode(img):
        myData = barcode.data.decode('utf-8')
        print(myData)
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, (255, 0, 255), 5)
        pts2 = barcode.rect
        cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,
                    0.9, (255, 0, 255), 2)
        webOpen = webbrowser.open(myData)
        if webOpen:
            reqs = requests.get(myData)
            soup = BeautifulSoup(reqs.text, 'html.parser')
            for title in soup.find_all('title'):
                speak("Opening" + title.get_text())
                sys.exit()

    cv2.imshow('Qr Code Scanner', img)
    cv2.waitKey(1)
