import pygame as pg
import math as m
from pygame.sprite import Sprite


class Fear(Sprite):
    def __init__(self, screen, type):
        Sprite.__init__(self)
        self.image = pg.image.load("images/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = [320, 570]
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def moveToPlayer(self, px, py, maze):
        a = px - self.rect.centerx
        b = py - self.rect.centery
        self.rect.centerx += a / m.sqrt(a**2 + b**2) * 10
        self.rect.centery += b / m.sqrt(a**2 + b**2) * 10

    def dash(self, px, py, maze):
        a = px - self.rect.centerx
        b = py - self.rect.centery
        self.rect.centerx += a / max(m.sqrt(a**2 + b**2), 1) * 50
        self.rect.centery += b / max(m.sqrt(a**2 + b**2), 1) * 50
