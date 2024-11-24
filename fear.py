import pygame as pg
import math as m
from pygame.sprite import Sprite


class Fear(Sprite):
    def __init__(self, screen, type, x, y):
        Sprite.__init__(self)
        self.image = pg.image.load("images/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.screen = screen
        self.isAgro = False
        self.isMoving = False

    def draw(self):
        if self.isAgro:
            if self.isMoving:
                self.screen.blit(pg.image.load("images/pixil-frame-0-1")e, self.rect)
            else:
                self.screen.blit(pg.image.load("images/pixil-frame-0-3")e, self.rect)
        else:
            if self.isMoving:
                self.screen.blit(pg.image.load("images/pixil-frame-0-2.png")e, self.rect)
            else:
                self.screen.blit(pg.image.load("images/pixil-frame-0-4.png")e, self.rect)
    def detect(maze):
        a = px - self.rect.centerx
        b = py - self.rect.centery
        if (m.sqrt(a**2 + b**2) < 75):
            self.agro = True
            return True
        self.agro = False
        return False
        
    def moveToPlayer(self, px, py, maze):
        self.isMoving = True
        a = px - self.rect.centerx
        b = py - self.rect.centery
        self.rect.centerx += min(a / max(m.sqrt(a**2 + b**2), 1) * 10, a)
        self.rect.centery += min(b / max(m.sqrt(a**2 + b**2), 1) * 10, b)
        a = px - self.rect.centerx
        b = py - self.rect.centery
        if a==b==0:
            self.isMoving = False

    def dash(self, px, py, maze):
        self.isMoving = True
        a = px - self.rect.centerx
        b = py - self.rect.centery
        self.rect.centerx += min(a / max(m.sqrt(a**2 + b**2), 1) * 50, a)
        self.rect.centery += min(b / max(m.sqrt(a**2 + b**2), 1) * 50, b)
        a = px - self.rect.centerx
        b = py - self.rect.centery
        if a==b==0:
            self.isMoving = False
