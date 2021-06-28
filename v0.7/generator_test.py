import pygame as pg
import random
random.seed(528349)
screen2 = pg.display.set_mode((400, 500))
screen = pg.Surface((400, 500))
generate = lambda y: (   (25-y)%256   ,)*3
procent = 12
run = True
add_x = 0
add_y = 0
clock = pg.time.Clock()
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    move = screen2.subsurface(20, 0, 380, 500)
    screen.blit(move, (0, 0))
    add_x += 1
    for y in range(25):
        pg.draw.rect(screen, generate(y+add_y+2), (380, y*20, 20, 20))
    procent += random.randint(-1, 5)
    if procent > 100: procent = 100
    if random.randint(1, 100) - procent <= 0:
        print(add_y)
        if add_y >= 6: add = -1
        elif add_y <= 0: add = 1
        else: add = random.choice((1, -1))
        add_y += add
        procent = 0
    clock.tick(20)
    screen2.blit(screen, (0, 0))
    pg.display.update()