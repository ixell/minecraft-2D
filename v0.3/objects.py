import pygame as pg
from constants import *
import math as m

class Mouse:
    def __init__(self, bad, good, screen, player, chanks):
        self.bad = bad
        self.good = good
        self.screen = screen
        self.player = player
        self.chanks = chanks
    
    def block(self):
        mpos = pg.mouse.get_pos()
        pg.draw.rect(self.screen, self.good, (mpos[0]//BSIZE*BSIZE+self.player.x%BSIZE, mpos[1]//BSIZE*BSIZE+self.player.y%BSIZE, BSIZE, BSIZE), 4)
    
    def select(self):
        mpos = list(pg.mouse.get_pos())
        chank = abs(19-(((self.player.x-mpos[0])//BSIZE-CSIZE//2)//CSIZE+SPAWNCHANK))%20
        mpos[0] = (mpos[0]//BSIZE-self.player.x//BSIZE)*BSIZE
        mpos[1] = (mpos[1]//BSIZE-self.player.y//BSIZE)*BSIZE
        return self.chanks[chank].get_group(), mpos

    def set_block(self):
        chank, pos = self.select()
        for obj in chank:
            if obj.x == pos[0] and obj.y == pos[1]:
                return
        block = Stone(pos[0], pos[1], self.player)
        chank.add(block)
    
    def del_block(self, items):
        chank, pos = self.select()
        for obj in chank:
            if obj.x == pos[0] and obj.y == pos[1]:
                if obj.destructible:
                    chank.remove(obj)
                    items.add(TestItem(pos[0], -pos[1], self.player, take=True))
                return

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, img=None, size=(1, 2)):
        super().__init__()
        self.image = pg.Surface((size[0] * BSIZE, size[1] * BSIZE)) #pg.image.load(img)
        self.image.fill((50, 200, 100))
        self.rect = self.image.get_rect()
        self.rect.x = WWIDTH // 2 - self.rect.width // 2
        self.rect.y = WHEIGHT // 2 - self.rect.height // 2
        self.x, self.y = (x, y)
        self.change_y = self.change_x = 0
    
    def update(self, chank):
        self.move(chank)
        self.collision(chank)
        self.change_x = 0
    
    def jump(self, chank):
        self.rect.y += 2
        pd = bool(pg.sprite.spritecollide(self, chank, False))
        self.rect.y -= 4
        if pd:
            pd = not bool(pg.sprite.spritecollide(self, chank, False))
        self.rect.y += 2
        if pd or self.y <= self.rect.height:
            self.change_y = 5 * ((self.rect.height) // BSIZE)

    def move(self, chank):
        self.grav(chank)
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.change_x += 8
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.change_x -= 8
        if keys[pg.K_UP] or keys[pg.K_w] or keys[pg.K_SPACE]:
            self.jump(chank)
        if keys[pg.K_DOWN] or keys[pg.K_s]: pass
    
    def collision(self, chank):
        x, y = (self.rect.x, self.rect.y)
        self.rect.x += self.change_x
        bhl = pg.sprite.spritecollide(self, chank, False)
        if bool(bhl):
            self.rect.x = x
            if not bool(pg.sprite.spritecollide(self, chank, False)):
                obj = bhl[0]
                if self.change_x > 0:
                    self.rect.right = obj.rect.left
                else:
                    self.rect.left = obj.rect.right
            else:
                self.change_x = 0
        self.rect.y -= self.change_y
        bhl = pg.sprite.spritecollide(self, chank, False)
        if bool(bhl):
            self.rect.y = y
            if not bool(pg.sprite.spritecollide(self, chank, False)):
                obj = bhl[0]
                if self.change_y > 0:
                    self.rect.top = obj.rect.bottom
                    self.change_y *= -0.25
                else:
                    self.rect.bottom = obj.rect.top
                    self.change_y = 0
            else:
                self.change_y = 0
        cx = self.rect.x - x
        cy = self.rect.y - y
        self.cmove(cx, cy)
        self.rect.x = x
        self.rect.y = y
    
    def cmove(self, x, y):
        self.x -= x
        self.y -= y

    def grav(self, chank):
        if self.change_y == 0:
            self.change_y = -1
        else:
            self.change_y -= .25
        
        if self.y - self.rect.height <= 0:
            self.y = self.rect.height
            self.change_y = 0

class Block(pg.sprite.Sprite):
    def __init__(self, x, y, player, image, destructible=True):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.x, self.y = (x, y)
        self.player = player
        self.destructible = destructible
        self.update()
        #self.rect.x, self.rect.y = self.x

    def update(self):
        self.rect.x = self.player.x + self.x
        self.rect.y = self.player.y + self.y
    
    def copy(self):
        copy = self.__class__(self.x, self.y, self.player)
        return copy

class Grass(Block):
    def __init__(self, x, y, player):
        image = pg.Surface((BSIZE, BSIZE))
        pg.draw.rect(image, GREEN, (0, 0, BSIZE, BSIZE), 4)
        super().__init__(x, y, player, image)

class Dirt(Block):
    def __init__(self, x, y, player):
        image = pg.Surface((BSIZE, BSIZE))
        pg.draw.rect(image, BROWN, (0, 0, BSIZE, BSIZE), 4)
        super().__init__(x, y, player, image)

class Stone(Block):
    def __init__(self, x, y, player):
        image = pg.Surface((BSIZE, BSIZE))
        pg.draw.rect(image, GRAY, (0, 0, BSIZE, BSIZE), 4)
        super().__init__(x, y, player, image)

class Unbreakable(Block):
    def __init__(self, x, y, player):
        image = pg.Surface((BSIZE, BSIZE))
        super().__init__(x, y, player, image, False)

class Chank:
    def __init__(self, generation):
        self.map = pg.sprite.Group()
        self.map.add(*generation)
    
    def get_group(self):
        return self.map
    
    def change_pos(self, move_x=0, move_y=0):
        for obj in self.map:
            obj.x += move_x * BSIZE * CSIZE
            obj.y += move_y * BSIZE * CSIZE
    
    def copy(self):
        new_map = []
        for original in self.map:
            clone = original.copy()
            new_map.append(clone)
        new_map = pg.sprite.Group(new_map)
        return self.__class__(new_map)

class Item(pg.sprite.Sprite):
    def __init__(self, x, y, player, image, name, take):
        super().__init__()
        self.image = image
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = -y
        self.player = player
        self.name = name
        self.change_y = 0
        self.s = 0
        self.take = take
    
    def update(self):
        self.rect.x = self.player.x + self.x
        self.rect.y = self.player.y + self.y + self.change_y
        self.change_y += m.sin(self.s)
        self.s += 0.05
    
    def collision(self):
        return

class TestItem(Item):
    def __init__(self, x, y, player, name='test item', take=True):
        image = pg.Surface((ISIZE, ISIZE))
        image.fill(YELLOW)
        super().__init__(x, y, player, image, name, take)
    
    def collision(self):
        self.player.change_y = 8