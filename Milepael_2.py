import random
import time
import os

# Om du kjører koden lokalt kan du sette DEBUG til True.
# -- printer til terminal i stedet for RPi sensehat
DEBUG = True

if not DEBUG:
    from sense_hat import SenseHat
    sense = SenseHat()

ROWS = 8
COLS = 8

FPS = 25
FRAME_DURATION = 1 / FPS

GATE_FREQUENCY = 8
GATE_WIDTH = 2
CAR_Y_POS = 6
GAME_LENGTH = 200
CAR_COLOR = (255, 255, 255)
GATE_COLOR = (255, 0, 0)
NOCOLOR = (0, 0, 0)


def get_gate_pos():
    """Returner x-posisjon til gate som du skal treffe med bilen"""
    #Gjør så det er større sannsynlighet for å treffe porter i midten
    skew = lambda x: - (1/16) * (x - 4)**2 + 1

    port_pos = round(skew(random.randint(0, 99) / 100) * 8)
    return port_pos


def increment_buffer(buffer):
    """Flytt banen en piksel nedover"""
    pass


def intro_graphic():
    """Tegn noe kult"""
    pass


def game_over_graphic(score):
    """Vis score"""
    pass


def get_imu_values():
    """Få xyz-verdi"""
    pass


def calculate_car_position(imu_values):
    """Returner x-posisjon for bilen"""
    # returner tall mellom 0 og 7
    return 3


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
    score = 0
    #buffer = []


    intro_graphic()

    #Spillet starter
    while running:
        buffer = [[NOCOLOR for x in range(8)] for y in range(8)]
        #Finn nye gyro-verdier for xyz
        imu_values = get_imu_values()

        #Finn ut hvor bilen skal stå
        car_x_pos = calculate_car_position(imu_values)

        #Legg bilen til i printebuffer
        buffer[CAR_Y_POS][car_x_pos] = CAR_COLOR
        
        #Etter "GATE_FREQUENCY" iterasjoner, lag en ny gate
        if iterator % GATE_FREQUENCY == 0:
            gate_x_pos = get_gate_pos()
            gate_y_start = iterator
            print("Made gate")

        #Legg gaten til i printebuffer
        print(gate_x_pos)
        gate_y_pos = abs(iterator - gate_y_start)
        buffer[gate_y_pos][gate_x_pos] = GATE_COLOR
        buffer[gate_y_pos][gate_x_pos + GATE_WIDTH] = GATE_COLOR

        #Når bilen passerer en gate, sjekk om du traff
        if CAR_Y_POS == gate_y_pos:
            if gate_x_pos <= car_x_pos <= gate_x_pos + GATE_WIDTH:
                score += 1

        #Inkrementer iterator
        iterator += 1

        #Print banen
        if DEBUG:
            debug_print(buffer)
        else:
            #Får alt over på éi liste i stedet for ei liste av lister
            flat_buffer = [element for sublist in buffer for element in sublist]

            #Printer til sensehat-skjermen
            sense.set_pixels(buffer)

        #Når det har gått GAME_LENGTH antall iterasjoner, stopp spillet
        if iterator >= GAME_LENGTH:
            game_over_graphics(score)
            running = False

        #Delay
        time.sleep(FRAME_DURATION)


if __name__ == "__main__":
    main()
