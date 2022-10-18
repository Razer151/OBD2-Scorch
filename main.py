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
        print("no connection found...")
        eel.updateStatus("Connection failed")
    else:
        print("connection found")
        eel.updateStatus(connection.port_name())
        updateUI(connection)

@eel.expose
def connect_obd_test():
    # search for OBD port
    print("attempting connection")
    print("starting test mode...")
    eel.sleep(6)
    fakeui()


def updateUI(connection):
    # play welcome voice line
    welcomePilot()
    # this allows the visual effects to play before we start transmitting data
    eel.sleep(2)

    # introduce global voice lines and warning popup status
    global warm
    global warningOn

    # GUI control loop. should get variables and update UI in multiple threads/Multiple API updates,
    # but too lazy to set up
    while True:
        rpm = roundup(connection.query(obd.commands.RPM).value.magnitude)
        throttle = math.ceil(connection.query(obd.commands.THROTTLE_POS).value.magnitude)
        coolant = connection.query(obd.commands.COOLANT_TEMP).value.magnitude
        speed = connection.query(obd.commands.SPEED).value.magnitude
        fuel = math.ceil(connection.query(obd.commands.FUEL_LEVEL).value.magnitude)

        # oil temp not supported on a WRX STI
        # oil = connection.query(obd.commands.OIL_TEMP).value.magnitude

        # calculate which PNG should be displayed on the TAC
        tac1 = "img/" + str(math.floor((rpm / 7000) * 14)) + ".png"
        tac2 = "img/" + str(math.floor((speed / 220) * 14)) + ".png"

        # action flags
        # critical shift warning
        if rpm > 6000:
            shift()
        # warning on
        if rpm > 5700 and not warningOn:
            toggleWarningMode(True)
        # disable warning popup
        elif rpm < 5700 and warningOn:
            toggleWarningMode(False)

        # verbal update that car is up to temp
        if coolant > 80 and not warm:
            boostReady()
        # warning if speeding before up to temp
        elif coolant < 75 and rpm > 4000 and not warm:
            damage()

        # push frontend UI updates
        eel.updateReadout(rpm, throttle, coolant, speed, fuel, tac1, tac2)
        eel.sleep(0.01)


def welcomePilot():
    line = str(random.randint(1, 4))
    path = "../voices/scorch/" + line + ".mp3"
    print(path)
    resetLastVoiceLine()
    eel.play(path)
    eel.removeSplash()


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
    # this allows the visual effects to play before we start transmitting data
    eel.sleep(2)
    rpm = 1000
    gas = 50
    while rpm < 7000:
        k = random.randint(0, 1)
        if rpm > 6000:
            gas = 0
            if not warningOn:
                warningOn = True
                eel.toggleWarning(True)
                eel.toggleCritical(True)
            damage()
        elif 3800 < rpm < 4000:
            boostReady()
            gas = 34
        if rpm < 5700 and warningOn:
            warningOn = False
            eel.toggleWarning(False)
            eel.toggleCritical(False)

        speed = math.floor((rpm/7000)*150)

        tac1 = "img/" + str(math.floor((rpm/7000) * 14)) + ".png"
        tac2 = "img/" + str(math.floor((speed / 150) * 14)) + ".png"

        eel.updateReadout(roundup(rpm), 15, 79, speed, gas, tac1, tac2)
        if k > 0:
            rpm += 150.5
        else:
            rpm = rpm
        eel.sleep(.05)


def roundup(x):
    return int(math.ceil(x / 100.0)) * 100


eel.start('index.html', size=(1280, 460), position=(500, 0))
