import pygame as pg
from constants import *
BSIZE *= 10

class Mouse:
    def __init__(self, bad, good, screen, player):
        self.bad = bad
        self.good = good
        self.screen = screen
        self.player = player
    
    def block(self):
        mpos = pg.mouse.get_pos()
        pg.draw.rect(self.screen, self.good, (mpos[0]//BSIZE*BSIZE+self.player.x%BSIZE, mpos[1]//BSIZE*BSIZE+self.player.y%BSIZE, BSIZE, BSIZE), 4)
    
    def select(self, chank):
        mpos = list(pg.mouse.get_pos())
        mpos[0] = (mpos[0]//BSIZE-self.player.x//BSIZE)*BSIZE
        mpos[1] = (mpos[1]//BSIZE-self.player.y//BSIZE)*BSIZE
        return mpos

    def set_block(self, chank):
        mpos = self.select(chank)
        for obj in chank:
            if obj.x == mpos[0] and obj.y == mpos[1]:
                return
        block = Block(mpos[0], mpos[1], self.player)
        chank.add(block)
    
    def del_block(self, chank):
        mpos = self.select(chank)
        for obj in chank:
            if obj.x == mpos[0] and obj.y == mpos[1]:
                chank.remove(obj)
                return

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, img=None, size=(1, 2)):
        super().__init__()
        self.image = pg.Surface((size[0] * BSIZE, size[1] * BSIZE)) #pg.image.load(img)
        pg.draw.rect(self.image, (0, 255, 0), (0, 0, size[0]*BSIZE-1, size[1]*BSIZE-1), 2)
        self.rect = self.image.get_rect()
        self.rect.x = WWIDTH // 2 - self.rect.width // 2
        self.rect.y = WHEIGHT // 2 - self.rect.height // 2
        self.x, self.y = (x, y)
        self.change_y = self.change_x = 0
    
    def update(self, cmap):
        self.move(cmap)
        self.collision(cmap)
        self.change_x = 0
    
    def jump(self, cmap):
        self.rect.y += 2
        pd = bool(pg.sprite.spritecollide(self, cmap, False))
        self.rect.y -= 4
        if pd:
            pd = not bool(pg.sprite.spritecollide(self, cmap, False))
        self.rect.y += 2
        if pd or self.y <= self.rect.height:
            self.change_y = 5 * (self.rect.height // BSIZE)

    def move(self, cmap):
        self.grav(cmap)
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.change_x += 8
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.change_x -= 8
        if keys[pg.K_UP] or keys[pg.K_w] or keys[pg.K_SPACE]: self.jump(cmap)
        if keys[pg.K_DOWN] or keys[pg.K_s]: pass
    
    def collision(self, cmap):
        x, y = (self.rect.x, self.rect.y)
        self.rect.x += self.change_x
        bhl = pg.sprite.spritecollide(self, cmap, False)
        if bool(bhl):
            self.rect.x = x
            if not bool(pg.sprite.spritecollide(self, cmap, False)):
                obj = bhl[0]
                if self.change_x > 0:
                    self.rect.right = obj.rect.left
                else:
                    self.rect.left = obj.rect.right
            else:
                self.change_x = 0
        self.rect.y -= self.change_y
        bhl = pg.sprite.spritecollide(self, cmap, False)
        if bool(bhl):
            self.rect.y = y
            if not bool(pg.sprite.spritecollide(self, cmap, False)):
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

    def grav(self, cmap):
        if self.change_y == 0:
            self.change_y = -1
        else:
            self.change_y -= .25
        
        if self.y - self.rect.height <= 0:
            self.y = self.rect.height
            self.change_y = 0

class Block(pg.sprite.Sprite):
    def __init__(self, x, y, player, texture=None):
        super().__init__()
        self.image = pg.Surface((BSIZE, BSIZE))
        pg.draw.rect(self.image, RED, (0, 0, BSIZE-1, BSIZE-1), 2)
        self.rect = self.image.get_rect()
        self.x, self.y = (x, y)
        self.player = player
        self.update()
        #self.rect.x, self.rect.y = self.x

    def update(self):
        self.rect.x = self.player.x + self.x
        self.rect.y = self.player.y + self.y