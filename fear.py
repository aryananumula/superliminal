import pygame as pg
import math as m
from pygame.sprite import Sprite


class Fear(Sprite):
    def __init__(self, screen, pos):
        Sprite.__init__(self)
        self.pos = pos
        self.image = pg.image.load("images/player.png")
        self.rect = self.image.get_rect()
        self.screen = screen
        self.aggro = False
        self.lastSeen = pos
        self.radius = 5

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def agro(self, ppos):
        if (
            m.sqrt(
                (self.rect.centerx - ppos[0]) ** 2 + (self.rect.centery - ppos[1]) ** 2
            )
            < self.radius
        ):
            self.aggro = True
            self.lastSeen = ppos
        return self.aggro

    def dist(self, ppos):
        return m.sqrt(
            (self.rect.centerx - ppos[0]) ** 2 + (self.rect.centery - ppos[1]) ** 2
        )

    def moveToPlayer(self, ppos):
        a = ppos[0] - self.rect.centerx
        b = ppos[1] - self.rect.centery
        if self.dist(ppos) > 10:
            self.rect.centerx += a / m.sqrt(a**2 + b**2) * 10
            self.rect.centery += b / m.sqrt(a**2 + b**2) * 10

    def dash(self, ppos):
        a = ppos[0] - self.rect.centerx
        b = ppos[1] - self.rect.centery
        self.rect.centerx += a / max(m.sqrt(a**2 + b**2), 1) * 50
        self.rect.centery += b / max(m.sqrt(a**2 + b**2), 1) * 50
