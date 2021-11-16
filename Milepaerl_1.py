# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 08:36:51 2021

@author: Martin
"""

from sense_hat import SenseHat
from time import sleep

senseHat = SenseHat()

# Konstanter
a = -0.0065
R = 287.06
g_0 = 9.81
N = 200

#Variabler
T1 = 16 + 273.15
p_1 = 100000 #Trykket målt ved høyden h_1
h_1 = 0 #Vi gjør målingene relative dersom vi ønsker ved a sette h_1 = 0

def calc_pressure_Pa():
    p = a
    for _ in range (N):
        p += senseHat.pressure
        sleep(0.001)
    return p*100/N #Vi vil ha p i Pa, og multipliserer derfor med 100 etter vi deler på N


def stick_down():
    for e in senseHat.stick.get_events() :

        if e.direction=="down":
            return 1

while True:
    senseHat.show_message ("Venstre: maal - Hoyre: kalibrer - Ned: avbryt",0.05)

    event = senseHat.stick.wait_for_event()

    if event.direction == "left":
        while stick_down() != 1:
            p = calc_pressure_Pa()
            h = (T 1/a) * ( (p/p_1)**(-a*R/g_0) - 1) + h_1
            senseHat.show_message(str(round(h,2) )+ "m" ,0.07)
    if event.direction == "right":
        while stick down()) !=1:
            T_1 = senseHat.temp + 273.15
            p_1 = calc_pressure_Pa()
            senseHat.show_message(str(int (p_1))+" Pa "+str(T_1)+" K", 0.07)


# Ny kodefil

def write_to_log(write_data):
    with open(path, 'a') as f:
        f.write(str(write_data) + '\n')


# Ny kodefil

from sense_hat import SenseHat

senseHat =()
def draw():
    #Tegn hvilken etasje du er på

def calcEtasjer():
    # Konstanter
    a = -0.0065
    R = 287.06
    g_0 = 9.81
    
    # Variabler
    T_1 = 16 + 237.15
    p_1 = #Trykket målt i første etasje
    h_1 = 0 # Starthøyden (første etasje) er definert som 0
    h_e = # Høyden mellom etasjene
    
    p = senseHat.pressure * 100
    
    h = Hypsometrisk ligning
    
    etasje = h/h_e
    toppetasje = 14
    
    if etasje < 0:
        etasje = 0
    elif etasje > toppetasje:
        etasje = toppetasje
    return int(etasje)

while True:
    draw(calcEtasjer())
    
    
    
# Ny kodefil
from sense_hat import SenseHat
from time import sleep, time
from datatime import datatime as dt

senseHat = SenseHat()

# Konstanter
a = -0.0065
R = 287.06
g_0 = 9.81
N = 200
path = "/home/pi/Documents" # Skriv inn din egen mappe du ønsker dataene skal havne i
path = path.rstrip('/') + 'hoydedata.csv' # formaterer path riktig for å få filtypen vi vil ha

# Variabler
T_1 = 16 + 273.25
p_1 = 100000 #trykket målt ved høyden h_1
h_1 = 0 # vi gjør målingene relative dersom vi ønsker ved å sette h_1  = 0

def write_to_log(write_data):
    with open(path, 'a') as f:
        f.write(str(write_data) + '\n')

def calc_pressure_Pa():
    p = 0
    for _ in range (N):
        p += senseHat.pressure
        sleep(1/N)
    return p*100/N #Vi vil ha p i Pa, og multipliserer derfor med 100 etter vi deler på N
    
def stick_down():
    for e in senseHat.stick.get_events() :

        if e.direction=="down":
            return 1

while True:
    senseHat.show_message ("Venstre: maal - Hoyre: kalibrer - Ned: avbryt",0.05)

    event = senseHat.stick.wait_for_event()

    if event.direction == "left":
        start = time()
        
        write_to_log('\n\n### New measurements started at: ' + datatime.now().strftime('%d%m%Y %H:%M:%S' + ' ###\n'))

        while stick_down() !=1:
            p = calc_pressure_Pa()
            h = (T 1/a) * ( (p/p_1)**(-a*R/g_0) - 1) + h_1
            
            now = time() - start
            
            write_to_log(str(now) + ',' + str(p) + ',' + str(h) + ',' + str(senseHat.temp))

            senseHat.show_message(str(round(h,2)) + 'm', 0.03)

    if event.direction == "right":
        while stick down()) !=1:
            T_1 = senseHat.temp + 273.15
            p_1 = calc_pressure_Pa()
            senseHat.show_message(str(int (p_1))+" Pa "+str(eound(T_1))+" K", 0.03)


# Ny kodefil
form sense_hat import SenseHat # Import av SenseHat-funksjonen fra sense_hat modulen

senseHat = SenseHat() # Dannelse av et SenseHat-objekt

# Konstanter
a = -0.0065 # Temperaturgradient (Hvor mange grader kaldere luften blir per meter)
R = 287.06# Den spesifikke gasskonstant (for tørr luft)
g_0 = 9.81 # tyngdeakselerasjonen ved havnivå (omtrent)

# variabler
T_1 = 16 + 273.25 #Temperaturen målt ved h_1 og konvertert til kelvin
p_1 = 100000 #trykket målt ved høyden h_1
h_1 = 50 # Høyden målt ved bakkenivå ved hovedbygget til NTNU er 45 meter. Det er 50 ved realfagsbygget. vi tar 50 fordi vi sannsynligvis er litt over bakken der vi sitter. Sett verdien til null for å gjøre målinger relative til måleområdet

while True:
    p = senseHat.pressure * 100 # Lagrer trykket i Pa i stede for hPa som en variabel
    h = (T 1/a) * ( (p/p_1)**(-a*R/g_0) - 1) + h_1 # Den hypsometriske likningen
    
    senseHat.show_message(str(round(h,2)) + 'm', 0.008) # Skriver resultatet til Sense HAT
