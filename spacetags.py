#!/usr/bin/env python3

from termcolor import colored
from gpiozero import Buzzer, LED
from time import sleep

import RPi.GPIO as GPIO
import SimpleMFRC522
import requests
import sys

GPIO.setmode(GPIO.BCM)

buzzer = Buzzer(21)
led = LED(13)

addr = 'http://192.168.1.16:9002'
reader = SimpleMFRC522.SimpleMFRC522()

def beep():
    buzzer.beep(on_time=0.1, n=1)
    led.blink(on_time=0.5, n=1)

def read():
    print "[spacetags] waiting for tag to read..."
    id, text = reader.read()
    beep()
    print "[spacetags] info: found id " + str(id)
    print "[spacetags] info: " + text
    # cast vote

def write():
    name = raw_input("[spacetags] input tagholder name: ")
    auth = int(raw_input("[spacetags] input user level (helper 1, child 2): "))

    print "[spacetags] info: place tag to write..."
    id, text = reader.write(name + "," + str(auth))
    print id
    beep()

    url = addr + "/register/" + str(id) + "/" + name + "/" + str(auth)
    print(url)
    requests.get(url)

    print "[spacetags] info: written successfully"
    print "[spacetags] info: holder added to database"

def login():
    print("[spacetags] info: entering login mode")
    print("[spacetags] info: return to normal mode using blue tag")

    lastId = -1
    while True:
        id, text = reader.read()
        if id == 994498036507:
            beep()
            break
        elif id != lastId:
            requests.get(addr + "/login/" + str(id))
            print "[spacetags] info: successfully logged in"
            beep()
            lastId = id

def main():
    print "Welcome to spacetags 0.1"
    print "Copyright (c) 2018 Crossroad Nerds"
    print "Type q to quit"

    while True:
        rw = raw_input("(r/w/l/q)? ") 
        if rw == "r":
            read()
        elif rw == "w":
            write()
        elif rw == "l":
            login()
        elif rw == "q":
            sys.exit(0)
        else:
            print("Invalid operation")

if __name__ == "__main__":
    try:
        main()
    finally:
        GPIO.cleanup()
