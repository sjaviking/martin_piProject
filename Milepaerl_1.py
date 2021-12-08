# -*- coding: utf-8 -*-

# henter inn ulike bibliotek for bruk i koden
from sense_hat import SenseHat
from time import sleep
from datatime import datatime as dt


senseHat = SenseHat()  # Dannelse av et SenseHat-objekt

# Konstanter
a = -0.0065 # Temperaturgradient (Hvor mange grader kaldere luften blir per meter)
R = 287.06# Den spesifikke gasskonstant (for tørr luft)
g_0 = 9.81 # tyngdeakselerasjonen ved havnivå (omtrent)
N = 200
path = "/home/pi/Documents" # path vi ønsker at filen skal havne på
path = path.rstrip('/') + 'hoydedata.csv' # formaterer path riktig for å få filtypen vi vil ha


#Variabler
T1 = 16 + 273.15 #Temperaturen målt ved h_1 og konvertert til kelvin
p_1 = 100000 #Trykket målt ved høyden h_1
h_1 = 0 #Vi gjør målingene relative
''' Høyden målt ved bakkenivå ved hovedbygget til NTNU er 45 meter. Det er 50 ved realfagsbygget. 
Vi tar 50 fordi vi sannsynligvis er litt over bakken der vi sitter. 
Sett verdien til null for å gjøre målinger relative til måleområdet
'''

# funksjon som kalkulerer trykk og returnerer resultat i Pa
def calc_pressure_Pa():
    p = a  # trekker fra temperaturgradient - kan settes til 0
    for _ in range (N):  # range satt til N = 200
        p += senseHat.pressure  # legger til trykket på variabel p for hver kjøring av løkke
        sleep(0.001)  # 0.001s delay før progarm kjører videre
    return p*100/N #Vi vil ha p i Pa, og multipliserer derfor med 100 etter vi deler på N


# Funksjon ved event stick_down
def stick_down():
    for e in senseHat.stick.get_events() :

        if e.direction=="down":
            return 1
     
# Funksjon for skriving av data til log-fil
def write_to_log(write_data):
    # Bruker with open for automatisk lukking, settes til a for append
    with open(path, 'a') as f:
        # skriver write_data variabel til log-fil og slutter med linjeskift
        f.write(str(write_data) + '\n')
        
'''
# Tegning av etasje i egen funskjon
def draw(etasje):
    message = 'etg ' +  etasje  # lager string av etasje
     senseHat.show_message (message,0.05)  # printer string på HAT med speed 0.5
     
# funksjon som kalkulerer etasjer     
def calcEtasjer():
    h_e = 3 # Høyden mellom etasjene, satt til 3m da vi ikke vet nøyaktig
    p_e = senseHat.pressure * 100 # live trykke variabel
    
    h_l = (T_1/a) * ( (p_e/p_1)**(-a*R/g_0) - 1) + h_1 # beregner høyde med hypsometrisk ligning
   
    etasje = h_l/h_e  # Kalkulerer etasje ved å dele høyde i moh på høyde til etasje
    toppetasje = 14  # Satt maks antall etasjer i forhold til sentralbygget på Gløs
    
    if etasje < 0:
        etasje = 0
    elif etasje > toppetasje:
        etasje = toppetasje      
  '''     
        
while True:
    # Show message viser bruker hvordan PI styres
    senseHat.show_message ("Venstre: maal - Hoyre: kalibrer - Ned: avbryt",0.05)

    event = senseHat.stick.wait_for_event() # forkorting av stick event

    if event.direction == "left":  # hvis stikke på Hat trykkes mot venstre
        start = time() # Finner startiden på logging
        # Skriver over skrift til logg for å markere ny måling
        write_to_log('\n\n### New measurements started at: ' + datatime.now().strftime('%d%m%Y %H:%M:%S' + ' ###\n'))
        
        while stick_down() != 1:  # kjører frem til stikke trykkes ned
            p = calc_pressure_Pa() # henter kalkulert trykk
            h = (T_1/a) * ( (p/p_1)**(-a*R/g_0) - 1) + h_1 # beregner høyde med hypsometrisk ligning
            # finner tiden ved måling med å ta tiden minus starttid. Resulterer i tid etter start måling
            now = time() - start
            
            # Skriver data hentet til log med tidsstempel.
            write_to_log(str(now) + ',' + str(p) + ',' + str(h) + ',' + str(senseHat.temp))
            
            # Viser målt høyde avrundet i display med speed 0.03 (kommenteres ut hvis etasjemåling)
            senseHat.show_message(str(round(h,2) )+ "m" ,0.03)
            '''
            draw(calcEtasjer())  # Printer etasjevisning (kan kommenteres ut hvis ikke ønsket)  
            '''
    
    if event.direction == "right":  # Hvis stikke trykkes mot høyre
        while stick down()) !=1: # Kjøerer frem til stikke trykkes ned
            T_1 = senseHat.temp + 273.15 # finner temperatur og gjør om til grader celcius
            p_1 = calc_pressure_Pa() # Finner kalkulert trykk
             # viser målt høyde avrundet og temp i display med hastighet 0.03
            senseHat.show_message(str(int (p_1))+" Pa "+str(round(T_1))+" K", 0.03)          
