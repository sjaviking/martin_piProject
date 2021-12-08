#!/bin/python3
from sense_hat import SenseHat
from math import sin
from random import choice
from datetime import datetime
from PIL import Image
import numpy as np
import glob
import os
import math
import time
import csv

# Init
sense = SenseHat()
sense.set_rotation(90)

# Constants
ROWS = 8
COLS = 8

# Farger
RED = (255, 0, 0)
ORANGE = (252, 144, 3)
YELLOW = (120, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 180, 255)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 199)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)    
  


def aleksander():
  W = (255, 255, 255) # White
  B = (0, 0, 0)       # Black
  p = (51, 0, 102)    # Purple
  b = (0, 0, 255)     # Blue
  y = (255, 255, 0)   # Yellow
  o = (255, 69, 0)    # Orange
  r = (255, 0, 0)     # Red

  def getTemperature():
      # Henter temperaturverdi fra Senshat
      temperature = round(sense.get_temperature())
      
      # Gir melding en bakgrunnsfarge, avhengig av temperaturen
      if temperature <= 31:
          back_colour = p
      elif 31 < temperature <= 32:
          back_colour = b
      elif 32 < temperature <= 33:
          back_colour = y
      elif 33 < temperature <= 34:
          back_colour = o
      elif temperature > 34:
          back_colour = r
       
      # Printer ut temperaturen med bakgrunnsfarge
      speed = 0.05
      sense.show_message("The Temp is: " + str(temperature) +
                           "C", speed, text_colour=W, back_colour=back_colour)
      
      return temperature  # Returnerer temperaturen
    
  # Setter temperaturen til get temperaturen for å ta med temperatur verdien videre
  temperature = getTemperature()
  
  # Tegner termostaten
  myImage = [
      B, B, W, W, W, W, B, B,
      B, B, W, B, B, W, B, B,
      B, B, W, B, B, W, B, B,
      B, B, W, B, B, W, B, B,
      B, B, W, B, B, W, B, B,
      B, W, B, B, B, B, W, B,
      B, W, B, B, B, B, W, B,
      B, B, W, W, W, W, B, B,
      ]

  def plot_ranges(color):
      # Definerer fargene til en piksel posisjon
      color_ranges = {
          p: [(50, 54), (42, 46)],
          b: [(35, 37)],
          y: [(27, 29)],
          o: [(19, 21)],
          r: [(11, 13)],
      }
      # Bytter ut pixlene i termostaten med hvilken farge som skal vises
      for (start, end) in color_ranges[color]:
          for i in range(start, end):
              myImage[i] = color
      
      # Bildet opptater seg for hver farge som skal vises
      sense.set_pixels(myImage)
      time.sleep(1)

  # Sier hvilken farger som skal vises, avhengig av hvilken temperatur det er
  if temperature <= 31:
      plot_ranges(p)

  elif 31 < temperature <= 32:
      plot_ranges(p)
      plot_ranges(b)

  elif 32 < temperature <= 33:
      plot_ranges(p)
      plot_ranges(b)
      plot_ranges(y)

  elif 33 < temperature <= 34:
      plot_ranges(p)
      plot_ranges(b)
      plot_ranges(y)
      plot_ranges(o)

  elif 34 < temperature <= 39:
      plot_ranges(p)
      plot_ranges(b)
      plot_ranges(y)
      plot_ranges(o)
      plot_ranges(r)

  elif temperature >= 40:
      plot_ranges(p)
      plot_ranges(b)
      plot_ranges(y)
      plot_ranges(o)
      plot_ranges(r)
      for n in range(2, 6):
          myImage[n] = r
      myImage[9] = r
      myImage[14] = r
      myImage[16] = r
      myImage[22] = r
  
  # Setter bildet til slutt
  sense.set_pixels(myImage)
  time.sleep(3)


def kristian():
    #genererer rader med valgt farge fra høyre
    def paintRow(x, color):
        #tegner først et bilde med valgt bakgrunnsfarge
        array = []
        u = 0
        while u < 64:
            array.append(RED)
            u += 1
        i = 0
        #fyller rader med valgt farge og antall rader
        while i < 8*x:
            array[i] = color
            i += 1
        sense.set_pixels(array)

      
    #genererer rader med valgt farge fra venstre
    def paintRowLeft(x, color):
        #tegner først et bilde med valgt bakgrunnsfarge
        array = []
        u = 0
        while u < 64:
            array.append(RED)
            u += 1
        i = 63
        #fyller rader med valgt farge og antall rader
        while i > 63 - 8*x  :
            array[i] = color
            i -= 1
        sense.set_pixels(array)

      
    #henter verdier
    def getIMUValues():
        # Gather all three sensor values from IMU
        compass = sense.get_compass()
        gyro = sense.get_gyroscope()
        accel = sense.get_accelerometer()
        return {"compass":compass, "accel":accel, "gyro":gyro}


    #diff er differansen mellom nye rader
    diff = 2
    var = 360 #hvilket utgangspunkt du vil ha
    konstant_deg = 5
    #velg hvor lenge while løkka skal kjøre:
    tid = 8
  
    #teller 60 sekunder x antall ganger
    t_end = time.time() + tid
    i = 0 #brukes for å printe compass mindre
    while time.time() < t_end:
        IMUValues = getIMUValues()
        compass = round(IMUValues["compass"])
        accel = (IMUValues["accel"])
        gyro = (IMUValues["gyro"]["pitch"])
        i += 1
        if i % 10 == 0:
            print("\r", gyro, end="")
        #nedover rot er ca. mellom 345 - 360
        if gyro <= (var) and gyro > (var - diff):
            paintRow(0, WHITE)
        elif gyro <= (var - diff) and gyro > (var - (diff*2)):
            paintRow(1, WHITE)
        elif gyro <= (var - (diff*2)) and gyro > (var - (diff*3)):
            paintRow(2, WHITE)
        elif gyro <= (var - (diff*3)) and gyro > (var - (diff*4)):
            paintRow(3, WHITE)
        elif gyro <= (var - (diff*4)) and gyro > (var - (diff*5)):
            paintRow(4, WHITE)
        elif gyro <= (var - (diff*5)) and gyro > (var - (diff*6)):
            paintRow(5, WHITE)
        elif gyro <= (var - (diff*6)) and gyro > (var - (diff*7)):
            paintRow(6, WHITE)
        elif gyro <= (var - (diff*7)) and gyro > (var - (diff*8)):
            paintRow(7, WHITE)
        elif gyro <= (var - (diff*8)) and gyro > (var - (diff*9)):
            paintRow(8, WHITE)
        #oppover rot er ca mellom: 0 - 45
        elif gyro >= (0) and gyro < (konstant_deg):
            paintRowLeft(0, WHITE)
        elif gyro >= (konstant_deg) and gyro < (konstant_deg + diff):
            paintRowLeft(1, WHITE)
        elif gyro >= (konstant_deg + diff) and gyro < (konstant_deg + diff*2):
            paintRowLeft(2, WHITE)
        elif gyro >= (konstant_deg + diff*2) and gyro < (konstant_deg + diff*3):
            paintRowLeft(3, WHITE)
        elif gyro >= (konstant_deg + diff*3) and gyro < (konstant_deg + diff*4):
            paintRowLeft(4, WHITE)
        elif gyro >= (konstant_deg + diff*4) and gyro < (konstant_deg + diff*5):
            paintRowLeft(5, WHITE)
        elif gyro >= (konstant_deg + diff*5) and gyro < (konstant_deg + diff*6):
            paintRowLeft(6, WHITE)
        elif gyro >= (konstant_deg + diff*6) and gyro < (konstant_deg + diff*7):
            paintRowLeft(7, WHITE)
        elif gyro >= (konstant_deg + diff*7) and gyro < (konstant_deg + diff*8):
            paintRowLeft(8, WHITE)
        else:
            sense.clear()
    return gyro

  
def knut_ola():
    global sense
    global ROWS
    global COLUMNS
    
    COLUMNS = COLS

    ######## Config ########
    # Uncomment if pixel rotation is oposite from physical rotation
    invert_rotation = 1
    #invert_rotation = -1

    ######## Config ########
    # Uncomment the correct axis
    #AXIS = "pitch"
    AXIS = "yaw"
    #AXIS = "roll"

    COLOR = (255, 0, 0)
    BLACK = (0, 0, 0)
    center_x = COLUMNS // 2
    center_y = ROWS // 2

    class SenseBuffer():
        def __init__(self, sense):
            self.arr = []
            self.sense = sense
            self.clear()

        def set_pixel(self, x, y, color):
            self.arr[(y * COLUMNS) + x] = color

        def clear(self):
            self.arr = []
            for i in range(0, COLUMNS * ROWS):
                self.arr.append(BLACK)

        def draw(self):
            self.sense.set_pixels(self.arr)

    sense_buffer = SenseBuffer(sense)

    def set_pixel(x, y):
        global pixels
        absolute_x = center_x + x
        absolute_y = center_y - y
        if (0 <= absolute_x <= (COLUMNS - 1)) and (0 <= absolute_y <= (ROWS - 1)):
            sense_buffer.set_pixel(absolute_x, absolute_y, COLOR)

    """
        a version of the tangent function where
        tan(angle) is symmetric around tan(45deg) 
        and zero at tan(0deg) and tan(90deg)
    """

    def get_continious_tan(angle):
        small_angle = angle % 45
        is_upper = abs(angle % 90) >= 45
        tan = math.tan(math.radians(small_angle))
        return 1 - tan if is_upper else tan

    """
        flips the axis generated by the continious_tangent function
        to create a continious circulat motion
    """

    def handle_odd_quarter(angle, x, y):
        is_odd_quarter = abs(angle // 90) % 2
        # angles in quadrant zero and two are mirrored
        # in quadrants one and three, the x value should decrease from zero, rather than decrease from max
        return (-y, x) if is_odd_quarter else (x, y)

    def make_continious(ajacent, angle, tan):
        is_upper = abs(angle % 90) > 45
        oposing = int(round(ajacent * tan))
        if is_upper:
            # In the upper portion of a quadrant the x value will decrease with the tangent, while the y value will increase independently
            return handle_odd_quarter(angle, oposing, ajacent)
        # In the upper portion of a quadrant the y value will increase with the tangent, while the x value will decrease independently
        return handle_odd_quarter(angle, ajacent, oposing)

    def draw_water(angle, x, y):
        translate_direction = -1 if 135 <= abs(angle % 360) < 315 else 1
        translate_on_x = 45 < abs(angle % 180) < 135
        for offset in range(0, (COLUMNS if translate_on_x else ROWS) + 1):
            directional_offset = offset * translate_direction
            if translate_on_x:
                # TODO: Why must x be subtracted from instead of added?
                set_pixel(x - directional_offset, y)
            else:
                set_pixel(x, y + directional_offset)

    def draw_horizon(angle):
        tan = get_continious_tan(angle)
        for x in range(-(center_x + 1), (center_x + 2)):
            x2, y = make_continious(x, angle, tan)
            draw_water(angle, x2, y + 1)

    def get_angle():
        return round(sense.get_orientation_degrees()[AXIS], 1)

    # Sense setup
    sense.set_rotation(90)
    sense.set_imu_config(False, True, False)

    offset = 0

    def reset_orientation():
        global offset
        offset = get_angle()

    sense.stick.direction_down = reset_orientation

    # Main Loop
    angle = 0
    run_time = 100
    for run_iteration in range(run_time):
        new_angle = get_angle()
        if angle != new_angle:
            angle = new_angle
            sense_buffer.clear()
            draw_horizon(invert_rotation * (angle - offset))
            sense_buffer.draw()
        time.sleep(0.1)


def gunnar():
    ### Conway's Game of Life ###
    # Constants
    live_colour = WHITE
    dead_colour = BLACK
    rand_area = ((2,2), (5,5))

    # Defining helper functions
    def count_neighbours(grid, pos_y, pos_x):
        neighbours = 0
        for y in range(-1, 2):
            for x in range(-1, 2):
                if grid[(pos_y + y) % ROWS][(pos_x + x) % COLS] == 1:
                    neighbours += 1
        return neighbours

    def print_to_led(grid, live_colour):
        led_array = [element for sublist in grid for element in sublist]
        sense.set_pixels([live_colour if cell == 1 else dead_colour for cell in led_array])

    def rainbow(n):
        colorsin = lambda x: int(127 * sin(x) + 127)
        return (colorsin(n), colorsin(n + 85), colorsin(n + 170))


    # Initializing grid with random data in the middle, seeded by sensor reading
    humidity = sense.get_humidity()
    seed = list(bin(hash(humidity))[2:])
    simulation = [[choice([int(n) for n in seed])
                    if rand_area[0][0] < x < rand_area[1][0]
                    or rand_area[0][1] < y < rand_area[1][1]
                    else 0
                    for x in range(ROWS)] for y in range(COLS)]


    # Run for 30 generations then quit
    for generation in range(30):
        live_colour = rainbow(generation)
        print_to_led(simulation, live_colour)
        for y, row in enumerate(simulation):
            for x, cell in enumerate(row):
                neighbours = count_neighbours(simulation, y, x)

                # Any live cell with fewer than two live neighbours
                # dies, as if by underpopulation.
                if (cell == 1) and (neighbours < 2):
                    cell = 0

                # Any live cell with two or three live neighbours lives
                # on to the next generation.
                elif (cell == 1) and (neighbours in [2, 3]):
                    cell = 1

                # Any live cell with more than three live neighbours dies,
                # as if by overpopulation.
                elif (cell == 1) and (neighbours > 3):
                    cell = 0

                # Any dead cell with exactly three live neighbours becomes
                # a live cell, as if by reproduction
                elif (cell == 0) and (neighbours == 3):
                    cell = 1

                simulation[y][x] = cell
        time.sleep(0.3)
    return humidity

  
def rickroll(number_of_frames=5300, rel_path="../Pictures/rickroll"):
    """Reads all .png images in path and prints
       them to the SenseHat led array. Provided
       images should be 8x8 pixels and be uniformly
       named with an incrementing number."""

    FRAME_DELAY = 1 / 25

    # Declare path to images
    script_dir = os.path.dirname(__file__)
    img_dir = os.path.join(script_dir, rel_path)

    # Make list of all .png filenames in the provided path
    filepaths = []
    for filepath in glob.glob(os.path.join(img_dir, "*.png")):
        filepaths.append(filepath)

    # Sort filepaths by the numeric value, e.g. "img/sometext0001.png" --> 1
    filepaths.sort(key=lambda s: int("".join([c for c in s if c.isdigit()])))
    
    # Print images to the led array
    for frame_num, frame in enumerate(filepaths):
        if frame_num > number_of_frames:
            break
        with Image.open(frame) as imgfile:
            img_array = np.asarray(imgfile)
            flat_image_array = [element for sublist in img_array for element in sublist]
            sense.set_pixels(flat_image_array)
            time.sleep(FRAME_DELAY)
            
            
def martin():
  # Setter opp en liste med de farger jeg ønsker å bruke
    available_colors = [RED, GREEN, BLUE, CYAN, MAGENTA, YELLOW]
    
    # bruker for-løkke som teller fra 0 til 70
    for i in range (0, 70):
        for _y in range (0, 8): # Teller y antall pixler
            for _x in range (0, 8): # Teller x antall pixler
                random_colors = choice(available_colors) # Bruker choice til å finne randome farge
                sense.set_pixel(_x,_y, random_colors) # setter den pixelen til den tilfeldige fargen
                _x += 1  # Teller opp på x 
            _y += 1 # Teller opp på y 
        i += 1 # teller opp på i
        time.sleep(0.1) # Delay på 0.1s
    compass = sense.get_compass()   # henter til slutt ut kompassdata
    return compass # Returnerer kompassdata

  
def andre():
    #Henter trykkverdier fra SenseHat
    pressure_0 = sense.get_pressure() 
    r = RED
    o = ORANGE
    g = GREEN
    b = BLUE
    s = BLACK
    
    for i in range(0,70):
        pressure = sense.get_pressure()
        # Define some colours
        
    #Sjekker hvor høyt trykket har endret seg i forhold til startverdi.
        if pressure < pressure_0 + 0.02:
            display = [
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, b, b, s, s, s
        ]
        elif pressure < pressure_0 + 0.04:
            display = [
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s
        ]
        elif pressure < pressure_0 + 0.06:
            display = [
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s
        ]
        elif pressure < pressure_0 + 0.08:
            display = [
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s
        ]
        elif pressure < pressure_0 + 0.10:
            display = [
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s
        ]
        elif pressure < pressure_0 + 0.12:
            display = [
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s
        ]
        elif pressure < pressure_0 + 0.14:
            display = [
            s, s, s, s, s, s, s, s,
            s, s, s, o, o, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s
        ]
        elif pressure < pressure_0 + 0.16:
            display = [
            s, s, s, r, r, s, s, s,
            s, s, s, o, o, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s,
            s, s, s, b, b, s, s, s
        ]

        else:
            display = [
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s,
            s, s, s, s, s, s, s, s 
        ]
        print(pressure)
        sense.set_pixels(display)
        i += 1
        time.sleep(0.10)
    return pressure #Returnerer pressure verdi til csv-fil


def main():
    with open("sensor_values.csv", "w") as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Main program loop
        while True:
            aleksander()
            pressure = andre()
            humidity = gunnar()
            knut_ola()
            gyro = kristian()
            compass = martin()
            rickroll(number_of_frames=150)
            
            # Sensor values to be written in sensor_values.csv
            timestamp = datetime.now()
            sensor_values = [timestamp, pressure, humidity, gyro, compass]
            
            for value in sensor_values:
                csv_writer.writerow(sensor_values)
        
        

if __name__ == "__main__":
    main()
