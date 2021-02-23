import socket
# import os
import subprocess
import re
import json as j
import pyautogui
from playsound import playsound
from emoji import demojize

li = j.load(open('twitchinfo.json', 'r'))
pyautogui.FAILSAFE = False

s = socket.socket()
s.connect((li['server'], li['port']))

s.send(f"PASS {li['token']}\n".encode('utf-8'))
s.send(f"NICK {li['nickname']}\n".encode('utf-8'))
s.send(f"JOIN {li['channel']}\n".encode('utf-8'))

def moveMouse(x, y): pyautogui.moveTo(x, y, duration=0.2)

while True:
    resp = s.recv(2048).decode('utf-8')

    if resp.startswith('PING'):
        s.send("PONG\n".encode('utf-8'))
    
    elif len(resp) > 0:

        dmRESP = demojize(resp)
        
        user = dmRESP.strip().split(":")
        msg = re.sub(':(.*)\\!.*@.*\\.tmi\\.twitch\\.tv PRIVMSG #(.*) :', "", dmRESP)
        print(f'{user[1].split("!")[0]} sent command {msg}')

        if 'ipconfig' in msg:
            print("NO!")
            playsound('noo.mp3')
        
        elif 'cat twitchinfo.json' in msg or 'notepad twitchinfo.json' in msg:
            print("NO!")
            playsound('no.mp3')


        elif msg.startswith('!move') or msg.startswith('!movemouse'):
            try:
                moveX = msg.split("x")
                moveY = msg.split("y")
                print("Move cursor!")
                print(moveX[1].split('y')[0])
                print(moveY[1])
                
                moveMouse(x=int(moveX[1].split('y')[0]), y=int(moveY[1]))
            except Exception: pass

        elif msg.startswith('!click') or msg.startswith('m1'):
            try:
                pyautogui.click()
            except Exception: pass
        elif msg.startswith('!rightclick') or msg.startswith('m2'):
            try:
                pyautogui.click(button='right')
            except Exception: pass
        elif msg.startswith('!doubleclick'):
            try:
                pyautogui.click(clicks=2)
            except Exception: pass
        elif msg.startswith('!rightdoubleclick'):
            try:
                pyautogui.click(button='right', clicks=2)
            except Exception: pass

        elif msg.startswith('!drag'):
            try:
                moveX = msg.split("x")
                moveY = msg.split("y")
                print("Drag!")
                print(moveX[1].split('y')[0])
                print(moveY[1])

                pyautogui.dragTo(x=moveX[1].split('y')[0], y=moveY[1], button='left')

            except Exception: pass

        elif msg.startswith('!scroll'):
            try:
                scrollAmount = msg.split('!scroll')[1]
                pyautogui.scroll(int(scrollAmount))
            except Exception: pass

        elif msg.startswith('!keypress'):
            presstable = msg.split(" ")
            print(type(presstable))
            print(presstable)

        elif msg.startswith('!type'):
            text = msg.split('!type')[1]

            if text in li['dontTypeThese']:
                playsound("noo.mp3")
            else:
                pyautogui.typewrite(text, interval=0.05)

        elif msg.startswith('!clear'):
            pyautogui.hotkey('ctrl', 'a', 'backspace')

        else:
            try:
                subprocess.Popen(f'{msg}', shell=True)
            except Exception: pass
