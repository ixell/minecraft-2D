import pygame as pg
from module.settings import *
import math as m
import files
from module.interface import *

class Mouse:
    def __init__(self, bad, good, screen, player, chanks):
        self.bad = bad
        self.good = good
        self.screen = screen
        self.player = player
        self.chanks = chanks

    def block(self):
        mpos = pg.mouse.get_pos()
        pg.draw.rect(self.screen, self.good, ((mpos[0]-self.player.x%BSIZE)//BSIZE*BSIZE+self.player.x%BSIZE,
         (mpos[1]-self.player.y%BSIZE)//BSIZE*BSIZE+self.player.y%BSIZE, BSIZE, BSIZE), 4)

    def select(self):
        mpos = list(pg.mouse.get_pos())
        chank = 56 - abs(((self.player.x)//BSIZE)//CSIZE+SPAWNCHANK)
        mpos[0] = ((mpos[0]-self.player.x%BSIZE)//BSIZE-self.player.x//BSIZE)*BSIZE
        mpos[1] = ((mpos[1]-self.player.y%BSIZE)//BSIZE-self.player.y//BSIZE)*BSIZE
        return self.chanks[chank].get_group(), mpos

    def half_mode_select(self, c):
        mpos = pg.mouse.get_pos()
        c = mpos[0] + self.player.x if c == 'x' else mpos[1] + self.player.y
        res = 0 if c % BSIZE > BSIZE//2+1 else BSIZE//2
        return res

    def set_block(self, block):
        chank, pos = self.select()
        for obj in chank:
            if obj.x == pos[0] and obj.y == pos[1]:
                return False
        # block = CobbleStoneHB(pos[0], pos[1], self.player)
        block = block(*pos, self.player)
        if block.hb_mode: block.move = (0, self.half_mode_select('y'))
        chank.add(block)
        return True

    def del_block(self):
        chank, pos = self.select()
        for obj in chank:
            if obj.x == pos[0] and obj.y == pos[1]:
                if obj.destructible:
                    chank.remove(obj)
                    return pos, obj.id, True
                return (-1, -1), 0, False
        return (-1, -1), 0, False

class Image(pg.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def move_to(self, pos):
        self.last_rect = self.rect
        self.rect.x, self.rect.y = pos

    def move(self, pos):
        self.last_rect = self.rect
        self.rect.x += pos[0]
        self.rect.y += pos[1]

    def update(self, pos):
        self.move_to(pos)

    def copy(self):
        return self.__class__(self.image, (self.rect.x, self.rect.y))

    def rerect(self, x):
        self.rect = self.image.get_rect(x=x, y=self.rect.y)

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, img=None):
        super().__init__()
        self.images = files.player
        self.resprite(1)
        self.direction = 1
        self.sprites_move_to((WWIDTH//2-self.body.rect.width//2-self.lhand.rect.width,
                              WHEIGHT//2-self.body.rect.height//2-self.head.rect.height), True)
        self.x, self.y = (x, y)
        self.change_y = self.change_x = 0
        self.rect = pg.Rect(self.lhand.rect.x, self.head.rect.y,
            self.body.rect.width,
            self.head.rect.height + self.body.rect.height + self.lleg.rect.height)
        self.rots = {'lhand': [0, -1], 'rhand': [0, 1], 'lleg': [0, -1], 'rleg': [0, 1]}
        self.speed = PSPE

    def sprites_move_to(self, pos, orig=False):
        if self.direction in (0, 2):
            self.head.move_to((pos[0] + self.lhand.rect.w, pos[1]))
            self.lhand.move_to((pos[0], pos[1] + self.head.rect.h))
            self.body.move_to((pos[0] + self.lhand.rect.w, pos[1] + self.head.rect.h))
            self.rhand.move_to((pos[0] + self.rhand.rect.w + self.body.rect.w, 
                pos[1] + self.head.rect.h))
            self.lleg.move_to((pos[0] + self.lhand.rect.w,
                pos[1] + self.head.rect.h + self.body.rect.h))
            self.rleg.move_to((pos[0] + self.lhand.rect.w + self.lleg.rect.w,
                            pos[1] + self.body.rect.h + self.head.rect.h))
        elif self.direction in (1, 3):
            self.head.move_to((pos[0] + self.lhand.rect.w - self.body.rect.w//2,
                pos[1]))
            self.lhand.move_to((pos[0] + self.lhand.rect.w, pos[1] + self.head.rect.h))
            self.body.move_to((pos[0] + self.lhand.rect.w, pos[1] + self.head.rect.h))
            self.rhand.move_to((pos[0] + self.lhand.rect.w, pos[1] + self.head.rect.h))
            self.lleg.move_to((pos[0] + self.lhand.rect.w, 
            pos[1] + self.head.rect.h + self.body.rect.h))
            self.rleg.move_to((pos[0] + self.lhand.rect.w, 
            pos[1] + self.head.rect.h + self.body.rect.h))
        if orig:
            for i in (self.lhand, self.rhand, self.head, self.body, self.lleg, self.rleg):
                i.orig_rect = i.rect.copy()

    def sprites_rotate(self):
        self.lhand.image = pg.transform.rotate(self.lhand.original_image, self.rots['lhand'][0])
        self.rhand.image = pg.transform.rotate(self.rhand.original_image, self.rots['rhand'][0])
        self.lleg.image = pg.transform.rotate(self.lleg.original_image, self.rots['lleg'][0])
        self.rleg.image = pg.transform.rotate(self.rleg.original_image, self.rots['rleg'][0])
        for n, i in (('rleg', self.rleg), ('rhand', self.rhand), ('lleg', self.lleg), ('lhand', self.lhand)):
            _ = i.rerect(i.orig_rect.right-i.rect.w) if self.rots[n][0] < 0 else i.rerect(i.orig_rect.x+i.rect.width-i.rect.w)
        self.rots['rleg'][0] += self.rots['rleg'][1]*2
        self.rots['lleg'][0] += self.rots['lleg'][1]*2
        self.rots['rhand'][0] += self.rots['rhand'][1]*2
        self.rots['lhand'][0] += self.rots['lhand'][1]*2
        for k in self.rots:
            if abs(self.rots[k][0]) >= 65:
                self.rots[k][1] = -self.rots[k][1]

    def sprites_move(self, pos):
        # print('move:', pos)
        self.body.move(pos)
        self.head.move(pos)
        self.lleg.move(pos)
        self.rleg.move(pos)
        self.lhand.move(pos)
        self.rhand.move(pos)

    def resprite(self, num):
        self.sprites = pg.sprite.Group()
        self.body = Image(self.images['body'][num], (0, 0))
        self.head = Image(self.images['head'][num], (0, 0))
        self.lleg = Image(self.images['leg'][num], (0, 0))
        self.rleg = self.lleg.copy()
        self.lhand = Image(self.images['hand'][num], (0, 0))
        self.rhand = self.lhand.copy()
        self.sprites.add(self.head, self.rleg, self.lleg, self.body,
                         self.rhand, self.lhand)
        # self.sprites.add(self.head)

    def update(self, chank):
        self.move(chank)
        self.collision(chank)
        self.change_x = 0

    def draw(self, screen):
        self.sprites.draw(screen)

    def jump(self, chank):
        self.rect.y += 2
        cpd = pg.sprite.spritecollide(self, chank, False)
        pd = []
        self.rect.y -= 4
        for block in cpd:
            if not block.through:
                pd.append(block)
        pdb = bool(pd)
        if pd:
            cpd = pg.sprite.spritecollide(self, chank, False)
            pd = []
            for block in cpd:
                if not block.through:
                    pd.append(block)
            pdb = not bool(pd)
        self.rect.y += 2
        if pdb or self.y <= self.lleg.rect.height:
            self.change_y = 5 * ((self.rect.height) // BSIZE)

    def back(self, rotate):
        self.lleg.image = pg.transform.flip(self.lleg.original_image, rotate, False)
        self.rleg.image = pg.transform.flip(self.rleg.original_image, rotate, False)
        self.lhand.image = pg.transform.flip(self.lhand.original_image, rotate, False)
        self.rhand.image = pg.transform.flip(self.rhand.original_image, rotate, False)
        self.body.image = pg.transform.flip(self.body.original_image, rotate, False)
        self.head.image = pg.transform.flip(self.head.original_image, rotate, False)

    def move(self, chank):
        self.grav()
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_RIGHT] or keys[pg.K_a] or keys[pg.K_d]:
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.change_x += self.speed
                self.back(False)
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.change_x -= self.speed
                self.back(True)
            self.sprites_rotate()
        else:
            self.rots = {'lhand':[0, 1], 'rhand':[0, -1], 'lleg':[0, 1], 'rleg':[0, -1]}
            self.sprites_rotate()       
        if keys[pg.K_UP] or keys[pg.K_w] or keys[pg.K_SPACE]:
            self.jump(chank)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            pass

    def collision(self, chank):
        x, y = (self.rect.x, self.rect.y)
        self.rect.x += self.change_x
        cbhl = pg.sprite.spritecollide(self, chank, False)
        bhl = []
        cb = False
        for block in cbhl:
            if not block.through:
                bhl.append(block)
        if bool(bhl):
            self.rect.x = x
            nbhl = pg.sprite.spritecollide(self, chank, False)
            for i, block in enumerate(nbhl):
                if block.through: del nbhl[i]
            if not bool(nbhl):
                obj = bhl[0]
                if self.change_x > 0:
                    cb = obj.collision(self, 'x+')
                    self.rect.right = obj.rect.left
                else:
                    cb = obj.collision(self, 'x-')
                    self.rect.left = obj.rect.right
        cb = False
        self.rect.y -= self.change_y
        cbhl = pg.sprite.spritecollide(self, chank, False)
        bhl = []
        for block in cbhl:
            if not block.through:
                bhl.append(block)
        if bool(bhl):
            self.rect.y = y
            cnbhl = pg.sprite.spritecollide(self, chank, False)
            nbhl = []
            for block in cnbhl:
                if not block.through:
                    nbhl.append(block)
            if not bool(nbhl):
                obj = bhl[0]
                if self.change_y > 0:
                    cb = obj.collision(self, 'y-')
                    self.rect.top = obj.rect.bottom
                    if not cb: self.change_y *= -0.25
                else:
                    cb = obj.collision(self, 'y+')
                    self.rect.bottom = obj.rect.top
                    if not cb: self.change_y = 0
        cx = self.rect.x - x
        cy = self.rect.y - y
        self.cmove(cx, cy)
        self.rect.x = x
        self.rect.y = y

    def cmove(self, x, y):
        self.x -= x
        self.y -= y

    def grav(self):
        if self.change_y == 0:
            self.change_y = -1
        else:
            self.change_y -= .25
        self.change_y = max(-BSIZE, self.change_y)

        if self.y - self.lleg.rect.height <= 0:
            self.y = self.lleg.rect.height
            self.change_y = PSPE


class Block(pg.sprite.Sprite):
    def __init__(self, x, y, player, image, id, destructible=True, size=(1, 1), hb_mode=False, through=False):
        super().__init__()
        self.image = image
        self.image = self.image.subsurface((0, 0, int(size[0]*BSIZE), int(size[1]*BSIZE)))
        self.rect = self.image.get_rect()
        self.x, self.y = (x, y)
        self.player = player
        self.destructible = destructible
        self.id = id
        self.move = (0, 0)
        self.hb_mode = hb_mode
        self.through = through
        self.update()
        #self.rect.x, self.rect.y = self.x

    def update(self):
        self.rect.x = self.player.x + self.x + self.move[0]
        self.rect.y = self.player.y + self.y + self.move[1]

    def copy(self):
        copy = self.__class__(self.x, self.y, self.player)
        return copy

    def collision(self, mob, coord):
        return False


class Grass(Block):
    def __init__(self, x, y, player):
        image = files.blocks['Grass']
        super().__init__(x, y, player, image, 1)

class Dirt(Block):
    def __init__(self, x, y, player):
        image = files.blocks['Dirt']
        super().__init__(x, y, player, image, 1)

class Stone(Block):
    def __init__(self, x, y, player):
        image = files.blocks['Stone']
        super().__init__(x, y, player, image, 4)

class Bedrock(Block):
    def __init__(self, x, y, player):
        image = files.blocks['Bedrock']
        super().__init__(x, y, player, image, 5, destructible=False)

class CobbleStone(Block):
    def __init__(self, x, y, player):
        image = files.blocks['CobbleStone']
        super().__init__(x, y, player, image, 4)

class CobbleStoneHB(Block):
    def __init__(self, x, y, player):
        image = files.blocks['CobbleStone']
        super().__init__(x, y, player, image, 6, size=(1, 0.5), hb_mode=True)

class SlimeBlock(Block):
    def __init__(self, x, y, player):
        image = files.blocks['SlimeBlock']
        super().__init__(x, y, player, image, 7)

    def collision(self, mob, coord):
        if 'y' in coord: mob.change_y = (mob.change_y - 1) * -0.5
        return True

class Fire(Block):
    def __init__(self, x, y, player):
        image = files.blocks['Fire']
        super().__init__(x, y, player, image, 8, through=True, destructible=False)

class Wood(Block):
    def __init__(self, x, y, player):
        image = files.blocks['Wood']
        super().__init__(x, y, player, image, 9, through=True)

class Leaves(Block):
    def __init__(self, x, y, player):
        image = files.blocks['Leaves']
        super().__init__(x, y, player, image, 10)


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
    def __init__(self, x, y, player, image, name, take, id=None):
        super().__init__()
        self.image = image
        self.image = pg.transform.scale(self.image, (ISIZE, ISIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.player = player
        self.name = name
        self.change_y = 0
        self.take = take
        if id!=None: self.id = id

    def update(self, chank):
        self.rect.x = self.player.x + self.x
        self.rect.y = self.player.y + self.y
        self.grav(chank)
        self.y += self.change_y
    
    def grav(self, chank):
        self.rect.y -= 8
        col = pg.sprite.spritecollide(self, chank, False)
        if bool(col):
            y = self.rect.y
            self.change_y = 0
            self.rect.bottom = col[0].rect.top
            self.y += self.rect.y - y
        else:
            self.change_y = 8
        self.rect.y += 8

    def collision(self):
        return self.player.inventory.add(self.id, 1)


class TestItem(Item):
    def __init__(self, x, y, player, name='test item', take=True):
        image = pg.Surface((ISIZE, ISIZE))
        image.fill((200, 150, 0))
        super().__init__(x, y, player, image, name, take)

    def collision(self):
        self.player.change_y = 8


class ItemDirt(Item):
    def __init__(self, x, y, player, name='dirt', take=True):
        id = 1
        image = 'files/textures/' + items[id].split('  ')[1]
        image = pg.image.load(image).convert_alpha()
        super().__init__(x, y, player, image, name, take, id=id)

class ItemGrass(Item):
    def __init__(self, x, y, player, name='grass', take=True):
        id = 2
        image = 'files/textures/' + items[id].split('  ')[1]
        image = pg.image.load(image).convert_alpha()
        super().__init__(x, y, player, image, name, take, id=id)

class ItemStone(Item):
    def __init__(self, x, y, player, name='stone', take=True):
        id = 3
        image = 'files/textures/' + items[id].split('  ')[1]
        image = pg.image.load(image).convert_alpha()
        super().__init__(x, y, player, image, name, take, id=id)

class ItemCobbleStone(Item):
    def __init__(self, x, y, player, name='cobblestone', take=True):
        id = 4
        image = 'files/textures/' + items[id].split('  ')[1]
        image = pg.image.load(image).convert_alpha()
        super().__init__(x, y, player, image, name, take, id=id)

class ItemBedrock(Item):
    def __init__(self, x, y, player, name='bedrock', take=True):
        id = 5
        image = 'files/textures/' + items[id].split('  ')[1]
        image = pg.image.load(image).convert_alpha()
        super().__init__(x, y, player, image, name, take, id=id)

class ItemCobbleStoneHB(Item):
    def __init__(self, x, y, player, name='cobblestone HB', take=True):
        id = 6
        image = 'files/textures/' + items[id].split('  ')[1]
        image = pg.image.load(image).subsurface((0, 0, ISIZE, ISIZE//2)).convert_alpha()
        super().__init__(x, y, player, image, name, take, id=id)

class ItemSlimeBlock(Item):
    def __init__(self, x, y, player, name='slime block', take=True):
        id = 7
        image = 'files/textures/' + items[id].split('  ')[1]
        image = pg.image.load(image).convert_alpha()
        super().__init__(x, y, player, image, name, take, id=id)

class ItemWood(Item):
    def __init__(self, x, y, player, name='oak log', take=True):
        id = 9
        image = 'files/textures/' + items[id].split('  ')[1]
        image = pg.image.load(image).convert_alpha()
        super().__init__(x, y, player, image, name, take, id=id)

class ItemLeaves(Item):
    def __init__(self, x, y, player, name='oak leaves', take=True):
        id = 10
        image = 'files/textures/' + items[id].split('  ')[1]
        image = pg.image.load(image).convert_alpha()
        super().__init__(x, y, player, image, name, take, id=id)


class Mob(pg.sprite.Sprite):
    def __init__(self, x, y, player, speed, size=(2, 1)):
        super().__init__()
        self.image = pg.Surface((size[0]*BSIZE, size[1]*BSIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.change_x = 0
        self.change_y = 0
        self.player = player
        self.speed = speed

    def update(self, chank1, chank2, chanks):
        self.rect.x = self.player.x + self.x + self.change_x
        self.rect.y = self.player.y + self.y - abs(self.player.change_y)
        index = abs(55-(((-self.x)//BSIZE-CSIZE//2)//CSIZE+SPAWNCHANK))
        if chanks[index] == chank1 or chanks[index] == chank2:
            chank = chanks[index].get_group()
        else:
            return
        self.move(chank)

    def move(self, chank):
        self.grav(chank)
        self.collision(chank)
        self.change_x = 0

    def jump(self, chank):
        pd = pg.sprite.spritecollide(self, chank, False)
        if not pd:
            self.rect.y += 2
            pd = bool(pg.sprite.spritecollide(self, chank, False))
            self.rect.y -= 4
            if pd:
                pd = not bool(pg.sprite.spritecollide(self, chank, False))
            self.rect.y += 2
            if pd or self.y <= self.rect.height:
                # min(BSIZE, max(8, 5 * ((self.rect.height) // BSIZE)))
                self.change_y = 10

    def collision(self, chank):
        x, y = (self.rect.x, self.rect.y)
        self.change_x = -self.change_x
        self.rect.x -= self.change_x + self.player.change_x
        col = pg.sprite.spritecollide(self, chank, False)
        if bool(col):
            self.rect.x = x
            if not bool(pg.sprite.spritecollide(self, chank, False)):
                block = col[0]
                if self.change_x > 0:
                    self.rect.left = block.rect.right
                else:
                    self.rect.right = block.rect.left
                self.jump(chank)
            self.change_x = 0
        self.rect.y -= self.change_y
        col = pg.sprite.spritecollide(self, chank, False)
        if bool(col):
            self.rect.y = y
            if bool(pg.sprite.spritecollide(self, chank, False)):
                block = col[0]
                if self.change_y < 0:
                    self.rect.bottom = block.rect.top
                    self.change_y = 0
                else:
                    self.rect.top = block.rect.bottom
                    self.change_y *= -.25
            else:
                self.change_y = 0
        cx = x - self.rect.x
        cy = self.rect.y - y
        self.cmove(cx, cy)
        self.rect.x = x
        self.rect.y = y

    def cmove(self, x, y):
        self.x -= x
        self.y += y

    def grav(self, chank):
        if self.change_y == 0:
            self.change_y = -1
        else:
            self.change_y -= .25
