import pygame
import math
import json
import random

import create
import fear


class Button:
    def __init__(self, size, text, pos, bgColor=(255, 255, 255), textColor=(0, 0, 0)):
        self.pos = pos
        self.size = size
        self.text = text
        self.font = pygame.font.Font(pygame.font.get_default_font(), size[1])
        self.textSurf = self.font.render(f"{text}", True, textColor)
        self.button = pygame.Surface((size[0], size[1])).convert()
        self.button.fill(bgColor)
        self.rect = self.button.get_rect()
        self.rect.center = self.pos
        self.color = bgColor

    def render(self, window):
        pygame.draw.rect(window, self.color, self.rect, border_radius=10)
        window.blit(self.textSurf, (self.pos[0] - 5, self.pos[1] + 5))

    def clicked(self, events):
        mousePos = pygame.mouse.get_pos()  #  get the mouse position
        for event in events:
            if self.button.get_rect(topleft=self.pos).collidepoint(
                mousePos[0], mousePos[1]
            ):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return True
        return False


# import fear
pygame.mixer.init()

pygame.mixer.music.load("sounds/ambient.mp3")
pygame.mixer.music.play(-1)
di = 0
# grid = create.OO0OOO0000O0OOOO0(64)
grid = create.gm(8)

pygame.font.init()

text = pygame.font.Font("vinque.otf", 30)

# open("level1.json", "w").write(str(grid.tolist()))

tab = pygame.image.load("images/tab.png")

# pygame setup
WIDTH = 1280
HEIGHT = 720
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1, flags=pygame.SCALED)
clock = pygame.time.Clock()
# fear1 = fear.Fear(screen, "something")
running = True
dt = 0

ps = 128

plx, ply = ps / 2, ps / 2
scx, scy = plx, ply

playerSprite = pygame.image.load("images/shade1.png")
playerSprite = pygame.transform.scale(playerSprite, (ps, ps))

overlay = pygame.image.load("images/overlay.png")
overlay = pygame.transform.scale(overlay, (1280, 720))

level = json.load(open("level1.json"))

t = -1
j = 10
onGround = True
lt = 0
stage = "game"
flashlight = False
flashlight_image = pygame.image.load("images/fr.png")
flashlight_image = pygame.transform.scale(flashlight_image, (WIDTH * 1.4, HEIGHT * 2))
size = 256

tile1 = pygame.image.load("images/tile1.png")
tile1 = pygame.transform.scale(tile1, (size, size))
tile3 = pygame.image.load("images/tile3.png")
tile3 = pygame.transform.scale(tile3, (size, size))
tile4 = pygame.image.load("images/tile4.png")
tile4 = pygame.transform.scale(tile4, (size, size))

fears = [fear.Fear(screen, pos=[0, 0])]


def smmothstep(edge0, edge1, x):
    t = min(1, max(0, (x - edge0) / (edge1 - edge0)))
    return t * t * (3.0 - 2.0 * t)


def gen_damage_image(scale, source):
    scale_size = (20, 20)
    scale_img = pygame.Surface(scale_size, flags=pygame.SRCALPHA)
    for i in range(scale_size[0]):
        for j in range(scale_size[1]):
            fx = smmothstep(0, scale_size[0] / 2 * scale, min(i, scale_size[0] - i))
            fy = smmothstep(0, scale_size[1] / 2 * scale, min(j, scale_size[1] - j))
            fade_color = [int(max(0, 255 - (1 - fx * fy) * 255)) for c in range(4)]
            scale_img.set_at((i, j), fade_color)
    dest = source.copy()
    scale_img = pygame.transform.smoothscale(scale_img, dest.get_size())
    dest.blit(scale_img, (0, 0), special_flags=pygame.BLEND_ADD)
    return dest


def draw_ngon(Surface, color, n, radius, position):
    pi2 = 2 * 3.14

    for i in range(0, n):
        pygame.draw.line(
            Surface,
            color,
            position,
            (
                cos(i / n * pi2) * radius + position[0],
                sin(i / n * pi2) * radius + position[1],
            ),
        )

    return pygame.draw.lines(
        Surface,
        color,
        True,
        [
            (
                cos(i / n * pi2) * radius + position[0],
                sin(i / n * pi2) * radius + position[1],
            )
            for i in range(0, n)
        ],
    )


def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


largeText = pygame.font.Font("vinque.otf", 100)

# Creating a Title Screen
TextSurf, TextRect = text_objects("data", largeText)
TextRect.center = (WIDTH // 2, HEIGHT // 2)

# Play Button

button = Button([WIDTH // 2, HEIGHT // 2], "start", [50, 50])

# Loop until the user clicks the close button
done = False

vy = 0
vx = 0
while running:
    t += 1
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if stage == "menu":
        screen.fill((0, 0, 0))
        button.render(screen)
        if button.clicked(pygame.event.get()):
            stage = "game"
    elif stage == "game":
        if keys[pygame.K_SPACE]:
            flashlight = True
        else:
            flashlight = False
        scx = round(scx + (plx - scx) / 10)
        scy = round(scy + (ply - scy) / 10)
        screen.fill("#060606")
        o = -1
        r = 2
        if flashlight and random.randrange(0, 60) != 0:
            for i in level:
                o += 1
                p = -1
                for j in i:
                    p += 1
                    if j > 0:
                        if size * p - (r) * size < plx < p * size + size * (
                            1 + r
                        ) and size * o - (r) * size < ply < o * size + size * (1 + r):
                            # checks
                            pygame.draw.rect(
                                screen,
                                (255, 0, 0),
                                (
                                    size * p - scx + screen.get_width() / 2,
                                    size * o - scy + screen.get_height() / 2,
                                    size,
                                    size,
                                ),
                            )
                            if j == 2:
                                shrine = pygame.image.load(
                                    f"images/shrinebase{t%3 + 1}.png"
                                )
                                shrine = pygame.transform.scale(
                                    shrine, (size / 2, size / 2)
                                )
                                screen.blit(
                                    shrine,
                                    (
                                        size * p - scx + screen.get_width() / 2,
                                        size * o
                                        - scy
                                        + screen.get_height() / 2
                                        + 128
                                        + 4,
                                    ),
                                )
                                tab = pygame.transform.scale(tab, (128, 128))
                                screen.blit(
                                    tab,
                                    (
                                        size * p - scx + screen.get_width() / 2 + 2,
                                        size * o
                                        - scy
                                        + screen.get_height() / 2
                                        + 64
                                        + 20 * math.sin(t / 25),
                                    ),
                                )
                        """if o + 1 == len(level):
                            if o == 0:
                                if p + 1 == len(level[o]):
                                    if 0 == p:
                                        screen.blit(
                                            pygame.transform.rotate(tile1.copy(), 90),
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                    elif level[o][p - 1] == 0:
                                        screen.blit(
                                            pygame.transform.rotate(tile1.copy(), 90),
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                    else:
                                        pass
                                elif level[o][p + 1] == 0:
                                    screen.blit(
                                        pygame.transform.rotate(tile1.copy(), 90),
                                        (
                                            size * p - scx + screen.get_width() / 2,
                                            size * o - scy + screen.get_height() / 2,
                                            size,
                                            size,
                                        ),
                                    )
                                else:
                                    if 0 == p:
                                        screen.blit(
                                            pygame.transform.rotate(tile1.copy(), 90),
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                    elif level[o][p - 1] == 0:
                                        screen.blit(
                                            pygame.transform.rotate(tile1.copy(), 90),
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                    else:
                                        screen.blit(
                                            tile1,
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                            elif level[o - 1][p] == 0:
                                if p + 1 == len(level[o]):
                                    screen.blit(
                                        pygame.transform.rotate(tile1.copy(), 90),
                                        (
                                            size * p
                                            - scx
                                            + screen.get_width() / 2
                                            - 19,
                                            size * o
                                            - scy
                                            + screen.get_height() / 2
                                            - 19,
                                            size + 19 * 2,
                                            size + 19 * 2,
                                        ),
                                    )
                                elif level[o][p + 1] == 0:
                                    screen.blit(
                                        pygame.transform.rotate(tile1.copy(), 90),
                                        (
                                            size * p - scx + screen.get_width() / 2,
                                            size * o - scy + screen.get_height() / 2,
                                            size,
                                            size,
                                        ),
                                    )
                                else:
                                    screen.blit(
                                        pygame.transform.rotate(tile3.copy(), 90),
                                        (
                                            size * p - scx + screen.get_width() / 2,
                                            size * o - scy + screen.get_height() / 2,
                                            size,
                                            size,
                                        ),
                                    )
                            else:
                                if p + 1 == len(level[o]):
                                    if 0 == p:
                                        screen.blit(
                                            pygame.transform.rotate(tile1.copy(), -90),
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                    elif level[o][p - 1] == 0:
                                        screen.blit(
                                            pygame.transform.rotate(tile1.copy(), -90),
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                    else:
                                        screen.blit(
                                            pygame.transform.rotate(tile3.copy(), -90),
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                elif level[o][p + 1] == 0:
                                    if 0 == p:
                                        screen.blit(
                                            tile3,
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                    elif level[o][p - 1] == 0:
                                        screen.blit(
                                            tile3,
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                    else:
                                        screen.blit(
                                            pygame.transform.rotate(tile3.copy(), 90),
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                else:
                                    if 0 == p:
                                        screen.blit(
                                            tile3,
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                    elif level[o][p - 1] == 0:
                                        screen.blit(
                                            tile3,
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                    else:
                                        # good
                                        screen.blit(
                                            tile4,
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                        elif level[o + 1][p] == 0:
                            if o == 0:
                                if p + 1 == len(level[o]):
                                    if 0 == p:
                                        screen.blit(
                                            pygame.transform.rotate(tile1.copy(), 90),
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                    elif level[o][p - 1] == 0:
                                        screen.blit(
                                            pygame.transform.rotate(tile1.copy(), 90),
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                    else:
                                        pass
                                elif level[o][p + 1] == 0:
                                    screen.blit(
                                        pygame.transform.rotate(tile1.copy(), 90),
                                        (
                                            size * p - scx + screen.get_width() / 2,
                                            size * o - scy + screen.get_height() / 2,
                                            size,
                                            size,
                                        ),
                                    )
                                else:
                                    if 0 == p:
                                        screen.blit(
                                            pygame.transform.rotate(tile1.copy(), 90),
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                    elif level[o][p - 1] == 0:
                                        screen.blit(
                                            pygame.transform.rotate(tile1.copy(), 90),
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                    else:
                                        screen.blit(
                                            tile1,
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                            elif level[o - 1][p] == 0:
                                if p + 1 == len(level[o]):
                                    screen.blit(
                                        pygame.transform.rotate(tile1.copy(), 90),
                                        (
                                            size * p
                                            - scx
                                            + screen.get_width() / 2
                                            - 19,
                                            size * o
                                            - scy
                                            + screen.get_height() / 2
                                            - 19,
                                            size + 19 * 2,
                                            size + 19 * 2,
                                        ),
                                    )
                                elif level[o][p + 1] == 0:
                                    screen.blit(
                                        pygame.transform.rotate(tile1.copy(), 90),
                                        (
                                            size * p - scx + screen.get_width() / 2,
                                            size * o - scy + screen.get_height() / 2,
                                            size,
                                            size,
                                        ),
                                    )
                                else:
                                    screen.blit(
                                        pygame.transform.rotate(tile3.copy(), 90),
                                        (
                                            size * p - scx + screen.get_width() / 2,
                                            size * o - scy + screen.get_height() / 2,
                                            size,
                                            size,
                                        ),
                                    )
                            else:
                                if p + 1 == len(level[o]):
                                    if 0 == p:
                                        screen.blit(
                                            pygame.transform.rotate(tile1.copy(), -90),
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                    elif level[o][p - 1] == 0:
                                        screen.blit(
                                            pygame.transform.rotate(tile1.copy(), -90),
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                    else:
                                        screen.blit(
                                            pygame.transform.rotate(tile3.copy(), -90),
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                elif level[o][p + 1] == 0:
                                    if 0 == p:
                                        screen.blit(
                                            tile3,
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                    elif level[o][p - 1] == 0:
                                        screen.blit(
                                            tile3,
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                    else:
                                        screen.blit(
                                            pygame.transform.rotate(tile3.copy(), 90),
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                else:
                                    if 0 == p:
                                        screen.blit(
                                            tile3,
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                    elif level[o][p - 1] == 0:
                                        screen.blit(
                                            tile3,
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                                    else:
                                        # good
                                        screen.blit(
                                            tile4,
                                            (
                                                size * p - scx + screen.get_width() / 2,
                                                size * o
                                                - scy
                                                + screen.get_height() / 2,
                                                size,
                                                size,
                                            ),
                                        )
                        else:
                            pass"""
        """screen.blit(
            playerSprite,
            (
                screen.get_width() / 2 - scx,
                screen.get_height() / 2 - scy,
            ),
        )"""
        if keys[pygame.K_SPACE]:
            ms = 5
        else:
            ms = 10
        a = 1
        if keys[pygame.K_a]:
            if di == 1:
                di = 0
                playerSprite = pygame.transform.flip(playerSprite, True, False)
            if keys[pygame.K_w] and not onGround:
                vx -= a
                # vx = max(-ms, vx)
            else:
                vx = -ms
        if keys[pygame.K_d]:
            if di == 0:
                di = 1
                playerSprite = pygame.transform.flip(playerSprite, True, False)
            if keys[pygame.K_w] and not onGround:
                vx += a
                # vx = min(ms, vx)
            else:
                vx = ms
        if keys[pygame.K_w]:
            if onGround:
                vy = -7
            elif vy > 0:
                vy = 2
        vx *= 0.8
        fl = 40
        b = 0
        o = -1
        for vmx in range(abs(round(vx))):
            if vx == 0:
                break
            plx += 1 if vx > 0 else -1
            for i in level:
                o += 1
                p = -1
                for j in i:
                    p += 1
                    if j > 0:
                        if vx < 0:
                            try:
                                if (
                                    size * o - ps / 2 <= ply <= o * size + size + ps / 2
                                    and p * size - size / 2 <= plx <= p * size + ps / 4
                                    and level[o][p - 1] == 0
                                ):
                                    plx += 1
                                    vx = 0
                            except Exception:
                                plx += 1
                                vx = 0
                        if vx > 0:
                            try:
                                if (
                                    size * o <= ply <= o * size + size + ps / 2
                                    and p * size + size - ps / 4
                                    <= plx
                                    <= p * size + size + size / 2
                                    and level[o][p + 1] == 0
                                ):
                                    plx -= 1
                                    vx = 0
                            except Exception:
                                plx -= 1
                                vx = 0
        o = -1
        d = 0
        onGround = False
        peak = False
        vy += 5 * dt
        for vmy in range(abs(round(vy))):
            if vy == 0 or onGround:
                break
            if vy > 0:
                ply += 1
            else:
                ply -= 1

            for i in level:
                if onGround:
                    break
                o += 1
                p = -1
                for j in i:
                    if onGround:  # break out of the loop
                        break
                    p += 1
                    if j > 0:
                        if vy > 0:
                            try:
                                if (
                                    size * p - ps / 2 + 1
                                    <= plx
                                    <= p * size + size + ps / 2 - 1
                                    and o * size + size - fl - 48
                                    <= ply
                                    <= o * size + size - fl
                                    and level[o + 1][p] == 0
                                ):
                                    ply -= 1
                                    vy = 0
                                    d = 1
                                    onGround = True
                                    break
                            except Exception:
                                ply -= 1
                                d = 1
                                vy = 0
                                onGround = True
                                break
                        if vy < 0:
                            try:
                                if (
                                    size * p - ps / 4 <= plx <= p * size + size + ps / 4
                                    and o * size - ps / 2 <= ply <= o * size + ps / 2
                                    and level[o - 1][p] == 0
                                ):
                                    ply += 1
                                    vy = 0
                                    peak = True
                                    onGround = True
                            except Exception:
                                ply += 1
                                vy = 0
                                peak = True
                                onGround = True
        if peak:
            onGround = False
        # flip() the display to put your work on screen
        for fearr in fears:
            print(fearr.pos)
            if fearr.dist(ppos=[plx, ply]) > 100 and random.randrange(
                0, 20
            ) <= t % random.randrange(60, 120) <= random.randrange(10, 25):
                screen.fill((40, 0, 0, 10), special_flags=pygame.BLEND_RGB_MIN)
        # screen.fill((40, 0, 0, 10), special_flags=pygame.BLEND_RGB_MIN)
        # screen.blit(overlay, overlay.get_rect(center=screen.get_rect().center))
        for fearr in fears:
            if fearr.agro([plx, ply]):
                fearr.dash([plx, ply])
            fearr.moveToPlayer(
                [plx, ply],
            )
        if flashlight:
            flashlightRect1 = flashlight_image.copy()
            flashlightRect2 = flashlight_image.copy()
            flashlightRect2 = pygame.transform.flip(flashlightRect2, False, True)
            angle = math.degrees(
                math.atan2(
                    pygame.mouse.get_pos()[1] - (ply - scy + screen.get_height() / 2),
                    pygame.mouse.get_pos()[0] - (plx - scx + screen.get_width() / 2),
                )
            )
            flashlightRect1 = pygame.transform.rotate(flashlightRect1, -angle + 15)
            flashlightRect2 = pygame.transform.rotate(flashlightRect2, -angle - 15)
            flashlightRect1_rect = flashlightRect1.get_rect(
                center=(
                    plx - scx + screen.get_width() / 2,
                    ply - scy + screen.get_height() / 2,
                )
            )
            flashlightRect2_rect = flashlightRect2.get_rect(
                center=(
                    plx - scx + screen.get_width() / 2,
                    ply - scy + screen.get_height() / 2,
                )
            )
            screen.blit(flashlightRect1, flashlightRect1_rect)
            screen.blit(flashlightRect2, flashlightRect2_rect)
        else:
            for fearr in fears:
                screen.blit(fearr.image, (fearr.rect.x - scx, fearr.rect.y - scy))
        if t <= 300 and random.randrange(0, 70) != 1:
            ts = text.render(
                "WASD to move, SPACE to use flashlight to see in the dark",
                False,
                (100, 100, 100, 25),
            )
            screen.blit(
                ts,
                (
                    WIDTH / 2 - ts.get_width() / 2,
                    HEIGHT / 2 - ts.get_height() / 2 - 100,
                ),
            )
        """elif t <= 600 and random.randrange(0, 25) != 0:
            ts = text.render(
                "Use the flashlight to see in the dark", False, (255, 255, 255, 50)
        )"""
    if 0 <= vy <= 1:
        screen.blit(
            playerSprite,
            (
                plx - scx + screen.get_width() / 2 - ps / 2,
                ply
                - scy
                + screen.get_height() / 2
                + 20 * math.sin((t - lt) / 20)
                - ps / 2,
            ),
        )
    else:
        lt = t
        screen.blit(
            playerSprite,
            (
                plx - scx + screen.get_width() / 2 - ps / 2,
                ply - scy + screen.get_height() / 2 - ps / 2,
            ),
        )

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
