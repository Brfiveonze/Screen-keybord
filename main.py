import cv2
import pynput.keyboard
from cvzone.HandTrackingModule import HandDetector
from time import sleep
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 1200)
cap.set(4, 720)
f_l = 30
keybroad = Controller()

detector = HandDetector(detectionCon=0.8)
butText = [['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
           ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';'],
           ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/']]
bt2 = [['tab', 'SPACE', 'BACK']]
num = [['1', '2', '3'],
       ['4', '5', '6'],
       ['7', '8', '9'],
       ['0']]

board = True

class button():
    def __init__(self, pos, text, size=[50, 50]):
        self.pos = pos
        self.size = size
        self.text = text
    def draw(self, img):
        x, y = self.pos
        w, h = self.size
        cv2.rectangle(img, self.pos, (x+w, y+h), (255, 255, 0), cv2.FILLED)
        cv2.putText(img, self.text, (x+10, y+30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
        return img

buttonList = []
sysl = []
numl = []
for i, l in enumerate(butText):
    for j, key in enumerate(l):
        buttonList.append(button([40 + 60*j, 50 + 60*i], key))
for i, l in enumerate(num):
    for j, key in enumerate(l):
        numl.append(button([40 + 60*j, 50 + 60*i], key))

sysl.append(button([40, 240], 'TAB', size=[80, 50]))
sysl.append(button([180, 240], 'SPACE', size=[120, 50]))
sysl.append(button([320, 240], 'BACK', size=[100, 50]))

def get_bt_event(bt, board, t):
    x, y = bt.pos
    w, h = bt.size
    if x < cursor[0] < x + w and y < cursor[1] < y + h:
        length, info, _ = detector.findDistance(lmList[8][:2], lmList[12][:2], img)
        cv2.rectangle(img, bt.pos, (x + w, y + h), (175, 175, 0), cv2.FILLED)
        cv2.putText(img, bt.text, (x + 10, y + 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
        if length < f_l:

            if t=='kb':
                keybroad.press(bt.text)
            elif t=='cl':
                if bt.text == 'ESC': keybroad.press(pynput.keyboard.Key.tab)
                elif bt.text == 'SPACE': keybroad.press(pynput.keyboard.Key.space)
                elif bt.text == 'BACK': keybroad.press(pynput.keyboard.Key.backspace)

            cv2.rectangle(img, bt.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, bt.text, (x + 10, y + 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
            sleep(0.15)

    return board


while True:
    success, img = cap.read()
    hands, img = detector.findHands(img, flipType=False)
    if board:
        for i in buttonList:
            img = i.draw(img)
        for i in sysl:
            img = i.draw(img)
    else:
        for i in numl:
            img = i.draw(img)

    if hands:
        lmList = hands[0]['lmList']
        cursor = lmList[8]
        if board:
            for bt in buttonList:
                board = get_bt_event(bt, board, 'kb')
            for bt in sysl:
                board = get_bt_event(bt, board, 'cl')
        else:
            for bt in numl:
                board = get_bt_event(bt, board, 'kb')

        switch, _, _ = detector.findDistance(lmList[12][:2], lmList[16][:2], img)
        if switch < f_l:
            keybroad.press(pynput.keyboard.Key.shift)
            keybroad.release(pynput.keyboard.Key.shift)
            sleep(0.15)

        length, info, _ = detector.findDistance(lmList[4][:2], lmList[8][:2], img)
        if length < f_l:
            if board is True:
                board = False
            else:
                board = True
            sleep(0.15)

    cv2.imshow("Image", img)
    cv2.waitKey(1)