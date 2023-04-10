import random
from enums import CProperty
from floatingobject import FloatingObject


class Monomer(FloatingObject):
    def __init__(self, texture, p):
        super().__init__()
        self.vTexture = texture
        self.property = p
        self.affectsType = random.randint(0, 9)

        # pick a color based on property
        if self.property == CProperty.ATTACH:
            self.color = (0, 0, 255)
        elif self.property == CProperty.ATTRACT:
            self.color = (255, 105, 180)
        elif self.property == CProperty.COMBINE:
            self.color = (128, 0, 128)
        elif self.property == CProperty.COPY:
            self.color = (255, 0, 0)
        elif self.property == CProperty.DECREASE_PH:
            self.color = (255, 255, 0)
        elif self.property == CProperty.INCREASE_PH:
            self.color = (255, 165, 0)
        elif self.property == CProperty.REPEL:
            self.color = (128, 128, 0)
        elif self.property == CProperty.SPLIT:
            self.color = (165, 42, 42)
        elif self.property == CProperty.SUBTRACT:
            self.color = (0, 0, 0)
        
        self.vCurrentForce = (0, random.randint(0, 9) - 5)
        self.objectType = random.randint(0, 9)
        self.offset = (0, 0)

    def update(self, graphicsDevice, gameTime):
        super().update(graphicsDevice, gameTime)

    def draw(self, screen):
        screen.blit(self.vTexture, self.vPosition, self.color, (0, 0, self.vTexture.get_width(), self.vTexture.get_height()))
        super().draw(screen)
