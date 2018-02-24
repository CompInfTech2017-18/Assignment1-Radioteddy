#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 11:53:17 2018

@author: radioteddy
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

class solid:
    def __init__(self, m, Vx, Vy, g, plotter):
        self.mass = m
        self.x_velocity = Vx
        self.y_velocity = Vy
        self.gravity = m*g
        self.plotter = plotter
    
    def x_coordinate(self, t):
        return self.x_velocity*t
    
    def y_coordinate(self, t):
        return self.y_velocity*t - self.gravity*t**2/(2.0*self.mass)
    
    def evolution(self):
        t = np.linspace(0, 10, 50)
        x = self.x_coordinate(t)
        y = self.y_coordinate(t)
        self.plotter.plot(x, y, 'red')
        
class rotator(solid):
    def __init__(self, m, Vx, Vy, g, r, phi, omega, q, E, plotter):
        solid.__init__(self, m, Vx, Vy, g, plotter)
        self.radius = r
        self.angle = phi
        self.angle_velocity = omega
        self.charge = q
        self.field = E
        
    def x_rotating(self, t, n):
        return self.x_coordinate(t) + ((-1)**n)*self.radius*np.cos(t*self.angle_velocity+self.angle)
    
    def y_rotating(self, t, n):
        return self.y_coordinate(t) + ((-1)**n)*self.radius*np.sin(t*self.angle_velocity+self.angle)    
        
    def rotating_evolution(self):      
        t = np.linspace(0, 10, 50)
        
        x_1 = self.x_coordinate(t) + self.radius*np.cos(t*self.angle_velocity+self.angle)
        y_1 = self.y_coordinate(t) + self.radius*np.sin(t*self.angle_velocity+self.angle)
        self.plotter.plot(x_1, y_1, 'orange')
        
        x_2 = self.x_coordinate(t) - self.radius*np.cos(t*self.angle_velocity+self.angle)
        y_2 = self.y_coordinate(t) - self.radius*np.sin(t*self.angle_velocity+self.angle)
        self.plotter.plot(x_2, y_2, 'darkblue')   
        
    def field_phase(self, t):
        def function(x, t):
            phi, omega = x
            return [omega, (self.mass*self.radius)/(self.charge*self.field)*np.sin(omega)]
        return odeint(function, [0, self.angle_velocity], t)[:, 0]
      
    def field_evolution(self):
        t = np.linspace(0, 10, 50)
        
        x_1 = self.x_coordinate(t) + self.radius*np.cos(self.field_phase(t))
        y_1 = self.y_coordinate(t) + self.radius*np.sin(self.field_phase(t))
        self.plotter.plot(x_1, y_1, 'seagreen')
            
        x_2 = self.x_coordinate(t) - self.radius*np.cos(self.field_phase(t))
        y_2 = self.y_coordinate(t) - self.radius*np.sin(self.field_phase(t))
        self.plotter.plot(x_2, y_2, 'maroon')
    

class plotter:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)      
    
    def plot(self, x, y, color):
        return self.ax.plot(x, y, color)
    
    def show(self):
        plt.show()    
    
plotting = plotter()
system = rotator(1.0, 0.1, 0.5, 1.0, 0.1, 0.1, 6.0, 1.0, 1.0, plotting)
system.evolution()
system.rotating_evolution()
system.field_evolution()        
