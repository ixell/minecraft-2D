from constants import *
import objects
import pygame as pg
BSIZE *= 10

class Main:
    def __init__(self):
        self.screen = pg.display.set_mode(WSIZE)
        pg.display.set_caption(WNAME)
        self.clock = pg.time.Clock()
        self.block_sprites = pg.sprite.Group()
        self.player = objects.Player(0, 1000, None, (1, 2))
        self.generate()
        self.mouse = objects.Mouse((255, 0, 0), (0, 0, 255), self.screen, self.player)
    
    def play(self):
        self.player.update(self.block_sprites)
        self.block_sprites.update()
    
    def generate(self):
        blocks = [objects.Block]
        block_list = [
            [0, 1, 7],
            [0, 6, 0],
            [0, 6, 1]
        ]
        for x in range(20):
            for y in range(8):
                block_list.append([0, x-20, y+4])
        for coord in block_list:
            coord[1] = coord[1] * BSIZE
            coord[2] = (coord[2]-8) * -BSIZE
            block = blocks[coord[0]](*coord[1:], self.player)
            self.block_sprites.add(block)
    
    def draw(self):
        self.screen.fill(WHITE)
        self.block_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.mouse.block()
        pg.display.update()

    def run(self):
        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.mouse.set_block(self.block_sprites)
                    elif event.button == 3:
                        self.mouse.del_block(self.block_sprites)
            
            pg.display.update()
            self.play()
            self.draw()
            self.clock.tick(FPS)
        pg.quit()

if __name__ == '__main__':
    game = Main()
    game.run()