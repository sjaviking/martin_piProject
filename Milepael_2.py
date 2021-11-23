import random
import time
import os

from flask import Flask
from sense_hat import SenseHat
from flask_cors import CORS
from flask_socketio import SocketIO
import threading
from logging.config import dictConfig

# Om du kjører koden lokalt kan du sette DEBUG til True.
# -- printer til terminal i stedet for RPi sensehat
DEBUG = True

if not DEBUG:
    from sense_hat import SenseHat
    sense = SenseHat()

ROWS = 8
COLS = 8
car_x_pos = 3

FPS = 5
FRAME_DURATION = 1 / FPS

GATE_FREQUENCY = 8
FUEL_FREQUENCY = 23
GATE_WIDTH = 2
CAR_Y_POS = 6
GAME_LENGTH = 200
CAR_COLOR = (255, 255, 255)
GATE_COLOR = (255, 0, 0)
NOCOLOR = (0, 0, 0)

def restrict_value(value, min_value, max_value):
    return max(min_value, min(max_value, value))
    
def move_car(change):
    global car_x_pos
    car_x_pos = restrict_value(car_x_pos + change, 0, COLS - 1)

def get_gate_pos():
    """Returner x-posisjon til gate som du skal treffe med bilen"""
    #Gjør så det er større sannsynlighet for å treffe porter i midten
    skew = lambda x: - (1/16) * (x - 4)**2 + 1

    gate_pos = int(skew(random.randint(0, 99) / 100) * 8)
    return gate_pos


def increment_buffer(buffer):
    """Flytt banen en piksel nedover"""
    pass


def intro_graphic():
    sense.low_light = True
    TheGame = 'Midjo Grand Prix'
    sense.show_message('Welcome to', scroll_speed=0.06, text_colour=[0,0,0], back_colour=[194, 27, 209])

    sense.low_ligh = False
    for q in range(0, len(TheGame)-1, 2):
      sense.show_letter(TheGame[q], text_colour=[255, 255, 255], back_colour=[0, 0 ,0])
      time.sleep(0.5)
      sense.show_letter(TheGame[q+1], text_colour=[0,0,0], back_colour=[255, 255, 255])
      time.sleep(0.5)
    sense.low_light = True

    sense.show_message('Pitch to control', scroll_speed=0.05, text_colour=[0,0,0], back_colour=[194, 27, 209])
    sense.clear()
    pass


def game_over_graphic(score):
    score = str(123) # midlertidig poengsum, for at proragm skal kjøre
 
    sense.low_light = True   # Lav lysintensitet

    sense.show_message("Game Over! Score:", scroll_speed=0.06, text_colour=[255, 0, 0], back_colour=[50, 166, 168])

    for p in range(0, len(str(score))):   # Printer hvert siffer i poengsum
        sense.show_letter(score[p], back_colour=[194, 27, 209])
        time.sleep(0.5)
        sense.clear(194, 27, 209)  # Clearer ut forgie siffer
        time.sleep(0.5)

    sense.show_message("Points", back_colour=[194, 27, 209])   # Printer points til slutt
    sense.clear()  # Clearer matrise


def get_imu_values():
    """Få xyz-verdi"""
    _gyro = sense.get_gyroscope()
    pitch = _gyro["pitch"]
    return round(pitch)


def calculate_car_position(imu_values):
    """Returner x-posisjon for bilen"""
    for number in range(-20, 20, 5):
        if imu_values in range(number, number+5):
            return imu_values/2.5


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
        #Lager ny buffer (som til slutt skal printes til skjermen)
        buffer = [[NOCOLOR for x in range(COLS)] for y in range(ROWS)]


        #Finn nye gyro-verdier for xyz
        if not DEBUG:
            imu_values = get_imu_values()


        #Finn ut hvor bilen skal stå
        if not DEBUG:
            car_x_pos = calculate_car_position(imu_values)
        else:
            #TODO: legg inn keyboard-kontroller her så du kan 
            # styre med piltastene på pc
            car_x_pos = 3


        #Legg bilen til i printebuffer
        buffer[CAR_Y_POS][car_x_pos] = CAR_COLOR
        

        #Etter "GATE_FREQUENCY" iterasjoner, lag en ny gate
        if iterator % GATE_FREQUENCY == 0:
            gate_x_pos = get_gate_pos()
            gate_y_start = iterator


        #TODO: legg til fuel-tønner som dukker opp etter FUEL_FREQUENCY
        # antall iterasjoner. Når du treffer fuel fyller du opp baren
        # på høyre side av skjermen. Går du tom for fuel er spillet over.


        #Legg gaten til i printebuffer
        gate_y_pos = abs(iterator - gate_y_start)
        buffer[gate_y_pos][gate_x_pos] = GATE_COLOR                 #Venstre påle
        buffer[gate_y_pos][gate_x_pos + GATE_WIDTH] = GATE_COLOR    #Høyre påle



        #Når bilen passerer en gate, sjekk om du traff
        if CAR_Y_POS == gate_y_pos:
            if gate_x_pos <= car_x_pos <= gate_x_pos + GATE_WIDTH:
                if car_x_pos == gate_x_pos + GATE_WIDTH // 2:
                    score += 3
                    print("Score + 3")
                else:
                    score += 1
                    print("Score + 1")


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
            if DEBUG:
                break
            game_over_graphics(score)
            running = False
        

        #Delay
        time.sleep(FRAME_DURATION)

app = Flask(__name__, static_url_path='/site', static_folder='web')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('move_left')
def on_socket_move_left():
    move_car(-1)

@socketio.on('move_right')
def on_socket_move_right():
    move_car(1)

@socketio.on('stop_moving_left')
def on_socket_stop_move_left():
    # TODO: Implement holding button down to move car
    pass

@socketio.on('stop_moving_right')
def on_socket_stop_move_right():
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

def host_websocket():
    """
        Multiplayer is hosted on
        http://pearpie.is-very-sweet.org:5001/site/index.html
    """
    configure_flask_logger()
    app.run(host="0.0.0.0", port=5001)
    socketio.run(app)

if __name__ == "__main__":
    threading.Thread(target=host_websocket).start()
    main()
