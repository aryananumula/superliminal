import pygame
import math
import json
import random

import create

# import fear
pygame.mixer.init()

pygame.mixer.music.load("sounds/ambient.mp3")
pygame.mixer.music.play(-1)
di = 0
# grid = create.OO0OOO0000O0OOOO0(64)
grid = create.gm(8)

# open("level1.json", "w").write(str(grid.tolist()))

# pygame setup

pygame.init()
screen = pygame.display.set_mode((1280, 720), vsync=1)
clock = pygame.time.Clock()
# fear1 = fear.Fear(screen, "something")
running = True
dt = 0

ps = 64

plx, ply = ps / 2, ps / 2
scx, scy = plx, ply

playerSprite = pygame.image.load("images/player.png")
playerSprite = pygame.transform.scale(playerSprite, (ps, ps))

overlay = pygame.image.load("images/overlay.png")
overlay = pygame.transform.scale(overlay, (1280 * 1.5, 720 * 1.5))

level = json.load(open("level1.json"))

t = -1
j = 10
onGround = True


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


vy = 0
vx = 0
while running:
    t += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    scx = round(scx + (plx - scx) / 10)
    scy = round(scy + (ply - scy) / 10)
    screen.fill("#0D0E0E")
    o = -1
    r = 5
    size = 256
    for i in level:
        o += 1
        p = -1
        for j in i:
            p += 1
            if j == 1:
                if size * p - (r) * size < plx < p * size + size * (
                    1 + r
                ) and size * o - (r) * size < ply < o * size + size * (1 + r):
                    pygame.draw.rect(
                        screen,
                        "#19191A",
                        (
                            size * p - scx + screen.get_width() / 2,
                            size * o - scy + screen.get_height() / 2,
                            size,
                            size,
                        ),
                    )
    screen.blit(
        playerSprite,
        (
            screen.get_width() / 2 - scx,
            screen.get_height() / 2 - scy,
        ),
    )

    screen.blit(
        playerSprite,
        (
            plx - scx + screen.get_width() / 2 - ps / 2,
            ply - scy + screen.get_height() / 2 + 10 * math.sin(t / 20) - ps / 2,
        ),
    )

    keys = pygame.key.get_pressed()
    vy += 5 * dt
    if keys[pygame.K_SPACE]:
        ms = 5
    else:
        ms = 10

    if keys[pygame.K_a]:
        if keys[pygame.K_w] and not onGround:
            vx -= 1
            vx = max(-ms, vx)
        else:
            vx = -ms
    if keys[pygame.K_d]:
        if keys[pygame.K_w] and not onGround:
            vx += 1
            vx = min(ms, vx)
        else:
            vx = ms
    if keys[pygame.K_w]:
        if onGround:
            vy = -7
        elif vy > 0:
            vy = 2
    vx *= 0.8
    fl = 32
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
                if j == 1:
                    if vx < 0:
                        try:
                            if (
                                size * o <= ply <= o * size + size
                                and p * size <= plx <= p * size + ps / 2
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
                                size * o <= ply <= o * size + size
                                and p * size + size - ps / 2 <= plx <= p * size + size
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
                if j == 1:
                    if vy > 0:
                        try:
                            if (
                                size * p <= plx <= p * size + size
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
                                size * p <= plx <= p * size + size
                                and o * size <= ply <= o * size + fl
                                and level[o - 1][p] == 0
                            ):
                                print("hit")
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
    if (
        random.randrange(0, 20)
        <= t % random.randrange(60, 120)
        <= random.randrange(10, 25)
    ):
        screen.fill((40, 0, 0, 10), special_flags=pygame.BLEND_RGB_MIN)
    if (
        random.randrange(0, 20)
        <= t % random.randrange(60, 120)
        <= random.randrange(10, 25)
    ):
        screen.blit(overlay, overlay.get_rect(center=screen.get_rect().center))
    pygame.display.flip()
    # fear1.moveToPlayer(plx, ply, [])
    # fear1.draw()
    dt = clock.tick(60) / 1000

pygame.quit()
