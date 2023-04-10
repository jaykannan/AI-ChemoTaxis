import pygame
import random
import numpy as np
import math
from enum import Enum
from pygame.math import Vector2
from logdata import LogData
from enums import FType, CProperty
from globals import Globals

class FloatingObject:
    def __init__(self, position, ftype):
        self.type = ftype
        self.temperature = 0.0
        self.drift = 0.0
        self.rise = 0.0

        # common logging data
        self.log = LogData()
        self.ID = random.randint(0, 999999)

        self.vPosition = Vector2(position)
        self.vCurrentForce = Vector2(0, 0)    # direction of the force
        self.vMechanicalForce = Vector2(0, 0)  # mechanical force which averages out  
        self.color = pygame.Color('white')
        self.vRadius = 1.0                    # radius of the vesicle
        self.vRadiusThreshold = 3.0           # maximum size of the vesicle before it breaks due to external forces
        self.rand = random.Random()
        self.currentPartition = 0
        
        # also a type of object
        self.objectType = 0                   # could be a random type of molecule that affects other monomers around it

    def LoadContent(self):
        pass

    def update(self, graphicsDevice, gameTime):
            # maintain a timer
            self.log.lifeTimer += gameTime.elapsed_time.total_seconds()

            # calculate distance travelled bu current and mechanical force
            self.log.distanceTravelled += np.linalg.norm(self.vCurrentForce) * gameTime.elapsed_time.total_seconds()
            self.log.distanceTravelled += np.linalg.norm(self.vMechanicalForce) * gameTime.elapsed_time.total_seconds()

            self.vPosition += self.vCurrentForce * gameTime.elapsed_time.total_seconds()

            self.vPosition += self.vMechanicalForce
            self.vMechanicalForce *= 0.95     # average out any mechanical force that is caused by monomers

            if self.type != FType.ABSORBED:    
                # if it is a polymer, it rides with the vesicle
                # temperature heats up the molecule - the closer to the bottom the hotter it gets
                # the closer to the surface the colder it gets
                self.temperature = self.sigmoid(self.vPosition[1] / graphicsDevice.get_height()) * 100
                self.drift = -((self.vPosition[1] / graphicsDevice.get_height()) - 0.5)

                self.vCurrentForce[0] = self.drift * random.randint(Globals.DRIFTMIN, Globals.DRIFTMAX)

                if self.temperature < random.randint(Globals.TEMPERATURE_LMIN, Globals.TEMPERATURE_LMAX):
                    self.vCurrentForce[1] += random.randint(Globals.RISE)
                elif self.temperature > random.randint(Globals.TEMPERATURE_UMIN, Globals.TEMPERATURE_UMAX):
                    self.vCurrentForce[1] -= random.randint(Globals.RISE)
                else:
                    self.vPosition[1] += self.vCurrentForce[1] * gameTime.elapsed_time.total_seconds() * random.randint(Globals.RISE / 2)

                # warp them so that the simulation looks consistant
                if self.vPosition[0] < 0:
                    self.vPosition[0] = graphicsDevice.get_width()
                if self.vPosition[0] > graphicsDevice.get_width():
                    self.vPosition[0] = 0
                if self.vPosition[1] < 0:
                    self.vPosition[1] = 0
                    self.vCurrentForce[1] *= -0.5
                if self.vPosition[1] > graphicsDevice.get_height():
                    self.vPosition[1] = graphicsDevice.get_height()
                    self.vCurrentForce[1] *= -0.5

    def sigmoid(self, x):
        return (2 / (1 + math.exp(-2 * x)) - 1)
