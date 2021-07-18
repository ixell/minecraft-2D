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
        self.generate(seed)

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

    def generate(self, seed):
        random.seed(seed)
        procent = random.randint(0, 100)
        wood_procent = random.randint(0, 100)
        cave_procent = 0
        caves = []
        add_y = 0
        for i in range(1, 60):
            block_list = []
            block_pos_list = []
            for x in range(CSIZE):
                block_pos_list.append([x-CSIZE//2, DEFAULT_Y+add_y])
                block_list.append(2)
                for y in range(3):
                    block_pos_list.append([x-CSIZE//2, DEFAULT_Y+add_y+y-3])
                    block_list.append(1)
                for y in range(DEFAULT_Y+add_y-4):
                    block_pos_list.append([x-CSIZE//2, DEFAULT_Y+add_y-y-4])
                    block_list.append(3)
                block_pos_list.append([x-CSIZE//2, 0])
                block_list.append(5)
                procent += random.randint(-2, 7)
                cave_procent += random.randint(2, 8)
                wood_procent += random.randint(2, 10)
                if procent > 100: procent = 100
                if wood_procent > 100: wood_procent = 100
                if wood_procent - random.randint(1, 100) >= 0:
                    if not 3 <= x <= 15:
                        wood_procent //= 4
                    else:
                        wood_size = DEFAULT_WOOD_SIZE + random.randint(0, 2)
                        for y in range(wood_size):
                            block_pos_list.append([x - CSIZE//2, DEFAULT_Y+add_y+1+y])
                            block_list.append(9)
                        for y in range(5):
                            for x2 in range(5):
                                if y >= 3 and (x2 == 0 or x2 == 4): continue
                                pos = [x2+x-CSIZE//2-2, DEFAULT_Y+add_y+wood_size+(y-1)]
                                if not pos in block_pos_list:
                                    block_pos_list.append(pos)
                                    block_list.append(10)
                        wood_procent = -30
                if cave_procent - random.randint(1, 100) >= 0:
                    cave_procent = 0
                    caves.append([x-CSIZE//2, add_y+DEFAULT_Y, random.randint(1, 4), random.randint(25, 75), 0, random.randint(0, 100)])
                    self.player.x = x + CSIZE * (len(self.chanks))
                    print(len(caves))
                for indx, cave_state in enumerate(caves):
                    cave_state[0] += 1
                    if cave_state[1] > DEFAULT_Y + add_y:
                        del caves[indx]
                        continue
                    cave_state[5] += random.randint(-2, 4)
                    if cave_state[5] - random.randint(1, 100) >= 0:
                        if cave_state[2] > 4: cave_state[2] -= random.randint(1, 2)
                        elif cave_state[2] <= 1: cave_state[2] += random.randint(1, 2)
                        else: cave_state[2] += random.randint(-1, 1)
                        cave_state[5] = random.randint(-5, 10)
                    elif cave_state[1] >= (DEFAULT_Y+add_y) - 10:
                        cave_state[3] += random.randint(2, 8)
                        cave_state[4] += random.randint(1, 3)
                    elif cave_state[1] > 7:
                        cave_state[4] += random.randint(2, 8)
                        cave_state[3] += random.randint(1, 3)
                    else: cave_state[4] += random.randint(7, 12)
                    for y in range(1, cave_state[2]+1):
                        if [cave_state[0], y+cave_state[1]-cave_state[2]] in block_pos_list:
                            index = block_pos_list.index([cave_state[0], y+cave_state[1]-cave_state[2]])
                            if block_list[index] == 5: continue
                            del block_pos_list[index]
                            del block_list[index]
                        # print(block_pos_list[indx])
                            print([cave_state[0], y+cave_state[1]-cave_state[2]])
                            # print(y, cave_state[1], cave_state[2])
                        # pg.time.delay(200)
                            # block_list[index] = 4
                    if cave_state[3] - random.randint(1, 100) >= 0:
                        if cave_state[3] <= 10: cave_state[1] -= 1
                        elif 10 < cave_state[3] <= 20: cave_state[1] -= 2
                        elif 20 < cave_state[3] <= 40: cave_state[1] -= 3
                        elif cave_state[3] > 40: cave_state[1] -= 4
                        cave_state[3] -= 10
                    if cave_state[4] - random.randint(1, 100) >= 0:
                        if cave_state[4] <= 10: cave_state[1] += 1
                        elif 10 < cave_state[4] <= 20: cave_state[1] += 2
                        elif 20 < cave_state[4] <= 40: cave_state[1] += 3
                        elif cave_state[4] > 40: cave_state[4] += 4
                        cave_state[4] -= 10
                if random.randint(1, 100) - procent <= 0:
                    if add_y >= 6: add = -1
                    elif add_y <= 0: add = 1
                    else: add = random.choice((1, -1))
                    if 7 - random.randint(1, 100) > 0: add *= 2
                    add_y += add
                    procent = 0
            lst = []
            for indx, coord in enumerate(block_pos_list):
                coord[0] = coord[0] * BSIZE
                coord[1] = (coord[1]-6) * -BSIZE
                block = self.blocks_id[block_list[indx]](*coord, self.player)
                lst.append(block)
            chank = objects.Chank(lst)
            chank.change_pos(move_x=-26+i)
            self.chanks.append(chank)
        self.set_chank()

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
