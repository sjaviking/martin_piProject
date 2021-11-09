# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 09:35:19 2021

@author: marti
"""
from sense_hat import SenseHat
def martin():
    sense = SenseHat()
    from random import choice
    
    r = (255, 0 , 0)
    g = (0, 255, 0)
    b = (0, 0, 255)
    
    c = (0, 180, 255)
    m = (255, 0, 199)
    y = (120, 255, 0)
    
    available_colors = [r, g, b, c, m, y]
    
    while True:
      for _y in range (0, 8):
        for _x in range (0, 8):
          random_colors = choice(available_colors)
          sense.set_pixel(_x,_y, random_colors)
          _x += 1 
        _y += 1
        
    pressure = sense.get_pressure()
    return pressure