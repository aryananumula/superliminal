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
        self.radius = 1000
        self.move = False

    def update(self):
        if self.move:
            if self.aggro:
                self.screen.blit(pg.image.load("images/pixil-frame-0-2.png"), self.rect)
            else:
                self.screen.blit(pg.image.load("images/pixil-frame-0-3.png"), self.rect)
        else:
            if self.aggro:
                self.screen.blit(pg.image.load("images/pixil-frame-0-4.png"), self.rect)
            else:
                self.screen.blit(pg.image.load("images/pixil-frame-0-5.png"), self.rect)

    def agro(self, ppos):
        if self.dist(ppos) < self.radius:
            self.aggro = True
            self.lastSeen = ppos
        else:
            self.aggro = False
        return self.aggro

    def dist(self, ppos):
        print(self.rect)
        return m.sqrt(
            (self.rect.centerx - ppos[0]) ** 2 + (self.rect.centery - ppos[1]) ** 2
        )

    def moveToPlayer(self, ppos):
        self.move = True
        a = ppos[0] - self.rect.centerx
        b = ppos[1] - self.rect.centery
        self.rect.centerx += a / max(m.sqrt(a**2 + b**2), 0.0001) * 1
        self.rect.centery += b / max(m.sqrt(a**2 + b**2), 0.0001) * 1
        print(a, b)
        if self.dist(ppos) < 10:
            self.move = False

    def dash(self, ppos):
        self.move = True
        a = ppos[0] - self.rect.centerx
        b = ppos[1] - self.rect.centery
        self.rect.centerx += a / max(m.sqrt(a**2 + b**2), 0.0001) * 50
        self.rect.centery += b / max(m.sqrt(a**2 + b**2), 0.0001) * 50
        if self.dist(ppos) < 10:
            self.move = False
