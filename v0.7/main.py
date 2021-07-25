from module import *
import pygame as pg
import random

class Main:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(WSIZE)
        pg.display.set_caption(WNAME)
        files.init()
        self.clock = pg.time.Clock()
        self.player = objects.Player(0, DEFAULT_Y*BSIZE+7*BSIZE+6)
        self.chanks = []
        self.mouse = objects.Mouse(
            (255, 0, 0), (0, 0, 255), self.screen, self.player, self.chanks)
        self.items = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.hotbar = objects.HotBar((175, 0), self.screen)
        self.hotbar.pos = (WWIDTH//2 - self.hotbar.rect.w//2, 0)
        self.inventory = objects.Inventory((0, 0), self.hotbar)
        self.inventory.pos = (WWIDTH//2-self.inventory.rect.w//2, WHEIGHT//2-self.inventory.rect.h//2)
        self.player.inventory = self.inventory
        self.blocks_id = {1: objects.Dirt, 2: objects.Grass, 3: objects.Stone, 4: objects.CobbleStone,
                          5: objects.Bedrock, 6:objects.CobbleStoneHB, 7:objects.SlimeBlock, 8:objects.Fire, 9:objects.Wood, 
                          10:objects.Leaves}
        self.items_id = {1: objects.ItemDirt, 2: objects.ItemGrass, 3: objects.ItemStone, 4: objects.ItemCobbleStone,
                         5: objects.ItemBedrock, 6:objects.ItemCobbleStoneHB, 7:objects.ItemSlimeBlock, 9:objects.ItemWood,
                         10:objects.ItemLeaves}
        seed = random.randint(0, 999999999999)
        print('seed: ' + str(seed))
        self.generator = generator.Generator()
        self.chanks = self.generator.generate(seed, self.blocks_id, self.player)
        self.set_chank()

    def play(self):
        self.player.speed = PSPE
        self.set_chank()
        self.hotbar.normalize()
        self.chank.update()
        self.chank2.update()
        self.player.update(self.chank, self.chank2)
        self.items.update(self.clchank, self.clchank2, self.chanks)
        self.item_collision()
        self.mobs.update(self.clchank, self.clchank2, self.chanks)
        # for i in self.mobs:
        #     print(i.x, i.y, i.rect.x, i.rect.y)
        #     self.player.x = -i.x
        #     break

    def set_chank(self):
        global SPAWNCHANK
        index = 56 - abs(self.player.x//BSIZE//CSIZE+SPAWNCHANK)
        self.clchank = self.chanks[index]
        self.chank = self.clchank.get_group()
        if ((self.player.x-WWIDTH//2-self.player.rect.w//2)//BSIZE-CSIZE//2) % CSIZE < CSIZE//2:
            self.clchank2 = self.chanks[index+1]
        else: self.clchank2 = self.chanks[index-1]
        self.chank2 = self.clchank2.get_group()

    def item_collision(self):
        taked = pg.sprite.spritecollide(self.player, self.items, False, False)
        for item in taked:
            if item.take:
                if item.collision():
                    self.items.remove(item)

    def draw(self):
        self.screen.fill((135, 206, 235))
        self.items.draw(self.screen)
        self.chank.draw(self.screen)
        self.chank2.draw(self.screen)
        self.mobs.draw(self.screen)
        self.player.draw(self.screen)
        if not self.inventory.active: 
            self.mouse.draw()
            self.hotbar.draw()
        self.inventory.draw()
        pg.display.update()

    def run(self):
        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if not self.inventory.active:
                        if event.button == 1:
                            if self.hotbar.get_hotslot().count > 0:
                                if self.mouse.set_block(self.blocks_id[self.hotbar.get_hotslot().id]):
                                    self.hotbar.clear(count=1)
                        elif event.button == 3:
                            block_pos, block_id, block_bool = self.mouse.del_block()
                            if block_bool:
                                block_pos = (block_pos[0]+(BSIZE-ISIZE)//2, block_pos[1]+(BSIZE-ISIZE)//2)
                                item = self.items_id[block_id](*block_pos, self.player)
                                self.items.add(item)
                    else:
                        if event.button == 1: self.inventory.move()
                        elif event.button == 3: self.inventory.move(True)
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_e:
                        self.inventory.OO()
                self.hotbar.choice(event)
            self.play()
            self.draw()
            self.clock.tick(FPS)
        pg.quit()

if __name__ == '__main__':
    game = Main()
    game.run()
