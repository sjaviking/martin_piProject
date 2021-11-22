from random import randint
from sense_hat import SenseHat

sense = SenseHat()


def get_gate_pos():
    """Returner x-posisjon til gate som du skal treffe med bilen"""
    #Gjør så det er større sannsynlighet for å treffe porter i midten
    skew = lambda x: - (1/16) * (x - 4)**2 + 1

    port_pos = skew(random.randint(0, 99) / 100) 
    pass


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
    pass


def debug_print(buffer):
    for line in buffer:
        print(line)


def main():
    running = True
    iterator = 0
    score = 0
    buffer = []

    ROWS = 8
    COLS = 8

    GATE_FREQUENCY = 8
    GATE_WIDTH = 4
    CAR_Y_POS = 1
    GAME_LENGTH = 120
    CAR_COLOR = (255, 255, 255)

    intro_graphic()

    #Spillet starter
    while running:
        #Finn nye gyro-verdier for xyz
        imu_values = get_imu_values()

        #Finn ut hvor bilen skal stå
        car_x_pos = calculate_car_position(imu_values)

        #TODO: Legg bilen til i printebuffer
        buffer[CAR_Y_POS][car_x_pos] = CAR_COLOR
        
        #Etter "GATE_FREQUENCY" iterasjoner, lag en ny gate
        if iterator % GATE_FREQUENCY == 0:
            gate_x_pos = get_gate_pos()
            gate_y_start = iterator

        #TODO: Legg gaten til i printebuffer
        # x = gate_x_pos
        gate_y_pos = abs(iterator - gate_y_start)

        #Inkrementer iterator
        iterator += 1

        #Når bilen passerer en gate, sjekk om du traff
        if CAR_Y_POS == gate_y_pos:
            if gate_x_pos <= car_x_pos <= gate_x_pos + GATE_WIDTH:
                score += 1

        #Når det har gått GAME_LENGTH antall iterasjoner, stopp spillet
        if iterator >= GAME_LENGTH:
            game_over_graphics(score)
            running = False


if __name__ == "__main__":
    main()
