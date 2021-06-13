from module import *
import pygame as pg

class Main:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(WSIZE)
        pg.display.set_caption(WNAME)
        files.init()
        self.clock = pg.time.Clock()
        self.player = objects.Player(0, 1206)
        self.chanks = []
        self.generate()
        self.mouse = objects.Mouse((255, 0, 0), (0, 0, 255), self.screen, self.player, self.chanks)
        self.items = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
    
    def play(self):
        self.set_chank()
        self.chank.update()
        self.chank2.update()
        self.player.update(self.chank)
        self.items.update()
        self.item_collision()
        self.mobs.update(self.clchank, self.clchank2, self.chanks)
        # for i in self.mobs:
        #     print(i.x, i.y, i.rect.x, i.rect.y)
        #     self.player.x = -i.x
        #     break
    
    def generate(self):
        blocks = [objects.Stone, objects.Dirt, objects.Grass, objects.Bedrock]
        block_list = []
        for x in range(CSIZE):
            block_list.append([3, x-CSIZE//2, 0])
        for x in range(CSIZE):
            for y in range(20):
                block_list.append([0, x-CSIZE//2, y+1])
        for x in range(CSIZE):
            for y in range(4):
                block_list.append([1, x-CSIZE//2, y+21])
        for x in range(CSIZE):
            block_list.append([2, x-CSIZE//2, y+22])
        lst = []
        for coord in block_list:
            coord[1] = coord[1] * BSIZE
            coord[2] = (coord[2]-6) * -BSIZE
            block = blocks[coord[0]](*coord[1:], self.player)
            lst.append(block)
        chank = objects.Chank(lst)
        chank.change_pos(move_x=-25)
        self.chanks.append(chank)
        for i in range(1, 60):
            ch = chank.copy()
            ch.change_pos(move_x=i)
            self.chanks.append(ch)
        self.set_chank()
    
    def set_chank(self):
        try:
            global SPAWNCHANK
            index = abs(55-(((self.player.x-WWIDTH//2)//BSIZE-CSIZE//2)//CSIZE+SPAWNCHANK))
            self.clchank = self.chanks[index]
            self.chank = self.clchank.get_group()
            if ((self.player.x-WWIDTH//2)//BSIZE-CSIZE//2)%CSIZE < CSIZE//2:
                self.clchank2 = self.chanks[index+1]
            else:
                self.clchank2 = self.chanks[index-1]
            self.chank2 = self.clchank2.get_group()
        except:
            pass
    
    def item_collision(self):
        taked = pg.sprite.groupcollide(self.player.sprites, self.items, False, False)
        for item in taked:
            if item.take:
                item.collision()
                self.items.remove(item)

    def draw(self):
        self.screen.fill(WHITE)
        self.chank.draw(self.screen)
        self.chank2.draw(self.screen)
        self.items.draw(self.screen)
        self.mobs.draw(self.screen)
        self.player.draw(self.screen)
        self.mouse.block()
        pg.display.update()
        # pg.time.delay(3000)

    def run(self):
        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.mouse.set_block()
                    elif event.button == 3:
                        self.mouse.del_block()
            
            # pr = pg.mouse.get_pressed()
            # if pr[0]:
            #     self.mouse.set_block()
            # elif pr[2]:
            #     self.mouse.del_block()

            self.play()
            self.draw()
            self.clock.tick(FPS)
        pg.quit()

if __name__ == '__main__':
    game = Main()
    game.run()