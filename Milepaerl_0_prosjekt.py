#!/bin/python3
from sense_hat import SenseHat
from time import sleep
from math import sin
from random import choice
from datetime import datetime
import csv

# Init
sense = SenseHat()

# Constants
ROWS = 8
COLS = 8

# Farger
r = (255, 0, 0)
g = (0, 255, 0)
b = (0, 0, 255)
c = (0, 180, 255)
m = (255, 0, 199)
y = (120, 255, 0)
k = (0, 0, 0)
w = (255, 255, 255)    

sense.set_rotation(90)

#genererer rader med valgt farge fra høyre
def paintRow(x, color):
  #tegner først et bilde med valgt bakgrunnsfarge
  array = []
  u = 0
  while u < 64:
    array.append(r)
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
    array.append(r)
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
  

def funksjonen_til_kristian():
    
  #diff er differansen mellom nye rader
  diff = 2
  var = 360 #hvilket utgangspunkt du vil ha
  konstant_deg = 5
  #velg hvor lenge while løkka skal kjøre:
  tid = 5
  
  #teller 60 sekunder x antall ganger
  t_end = time.time() + 60*tid
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
      paintRow(0, w)
    elif gyro <= (var - diff) and gyro > (var - (diff*2)):
      paintRow(1, w)
    elif gyro <= (var - (diff*2)) and gyro > (var - (diff*3)):
      paintRow(2, w)
    elif gyro <= (var - (diff*3)) and gyro > (var - (diff*4)):
      paintRow(3, w)
    elif gyro <= (var - (diff*4)) and gyro > (var - (diff*5)):
      paintRow(4, w)
    elif gyro <= (var - diff*5) and gyro > (var - (diff*6)):
      paintRow(5, w)
    elif gyro <= (var - (diff*6)) and gyro > (var - (diff*7)):
      paintRow(6, w)
    elif gyro <= (var - (diff*7)) and gyro > (var - (diff*8)):
      paintRow(7, w)
    elif gyro <= (var - (diff*8)) and gyro > (var - (diff*9)):
      paintRow(8, w)
    #oppover rot er ca mellom: 0 - 45
    elif gyro >= (0) and gyro < (konstant_deg):
      paintRowLeft(0, w)
    elif gyro >= (konstant_deg) and gyro < (konstant_deg + diff):
      paintRowLeft(1, w)
    elif gyro >= (konstant_deg + diff) and gyro < (konstant_deg + diff*2):
      paintRowLeft(2, w)
    elif gyro >= (konstant_deg + diff*2) and gyro < (konstant_deg + diff*3):
      paintRowLeft(3, w)
    elif gyro >= (konstant_deg + diff*3) and gyro < (konstant_deg + diff*4):
      paintRowLeft(4, w)
    elif gyro >= (konstant_deg + diff*4) and gyro < (konstant_deg + diff*5):
      paintRowLeft(5, w)
    elif gyro >= (konstant_deg + diff*5) and gyro < (konstant_deg + diff*6):
      paintRowLeft(6, w)
    elif gyro >= (konstant_deg + diff*6) and gyro < (konstant_deg + diff*7):
      paintRowLeft(7, w)
    elif gyro >= (konstant_deg + diff*7) and gyro < (konstant_deg + diff*8):
      paintRowLeft(8, w)
    else:
      sense.clear()


def gunnar():
    ### Conway's Game of Life ###
    # Constants
    live_colour = (255, 255, 255)
    dead_colour = (0, 0, 0)
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
        sleep(0.3)
    return humidity


def martin():
    
    available_colors = [r, g, b, c, m, y]
    
    i = 0
    for i in range ( 0, 10):
      for _y in range (0, 8):
        for _x in range (0, 8):
          random_colors = choice(available_colors)
          sense.set_pixel(_x,_y, random_colors)
          _x += 1 
        _y += 1
      i += 1
        
    compass = sense.get_compass()
    return compass
  
def andre():
    pressure_0 = sense.get_pressure()
    r = (255, 0, 0)
    o = (252, 144, 3)
    g = (0, 255, 0)
    b = (0, 255, 0)
    s = (0, 0, 0)
    
    while True:

        pressure = sense.get_pressure()
        # Define some colours
        

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

def main():
    with open("sensor_values.csv", "w") as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Main program loop
        while True:
            #aleksander()
            #andre()
            humidity = gunnar()
            #knut_ola()
            funksjonen_til_kristian()
            compass = martin()
            
            # Sensor values to be written in sensor_values.csv
            timestamp = datetime.now()
            sensor_values = [timestamp, humidity, compass]
            
            for value in sensor_values:
                csv_writer.writerow(sensor_values)
            
        
        
if __name__ == "__main__":
    main()
