import random
import time
import os
import subprocess
import sys
import threading

from sense_hat import SenseHat
sense = SenseHat()

host_multiplayer = len(sys.argv) == 0 and sys.argv[1] == "host"

if host_multiplayer:
    from flask_socketio import emit

"""
En liten visualisering på hvordan BUFFER fungerer
Det er en liste, delt inn i 8 lister, alle med 8 verdier hver
Hver liste fungerer som en y verdi, og hvert element i listen fungerer som en x verdi
Ser litt sånn her ut:

BUFFER:
--                                           --
| y_0[x_0, x_1, x_2, x_3, x_4, x_5, x_6, x_7] |
| y_1[x_0, x_1, x_2, x_3, x_4, x_5, x_6, x_7] |
| y_2[x_0, x_1, x_2, x_3, x_4, x_5, x_6, x_7] |
| ... -->                                     |
--                                           --
Eksempel:
Med fuel ønsker vi bare å bruke x_7 pixler
Derfor henter vi disse pixlene med f.eks en for/while løkke
hvor y varierer, mens x er konstant
i = 0
while i < 8:
    x_kordinater = BUFFER[i][7]
    i += 1
"""

ROWS = 8
COLS = 8

FPS = 20
FRAME_DURATION = 1 / FPS

MAX_FUEL = COLS
FUEL_SPAWN_CHANCE = 2
FUEL_DECREASE = 23
FUEL_FREQUENCY = 8
FUEL_SLOWNESS = 3

GATE_FREQUENCY = 8
GATE_SLOWNESS = 4

CAR_Y_POS = 6
DEFAULT_CAR_X_POS = 4

CAR_COLOR = (255, 255, 255)
FUEL_COLOR = (120, 255, 0)
GATE_COLOR = (255, 0, 0)
NOCOLOR = (0, 0, 0)

THEME_SONG =         "sound/midjo_gp_main.wav"
CRASH_SOUND =        "sound/crash_midjo_gp.wav"
PICKUP_FUEL_SOUND =  "sound/fuel_midjo_gp.wav"
LOW_FUEL_SOUND =     "sound/low_fuel_midjo_gp.wav"
SCORE_SOUND =        "sound/point_midjo_gp.wav"
GAME_OVER_SOUND =    "sound/game_over_midjo_gp.wav"
ENGINE_SOUND =       "sound/engine_sound.wav"
#TODO: Finn en ordentlig måte å spille av lyd på.
#      Akkurat nå fortsetter lyden å spille etter python-programmet har stoppa.

class Car:
    def __init__(self, color):
        self.x = DEFAULT_CAR_X_POS
        self.y = 0
        self.color = color
        self.fuel = MAX_FUEL
        
    def get_position(self):
        return self.x
        
    def get_color(self):
        return self.color
    
    def set_color(self, color):
        self.color = color
        
    def move_to(self, pos):
        self.x = restrict_value(pos, 0, COLS - 1)
    
    def move(self, change):
        self.move_car_to(self.x + change)
        
    def change_fuel(self, change):
        self.set_fuel(self.fuel + change)
    
    def set_fuel(self, fuel):
        self.fuel = restrict_value(fuel, 0, MAX_FUEL)
    
    def get_fuel(self):
        return self.fuel
    
    def move_left(self):
        self.move_car(-1)
        
    def move_right(self):
        self.move_car(1)
        
    def reset(self):
        self.set_fuel(MAX_FUEL)
        
    
class Player:
    def __init__(self, car, sid):
        self.car = car
        self.total_score = 0
        self.score = 0
        self.sid = sid
    
    def get_sid(self):
        return self.sid
    
    def get_car(self):
        return self.car

    def set_score(self, score):
        self.score = score
        
    def set_total_score(self, total_score):
        self.total_score = total_score
        
    def change_score(self, change):
        self.score += change
        
    def change_total_score(self, change):
        self.total_score += change
        
    def get_score(self):
        return self.score
    
    def get_total_score(self):
        return self.total_score
    
    def is_dead(self):
        return self.get_car().get_fuel() == 0
    
    def is_low_fuel_alarm(self):
        return self.is_low_fuel_alarm

    def set_low_fuel_alarm(self, is_low_fuel_alarm):
        self.is_low_fuel_alarm = is_low_fuel_alarm
        
    def reset(self):
        #Reset score, total_score og fuel
        self.set_score(0)
        self.set_total_score(0)
        self.get_car().reset()

# sid -> Player()
players = dict()
players['pi'] = Player(Car(CAR_COLOR), 'pi')

def get_player(sid):
    return players[sid]

def get_living_players():
    return [player for player in players.values() if not player.is_dead()]

def get_local_player():
    return get_player('pi')

def emit_websocket(player, event, data):
    if host_multiplayer and (player is not get_local_player()):
        emit(event, data, to=player.get_sid())

def restrict_value(value, min_value, max_value):
    return max(min_value, min(max_value, value))

def get_gate_pos(gate_width):
    """Returner x-posisjon til gate som du skal treffe med bilen"""
    #Bredden til banen er COLS minus bredden til fuel-baren
    game_width = COLS - 2
    right_pole_max = game_width - gate_width

    gate_pos = random.randint(0, right_pole_max)
    return gate_pos


def get_fuel_pos():
    """Returnerer x-posisjon til fuel som du skal treffe"""
    fuel_pos = random.randint(0, 6)
    return fuel_pos


def draw_fuel(mod_buffer, x):
    """Mellom 0 og 8, 0 er null fuel, 8 er max fuel
    funksjonen tar inn buffer-variabel og x (fuel)
    returnerer en modifisert buffer"""
    x_pos_fuelGauge_lokal = 7 #sier bare hvilken kolonne du ønsker
    i = 0
    u = 0
    if x < 0:
        return mod_buffer
    if x > 8:
        x = 8
    #Dette skriver om på buffer, og lager en kollonne med fuel
    while i < x:
        mod_buffer[i][x_pos_fuelGauge_lokal] = (255 - u, u, 0)
        i += 1
        u += 36
    u = 0 #bruker u som nullverdi for neste whileløkke
        #og beholder i, ettersom i er y verdi for sorte pixler
    resterende_pixler = 8 - x
    while u < resterende_pixler:
        mod_buffer[i][x_pos_fuelGauge_lokal] = NOCOLOR
        u += 1
        i += 1
    return mod_buffer #returnerer en modifisert buffer


def draw_score_bar(buffer, score):
    """Tegner score på den øverste baren"""
    
    SCORE_BAR_COLOR = (34, 34, 34)
    SCORE_POINTS_COLOR = (133, 255, 80)
    BAR_Y_POS = 0
    BAR_LENGTH = 7

    #Får "score" over til binærtall eks: 19 --> 10011
    binary_str_score = str(bin(score))[2:]

    #Passer på at "binary_str_score" er BAR_LENGTH lang
    leading_zeros = "0" * (BAR_LENGTH - len(binary_str_score)) 
    binary_str_score = leading_zeros + binary_str_score

    print("score: ", score, " bin: ", binary_str_score)
    
    #Legger til bakgrunnen
    for x in range(BAR_LENGTH):
        buffer[BAR_Y_POS][x] = SCORE_BAR_COLOR

    #Legger til prikker for score
    for x_pos, char in enumerate(binary_str_score):
        if char == "1":
            buffer[BAR_Y_POS][x_pos] = SCORE_POINTS_COLOR

    #Returnerer den modifiserte bufferen
    return buffer


def draw_sad_midjo(animation_length):
    """Tegner en animasjon av Midjo som gråter"""

    midjo_portrait = [
        (255,	255,	255),
        (255,	255,	255),
        (254,	254,	254),
        (201,	195,	193),
        (166,	151,	148),
        (203,	194,	193),
        (252,	251,	251),
        (255,	255,	255),
        (255,	255,	255),
        (255,	255,	255),
        (210,	206,	204),
        (151,	107,	97),
        (205,	154,	146),
        (218,	169,	162),
        (209,	193,	190),
        (255,	255,	255),
        (255,	255,	255),
        (255,	255,	255),
        (178,	169,	166),
        (175,	122,	111),
        (236,	185,	177),
        (242,	197,	191),
        (215,	185,	178),
        (255,	255,	255),
        (255,	255,	255),
        (255,	255,	255),
        (144,	122,	115),
        (157,	114,	106),
        (210,	157,	145),
        (214,	163,	152),
        (217,	180,	172),
        (255,	255,	255),
        (255,	255,	255),
        (255,	255,	255),
        (171,	158,	155),
        (201,	136,	127),
        (194,	135,	128),
        (229,	167,	160),
        (233,	199,	192),
        (255,	255,	255),
        (255,	255,	255),
        (251,	251,	250),
        (141,	132,	132),
        (155,	103,	93),
        (152,	97, 	93),
        (184,	124,	114),
        (236,	223,	221),
        (255,	255,	255),
        (210,	205,	201),
        (117,	102,	97),
        (43, 	36,		44),
        (130,	92,		81),
        (170,	115,	107),
        (180,	132,	125),
        (199,	188,	183),
        (244,	242,	240),
        (107,	78,		64),
        (97, 	68,		55),
        (63, 	42,		33),
        (46, 	34,		37),
        (106,	80,		77),
        (78,    71,     90),
        (109,	78, 	64),
        (118,	87, 	72)]

    buffer = midjo_portrait
    tear_color = (0, 0, 80)
          
    sense.set_pixels(midjo_portrait)
    for frame in range(animation_length):
        #tear 1
        for i in range(3):
            sense.set_pixel(3, 3+i, tear_color)
            time.sleep(0.1)
        
        #tear 2
        for j in range(3):
            sense.set_pixel(5, 3+j, tear_color)
            time.sleep(0.1)
        sense.set_pixels(midjo_portrait)


def intro_graphic():
    TheGame = 'Midjo GP'  # Spillets navn
    TheGame_odd = TheGame[::2] # Skiller ut odde karakterer
    TheGame_even = TheGame[1::2] # Skiller ut jevne karakterer

    g = (96, 125, 139)  # Gråfarge til bakgrunn
    w = (10, 10, 10)   # Hvit farge til bokstav
    r = (244, 66, 54)  # Rød farge til bokstav

    Background = []  # Tom liste som fylles av forløkke for bakgrunn
    # For løkke for å lage bakgrunn
    for color in range(0,64): # range 64 grunnet 64 pixler
        Background.append(g)


    # Første bilde med 1 bokstav
    def Midjo(g, w):
        drawing = [w, g, g, g, w, g, g, g,
                 w, w, g, w, w, g, g, g,
                 w, g, w, g, w, g, g, g,
                 w, g, g, g, w, g, g, g,
                 w, g, g, g, g, g, g, g,
                 g, g, g, g, g, g, g, g,
                 g, g, g, g, g, g, g, g,
                 g, g, g, g, g, g, g, g,]
        return drawing

    # Andre bilde med 2 bosktaver
    def Grand(g, r, w):
        drawing = [w, g, g, g, w, g, g, g,
                w, w, g, w, w, g, g, g,
                w, g, w, g, w, g, g, g,
                w, g, g, g, w, g, g, g,
                w, r, r, g, g, g, g, g,
                r, g, g, g, g, g, g, g,
                r, g, r, r, g, g, g, g,
                g, r, r, g, g, g, g, g,]
        return drawing

    # Tredje bilde med 3 bokstaver
    def Prix(g, r, w):
        drawing = [w, g, g, g, w, g, g, g,
                w, w, g, w, w, g, g, g,
                w, g, w, g, w, g, g, g,
                w, g, g, g, w, g, g, g,
                w, r, r, g, g, r, r, g,
                r, g, g, g, g, r, g, r,
                r, g, r, r, g, r, r, g,
                g, r, r, g, g, r, g, g,]
        return drawing

    # Setter først bakgrunn
    sense.set_pixels(Background)
    time.sleep(1) # Delay på 1s
    # Setter så M i bildet
    sense.set_pixels(Midjo(g, w))
    time.sleep(1) # Delay på 1s
    sense.set_pixels(Grand(g, r, w))
    # Setter så G i bildet
    time.sleep(1) # Delay på 1s
    # Setter så siste bokstav i bildet
    sense.set_pixels(Prix(g, r, w))
    time.sleep(1) # Delay på 1s
    
    # Finner string som er lengst av odd og even for å sette lengde på for-løkke
    if len(TheGame_odd) > len(TheGame_even):
        StrLenght = len(TheGame_odd)
    else: StrLenght = len(TheGame_even)

    # for løkke for å stave spillnavn meg generel lengde på spillets navn.
    # Bruker if setning, for å unngå lengde error på stringer 
    for character in range(0, StrLenght): # Løkken kjører like lenge som spillets navn.
        if StrLenght >= len(TheGame_odd): # Sjekker lengde opp mot telleverk for å ikke få index error 
            sense.show_letter(TheGame_odd[character], text_colour=[255, 255, 255], back_colour=[0, 0 ,0])
            time.sleep(0.4)  # Delay på 0.4s
        if StrLenght >= len(TheGame_even): # Sjekker lengde opp mot telleverk for å ikke få index error
            # Printer hver partall bokstav med hvit bakrunn og sort tekst
            sense.show_letter(TheGame_even[character], text_colour=[0,0,0], back_colour=[255, 255, 255])
            time.sleep(0.4)  # Delay på 0.4s
    sense.clear()  # Tømmer led-matrise


def next_level_graphic(level):
    #Spiller av motorlyd
    engine_sound = subprocess.Popen(["aplay", ENGINE_SOUND])

    #Farger
    W = (255, 255, 255)
    B = (0, 0, 0)
    r = (255, 0, 0)
    
    # Tegner speedometeret
    speedometer = [
        B, B, W, W, W, W, B, B,
        B, W, B, B, B, B, W, B,
        W, B, B, B, B, B, B, W,
        W, B, B, B, B, B, B, W,
        W, B, B, B, B, B, B, W,
        W, B, B, B, B, B, B, W,
        B, W, B, B, B, B, W, r,
        B, B, W, B, B, W, r, r,
        ]
  
    # Definerer arugmentene, og sier rangen på index
    def print_speedometer(message, maxRange):
        sense.show_message(message, speed, text_colour=W, back_colour=B)
        for index in range(0, maxRange):
            plot_ranges(index)
    
    def plot_ranges(index):
        # Lister over alle speedometer nivåene fra 0 til 6
        color_ranges = [
            [(44, 45), (51, 52)],
            [(41, 45)],
            [(44, 45), (35, 36), (26, 27), (17, 18)],
            [(44, 45), (36, 37), (28, 29), (20, 21), (12, 13)],
            [(43, 44), (36, 37), (29, 30), (22, 23)],
            [(43, 47)],
            [(43, 44), (52, 53)],
            ]
    
        # Bytter ut pixlene i speedometeret med, 
        # hvilket speedometer nivå som vises
        pixels = [v for v in speedometer]
        for (start, end) in color_ranges[index]:
            for i in range(start, end):
                pixels[i] = r
        
        # Clearer og printer ut speedometeret for hvert nivå,
        # helt til den når siste nivå for angitt level 
        sense.clear()
        sense.set_pixels(pixels)
        time.sleep(0.4)
  
    # Hastigheten på teksten som printes        
    speed = 0.04
      
    # Sier hvilken speedometer nivåer som skal printes,
    # avhengig av hvilket level vi befinner oss i
    levelPixelRange = {
        1: 3,
        2: 5,
        3: 7,
        }
      
    # Printer ut meldingen av hvilket level vi befinner oss i, 
    # og alle nivåene på speedometeret
    print_speedometer("Lvl " + str(level) , levelPixelRange[level])
        
    time.sleep(1)
    

def game_over_graphic(score):
    StrScore = str(score)  # egen variabel med score som string
    g = (96, 125, 139)  # Gråfarge til bakgrunn
    b = (0, 0, 0,) # Sort bakgrunn
    pink = (241, 0, 245)  # Rosa hodeskalle
    yellow = (247, 247, 0) # Rød hodeskalle

    # b er bakgrunn og s er skallen. tegnet opp:
    def skull(b , s):  # Bruker definisjon for å kunne ha forskjellige farger
        drawing = [b, s, s, s, s, s, b, b,
                s, s, s, s, s, s, s, b,
                s, b, b, s, b, b, s, b,
                s, b, b, s, b, b, s, b,
                s, s, s, b, s, s, s, b,
                b, s, s, s, s, s, b, b,
                b, s, b, s, b, s, b, b,
                b, b, b, b, b, b, b, b,]
        return drawing

    # Bruker for-løkke for å endre farge på hodeskalle
    for color_change in range (0, 5):   # Satt til å være hver farge 5 ganger
        sense.set_pixels(skull(b, pink))  # Rosa skalle
        time.sleep(0.2) # Delay på 0.2s
        sense.set_pixels(skull(b, yellow)) # gul skalle
        time.sleep(0.2) # Delay på 0.2s

    # For-løkke for å printe poeng sum et siffer av gangen
    for number in range(0, len(StrScore)):   # for hvert siffer i poengsum
        sense.show_letter(StrScore[number], text_colour=b, back_colour=g)  # Bruker show letter for 
        time.sleep(0.4)  # Setter delay etter tall på 0.4s
        sense.clear(g)  # Clearer ut forgie siffer
        time.sleep(0.4) # Delay før neste siffer
   
    # Printer points til slutt med speed 0.04
    sense.show_message("Points", scroll_speed=0.04, text_colour=b, back_colour=g)
    sense.clear()  # Clearer matrise

    
def winner_graphic():
    # konstanter for farger
    b = (0,0,0)  # Sort farge for bakgrunn
    g = (96, 125, 139) # Gråfarge for skrift på pokal
    y = (255, 235, 59)  # Gul farge for skygge på pokal
    gold = (255, 193, 7)  # Gull farge for pokal
    silver = (158, 158, 158) # Sølvfarge for pokal
    bronze = (176, 141, 87) # Bronsefarge for pokal


    # Bruker definisjon for å kunne endre farge på pokalen uten å
    # Måtte ha flere ulike lister
    def cup(x):  # X er den fargen vi ønsker å bytte
        drawing = [b, x, x, x, x, x, x, b,
                 x, y, x, x, g, x ,y, x,
                 x, y, x, g, g, x, y, x,
                 x, y, x, x, g, x, y, x,
                 b, x, x, x, g, x, x, b,
                 b, b, x, x, g, x, b, b,
                 b, b, b, x, x, b, b, b,
                 b, b, x, x, x, x, b, b,]
        return drawing
             
    sense.set_pixels(cup(bronze)) # Setter bronsefarge på pokal
    time.sleep(1.0) # Delay på 0.5s
    sense.set_pixels(cup(silver)) # Setter sølvarge på pokal
    time.sleep(1.0) # delay på 0.5s
    sense.set_pixels(cup(gold)) # Setter gullfarge på pokal
    time.sleep(1.0) # Dealy på 1s før program kjører videre

def get_imu_values():
    """Få xyz-verdi"""
    _gyro = sense.get_gyroscope()
    pitch = _gyro["pitch"]
    return round(pitch)


def calculate_car_position(gyro):
    #Høyresving
    if gyro <= 180:
        pass

    #Venstresving
    if gyro >= 180:
        gyro = - abs(360 - gyro)

    
    gyro = -(gyro // 10) + 3
    #passer på at bilen ikke går utenfor skjermen
    gyro = restrict_value(gyro, 0, 6)
    #Endre bilposisjon
    return gyro


def wait_for_joystick_released():
    event = sense.stick.wait_for_event(emptybuffer=True)
    if event.action == "released":
        print("SPILLET RESTARTER")


def debug_print(buffer):
    os.system("clear")
    for line in buffer:
        for char in line:
            if char == NOCOLOR:
                print("..", end="")
            if char == CAR_COLOR:
                print("XX", end="")
            if char == GATE_COLOR:
                print("OO", end="")
        print()
    print()


def main():
    running = True
    iterator = 0

    #TODO: disse variablene burde reformateres bort/legges inn i while
    turn = 0
    visible_fuel_list = []
    fuel_already_taken = False
    gate_already_taken = False

    #TODO: reformater koden slik at en kan endre level og dermed alle frekvenser
    #      automatisk.
    

    #Spillet starter på nivå 1, så inkrementerer når du når det neste nivået
    level = 1


    #Spillet starter
    intro_graphic()
    next_level_graphic(level)
    theme_song = subprocess.Popen(["omxplayer", "--loop", THEME_SONG])

    #Hovedloopen som kjører så lenge spillet varer
    while running:
        #Lager ny buffer (som til slutt skal printes til skjermen)
        buffer = [[NOCOLOR for x in range(COLS)] for y in range(ROWS)]


        #Oppdaterer konstanter i forhold til "level"
        if level == 1:
            gate_width = 4
            frame_duration = FRAME_DURATION
            level_score_requirement = 16

        if level == 2:
            gate_width = 3
            frame_duration = FRAME_DURATION
            level_score_requirement = 32

        if level == 3:
            gate_width = 3
            frame_duration = 1/50
            level_score_requirement = 32


        #Finn nye gyro-verdier for xyz
        imu_values = get_imu_values()


        #Finn ut hvor bilen til spilleren som kjører på pien skal stå
        get_local_player().get_car().move_to(calculate_car_position(imu_values))

        for player in get_living_players():
            car = player.get_car()
            #Legg bilen til i printebuffer
            buffer[CAR_Y_POS][car.get_position()] = car.get_color()
        
        

        #Etter "GATE_FREQUENCY" iterasjoner, lag en ny gate
        if iterator % (GATE_FREQUENCY * GATE_SLOWNESS) == 0:
            gate_x_pos = get_gate_pos(gate_width)
            gate_y_start = iterator
            gate_already_taken = False


        #Legg gaten til i printebuffer
        gate_y_pos = abs(iterator - gate_y_start) // GATE_SLOWNESS
        buffer[gate_y_pos][gate_x_pos] = GATE_COLOR                 #Venstre påle
        buffer[gate_y_pos][gate_x_pos + gate_width] = GATE_COLOR    #Høyre påle


        #Etter "FUEL_FREQUENCY" iterasjoner, lag en ny gate
        if iterator % (FUEL_FREQUENCY * FUEL_SLOWNESS) == 1:
            fuel_x_pos = get_fuel_pos()
            fuel_y_start = iterator
            fuel_already_taken = False
            

        #Legg fuel til i printebuffer
        if iterator > 1:
            #TODO: fuel_already_taken gjør at fuel ikke blir printa
            fuel_y_pos = abs(iterator - fuel_y_start) // FUEL_SLOWNESS
            buffer[fuel_y_pos][fuel_x_pos] = FUEL_COLOR
        

        #Fuelnivået synker hver FUEL_DECREASE 'te gang
        if iterator % FUEL_DECREASE == 0:
            if fuel_already_taken == False:
                for player in get_living_players():
                    player.get_car().change_fuel(-1)
                    emit_websocket(player, "fuel", player.get_car().get_fuel())


        for player in get_living_players():
            #Dersom du har 2 eller færre fuel, spill av alarmlyd
            if player.get_car().get_fuel() <= 2:
                if player.is_low_fuel_alarm() == False:
                    player.set_low_fuel_alarm(True)
                    emit_websocket(player, "low_fuel", True)
                    if player is get_local_player():
                        low_fuel_sound = subprocess.Popen(["aplay", LOW_FUEL_SOUND])
                        

            #Dersom alarmen er på men du har fler enn 2 fuel, skru den av
            if player.get_car().get_fuel() > 2:
                if player.is_low_fuel_alarm() == True:
                    player.set_low_fuel_alarm(False)
                    emit_websocket(player, "low_fuel", False)
                    if player is get_local_player():
                        low_fuel_sound.kill()


        #Oppdaterer fuelbaren med verdi fra "fuel"
        buffer = draw_fuel(buffer, get_local_player().get_car().get_fuel())
                
            
        for player in get_living_players():
            #Når bilen passerer en gate, sjekk om du traff
            if CAR_Y_POS == gate_y_pos:
                if gate_x_pos <= player.get_car().get_position() <= gate_x_pos + gate_width:
                    if gate_already_taken == False:
                        #Du traff en gate som ikke har blitt truffet før
                        player.change_score(1)
                        emit_websocket(player, "score", player.get_score())
                        if player is get_local_player():
                            score_sound = subprocess.Popen(["aplay", SCORE_SOUND])

        #Denne variablen passer på at du ikke tar gaten flere ganger
        gate_already_taken = True


        #Tegner poengbar i toppen av skjermen
        buffer = draw_score_bar(buffer, get_local_player().get_score())

        #Når bilen passerer en fuel, sjekk om du traff
        if iterator > 1:
            if CAR_Y_POS == fuel_y_pos:
                for player in get_living_players():
                    if fuel_x_pos == player.get_car().get_position():
                        if fuel_already_taken == False:
                            player.get_car().change_fuel(2)
                            emit_websocket(player, "fuel", player.get_car().get_fuel())
                            if player is get_local_player():
                                pickup_fuel_sound = subprocess.Popen(["aplay", PICKUP_FUEL_SOUND])
                            
        # Indenter denne linjen opp til for-loopen for å kun gi fuel til 1 spiller
        #Denne variablen passer på at du ikke tar fuelen flere ganger
        fuel_already_taken = True


        #Inkrementer iterator
        iterator += 1


        ### Printer det som står i buffer til skjermen
        #Får alt over på éi liste i stedet for ei liste av lister
        flat_buffer = [element for sublist in buffer for element in sublist]


        #Printer til sensehat-skjermen
        sense.set_pixels(flat_buffer)

        if len(get_living_players()) == 0:
            #Avslutter "theme_song" og spiller av game over
            theme_song.kill()
            game_over_sound = subprocess.Popen(["aplay", GAME_OVER_SOUND])
            game_over_graphic(get_local_player().get_score())
            draw_sad_midjo(8)

            #TODO: Legg til scoreboard som leser fra en fil "hiscore.txt" og
            #      printer de beste scorene i synkende rekkefølge til skjermen
            #      vha. "draw_score_bar()". Dersom du har en hiscore vil det
            #      blinke en rød piksel ved siden av scoren din, og den blir
            #      lagt til i fila.

            #Venter på at spilleren skal trykke på joystick
            wait_for_joystick_released()

            for player in players.values():
                player.reset()
                emit_websocket(player, "reset")
                
            level = 1

            next_level_graphic(level)

        #Sjekk om du har nok poeng til å gå til neste nivå
        if all(player.get_score() >= level_score_requirement for player in get_living_players()):
            #Inkrementerer nivåvariablen
            level += 1

            #Nullstiller score
            
            for player in get_living_players():
                player.change_total_score(player.get_score())
                player.set_score(0)
                emit_websocket(player, "score", 0)
                emit_websocket(player, "total_score", player.get_total_score())

            #Print grafikk for neste level
            if level <= 3:
                next_level_graphic(level)

            if level > 3:
                #Du har runna spillet
                winner_graphic()

                #Venter på at spilleren skal trykke på joystick
                wait_for_joystick_released()

                #Reset score, total_score og fuel
                for player in players.values():
                    player.reset()
                    emit_websocket(player, "reset")
                level = 1
                next_level_graphic(level)


        #Delay
        time.sleep(frame_duration)


def host_websocket():
    """
        Multiplayer is hosted on
        http://pearpie.is-very-sweet.org:5001/site/index.html
    """
    from flask import Flask, request
    from sense_hat import SenseHat
    from flask_cors import CORS
    from flask_socketio import SocketIO
    from logging.config import dictConfig
    
    app = Flask(__name__, static_url_path='/site', static_folder='web')
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    socketio = SocketIO(app, cors_allowed_origins="*")

    @socketio.on('connect')
    def on_connect():
        if not players[request.sid]:
            players[request.sid] = Player(Car(CAR_COLOR), request.sid)
            print("Player connected: " + request.sid)

    @socketio.on('disconnect')
    def on_disconnect():
        players.pop(request.sid)
        print("Player disconnected: " + request.sid)

    @socketio.on('change_color')
    def on_change_color(json):
        player = players[request.sid]
        if player:
            player.get_car().set_color(json)
            print("Player " + request.sid + " changed color to " + json)

    @socketio.on('move_to')
    def on_socket_move_to(json):
        # Json is in this case an int sent by the ws client
        car = get_player(request.sid).get_car()
        car.move_to(json)
        print(car.get_position())

    @socketio.on('move_left')
    def on_socket_move_left(json):
        get_player(request.sid).get_car().move_left()

    @socketio.on('move_right')
    def on_socket_move_right(json):
        get_player(request.sid).get_car().move_right()

    @socketio.on('stop_moving_left')
    def on_socket_stop_move_left(json):
        # TODO: Implement holding button down to move car
        pass

    @socketio.on('stop_moving_right')
    def on_socket_stop_move_right(json):
        # TODO: Implement holding button down to move car
        pass

    def configure_flask_logger():
        """Makes the logs less verbose"""
        dictConfig({
            'version': 1,
            'formatters': {'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }},
            'handlers': {'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            }},
            'root': {
                'level': 'ERROR',
                'handlers': ['wsgi']
            }
        })
    
    configure_flask_logger()
    port=443
    # Port 443 is HTTPS
    if port == 443:
        ssl_certificate_folder = "/etc/letsencrypt/live/epstin.com/"
        context = (ssl_certificate_folder + "cert.pem", ssl_certificate_folder + "privkey.pem")#certificate and key files
        app.run(host="0.0.0.0", port=port, ssl_context=context)
    else:
        app.run(host="0.0.0.0", port=port)
    socketio.run(app)

if __name__ == "__main__":
    # use command "sudo python3 Milepael_2.py host" to host multiplayer
    if host_multiplayer:
        threading.Thread(target=host_websocket).start()
    main()
