#!/bin/python3
from sense_hat import SenseHat
from time import sleep
from math import sin
from random import choice

# Init
sense = SenseHat()

# Constants
ROWS = 8
COLS = 8


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
    r = (255, 0 , 0)
    g = (0, 255, 0)
    b = (0, 0, 255)
    
    c = (0, 180, 255)
    m = (255, 0, 199)
    y = (120, 255, 0)
    
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


def main():
    with open("sensor_values.csv", "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Main program loop
        while True:
            #aleksander()
            #andre()
            humidity = gunnar()
            #knut_ola()
            #kristian()
            compass = martin()
            
            # Sensor values to be written in sensor_values.csv
            sensor_values = [humidity, compass]
            
            for value in sensor_values:
                csv_writer.writerow(sensor_values)
            
        
        
if __name__ == "__main__":
    main()
