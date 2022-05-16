# scorch 3.0.1
# Author: Nick Novacek
import datetime
import math
import random

import obd
import eel
import time

eel.init('web')
lastVoiceLine = time.time()
warm = False
warningOn = False

def resetLastVoiceLine():
    global lastVoiceLine
    lastVoiceLine = time.time()

def toggleWarningMode(toggle):
    global warningOn
    warningOn = toggle
    eel.toggleWarning(toggle)


@eel.expose
def connect_obd():
    # search for OBD port
    print("attempting connection")
    connection = obd.OBD()
    connected = connection.is_connected()
    if not connected:
        print("no connection found, starting test mode...")
        eel.sleep(2)
        eel.updateStatus("Testing")
        fakeui()
    else:
        print("connection found")
        eel.updateStatus(connection.port_name())
        updateUI(connection)


def updateUI(connection):
    welcomePilot()
    codes = connection.query(obd.commands.GET_DTC)
    print(codes)
    global warm;
    global warningOn;
    while True:
        rpm = roundup(connection.query(obd.commands.RPM).value.magnitude)
        throttle = math.ceil(connection.query(obd.commands.THROTTLE_POS).value.magnitude)
        coolant = connection.query(obd.commands.COOLANT_TEMP).value.magnitude
        speed = connection.query(obd.commands.SPEED).value.magnitude
        fuel = math.ceil(connection.query(obd.commands.FUEL_LEVEL).value.magnitude)
        if rpm > 6000:
            shift()
        if rpm > 5700 and not warningOn:
            toggleWarningMode(True)
        elif rpm < 5700 and warningOn:
            toggleWarningMode(False)
        if coolant > 80 and not warm:
            boostReady()
        elif coolant < 75 and rpm > 4000 and not warm:
            damage()
        eel.updateReadout(rpm, throttle, coolant, speed, fuel)
        eel.sleep(0.01)


def welcomePilot():
    line = str(random.randint(1, 4))
    path = "../voices/scorch/" + line + ".mp3"
    print(path)
    resetLastVoiceLine()
    eel.play(path)


def boostReady():
    path = "../voices/scorch/" + "boost" + ".mp3"
    global lastVoiceLine
    global warm
    if time.time() - lastVoiceLine > 3:
        print(path)
        eel.play(path)
        resetLastVoiceLine()
        warm = True


def shift():
    path = "../voices/scorch/" + "eject" + ".mp3"
    global lastVoiceLine
    if time.time() - lastVoiceLine > 1:
        print(path)
        eel.play(path)
        resetLastVoiceLine()


def damage():
    line = str(random.randint(1, 3))
    path = "../voices/scorch/d" + line + ".mp3"
    global lastVoiceLine
    if time.time() - lastVoiceLine > 3:
        print(path)
        eel.play(path)
        resetLastVoiceLine()


def titanDown():
    line = str(random.randint(1, 2))
    path = "../voices/scorch/td" + line + ".mp3"
    print(path)
    eel.play(path)


def fakeui():
    global warningOn
    welcomePilot()
    rpm = 1000
    while rpm < 7000:
        k = random.randint(0, 1)
        if rpm > 5700:
            if not warningOn:
                warningOn = True
                eel.toggleWarning(True)
                eel.toggleCritical(True)
            shift()
        elif 3800 < rpm < 4000:
            boostReady()
        elif 2000 < rpm < 2500:
            damage()
        if rpm < 5700 and warningOn:
            warningOn = False
            eel.toggleWarning(False)
            eel.toggleCritical(False)

        eel.updateReadout(roundup(rpm), 15, 79, math.floor((rpm/7000)*115), 40)
        if k > 0:
            rpm += 50.5
        else:
            rpm = rpm
        eel.sleep(.05)


def roundup(x):
    return int(math.ceil(x / 100.0)) * 100


eel.start('index.html', size=(1200, 460), position=(500, 0))
