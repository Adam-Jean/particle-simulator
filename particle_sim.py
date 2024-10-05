import pygame
import numpy as np
import random
from scipy.stats import truncnorm 
from random import randrange
import math
import sys
EPSILON = sys.float_info.epsilon  # Smallest possible difference.

pygame.init()

WINDOW = 1800,800
CENTER = [int(x/2) for x in WINDOW]


BLACK = (0,0,0)
WHITE = (255,255,255)

G = 0.9
M = 10e7

class Particle:
    def __init__(self, x, y, x_vel, y_vel, mass):
        self.g = G
        self.mass = mass
        self.x = x
        self.y = y
        self.momentum_x = x_vel 
        self.momentum_y = y_vel
        self.dt = 0.001
        velocity = round(abs(x_vel) + abs(y_vel)/2)
        self.rgb = self.convert_to_rgb(0,1800,velocity,self.get_color())
            
    def move(self, x_y_central_mass):
        x2 = x_y_central_mass[0]
        y2 = x_y_central_mass[1]
        hyp = (self.x - x2) ** 2 + (self.y - y2) ** 2
        theta = math.atan2(y2 - self.y, x2 - self.x)
        force = (self.g * self.mass * M) / hyp
        force_x = force * math.cos(theta)
        force_y = force * math.sin(theta)
        self.momentum_x += force_x * self.dt
        self.momentum_y += force_y * self.dt
        self.x += self.momentum_x / self.mass * self.dt
        self.y += self.momentum_y / self.mass * self.dt
        velocity = round(abs(self.momentum_x) + abs(self.momentum_y)/2)
        self.rgb = self.convert_to_rgb(0,1800,velocity,self.get_color())
        return [self.x, self.y, self.rgb]
    
    def convert_to_rgb(self, minval, maxval, val, colors):
        i_f = float(val-minval) / float(maxval-minval) * (len(colors)-1)
        i, f = int(i_f // 1), i_f % 1  # Split into whole & fractional parts.
        if f < EPSILON:
            #return colors[i]
            pass
        else: 
            (r1, g1, b1), (r2, g2, b2) = colors[0], colors[1]
            return (
                int(r1 + f*(r2-r1)), int(g1 + f*(g2-g1)), int(b1 + f*(b2-b1))
            )
    
    def get_color(self):
        max_r = randrange(200,255)
        max_g = randrange(0,55)
        max_b = randrange(0,55)

        min_r = randrange(0,55)
        min_g = randrange(0,55)
        min_b = randrange(200,255)

        return [(min_r, min_g, min_b), (max_r, max_g, max_b)]
    
    # def rgb_value(self, minimum, maximum, value):
    #     minimum, maximum = float(minimum), float(maximum)
    #     ratio = 2 * (value-minimum) / (maximum - minimum)
    #     b = int(max(0, 255*(1 - ratio)))
    #     r = int(max(0, 255*(ratio - 1)))
    #     g = 255 - b - r
    #     return (r, g, b)
        
def gaussian_random(mu, sigma, low, high):
    z = truncnorm.rvs(
    (low - mu) / sigma, (high - mu) / sigma, loc=mu, scale=sigma)
    return z


particles = []
def generator():
    for i in range(2000):
        x_vel = random.choice([gaussian_random(900, 100, 0, 1800)-900, gaussian_random(900, 100, 0,1800)-900, gaussian_random(900, 100, 0, 1800)-900])
        y_vel = random.choice([gaussian_random(900, 100, 0, 1800)-900, gaussian_random(900, 100, 0,1800)-900, gaussian_random(900, 100, 0, 1800)-900])

        mass = gaussian_random(2, 1, 1, 5)
        x_min, x_max = 0, WINDOW[0]
        y_min, y_max = 0, WINDOW[1]
        x = gaussian_random(CENTER[0], 400, x_min, x_max)
        y = gaussian_random(CENTER[1], 400, y_min, y_max)

        p = Particle(x,y,x_vel,y_vel,mass)
        particles.append(p)
    
def draw(): 
    for i in range(len(particles)):
        x_pos, y_pos, rgb = particles[i].move(pygame.mouse.get_pos())
        try:
            pygame.draw.circle(screen, rgb, (x_pos,y_pos), round(1.5*particles[i].mass))
        
        except:
            pygame.draw.circle(screen, WHITE, (x_pos,y_pos), round(1.5*particles[i].mass))



screen = pygame.display.set_mode(WINDOW)
generator()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #The user closed the window!
            running = False
           
    # Logic goes here
    screen.fill(BLACK)
    draw()
    pygame.display.update()

pygame.quit()

