import pygame


class SpacePartition:
    def __init__(self):
        self.ID = 0   # ID and the serial of the partition block
        self.Bounds = pygame.Rect(0, 0, 0, 0)
        self.ObjectList = []

        # neighbour IDs
        self.Neighbour = [0] * 8
