import pygame

from floatingobject import FloatingObject
from polymer import Polymer

class Vesicle(FloatingObject):
    def __init__(self, texture):
        super().__init__()
        self.VTexture = texture
        self.Polymers = [Polymer()]

    def update(self, graphicsDevice, gameTime):
        for p in self.Polymers:
            for m in p.Chain:
                m.vPosition = self.vPosition + (m.offset * 0.5)

        super().update(graphicsDevice, gameTime)

    def draw(self, spriteBatch):
        center = pygame.Vector2(self.VTexture.get_rect().center)
        scale = self.vRadius / 64.0
        for p in self.Polymers:
            for m in p.Chain:
                m.draw(spriteBatch)
        spriteBatch.draw(self.VTexture, self.vPosition, None, super().color, 0.0, center, scale, pygame.sprite.SpriteEffects.NONE, 1.0)
        super().draw(spriteBatch)
