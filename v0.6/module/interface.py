import pygame as pg
# from module.settings import *
items = open('files/objects/items.txt', 'r')
items2 = items.readlines()
items.close()
items = items2

class Slot:
    def __init__(self, item_id, count=0):
        self.id = item_id
        self.line = items[self.id].strip().split('  ')
        self.name = self.line[0]
        self.image = pg.image.load('files/textures/' + self.line[1]).convert_alpha()
        self.rect = self.image.get_rect()
        self.use = self.line[2]
        self.other = self.line[3:]
        self.hb_mode = False
        if self.use == 'block' and len(self.other) > 0 and 'HB' in self.other:
            self.image = self.image.subsurface(0, 0, self.rect.w, self.rect.h//2)
            hb_mode = True
        self.rect = self.image.get_rect()
        self.count = count

    def normalize(self):
        if self.count <= 0:
            self.id = 0
            self.reID(0)
        if self.count > 64: self.count = 64
        if self.id == 0: self.count = 0

    def reID(self, new_id):
        self.id = new_id
        self.line = items[self.id].strip().split('  ')
        self.name = self.line[0]
        self.image = pg.image.load('files/textures/' + self.line[1]).convert_alpha()
        self.rect = self.image.get_rect()
        self.use = self.line[2]
        self.other = self.line[3:]
        hb_mode = False
        if self.use == 'block' and 'HB' in self.other:
            self.image = self.image.subsurface(0, 0, self.rect.w, self.rect.h//2)
            hb_mode = True
        self.rect = self.image.get_rect()
        self.count = 1

class HotBar:
    def __init__(self, pos, screen):
        self.pos = pos
        self.screen = screen
        self.slots = [Slot(0) for _ in range(9)]
        self.original_image = pg.image.load('files/textures/hotbar.png').convert_alpha()
        self.original_image = pg.transform.scale(self.original_image, (400, 50))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.width = self.rect.width//8
        self.xwidth = self.rect.width//9
        self.hotslot_image = pg.image.load('files/textures/hotslot.png')
        self.hotslot_image = pg.transform.scale(self.hotslot_image, (50, 50))
        self.hotslot = 0
        self.font = pg.font.SysFont(None, 20)

    def draw(self):
        self.image = self.original_image.copy()
        self.image.blit(self.hotslot_image, (self.hotslot * self.xwidth, 0))
        for x, slot in enumerate(self.slots):
            if slot.id != 0:
                self.image.blit(slot.image, ((self.width - slot.rect.w)//2 + x * self.xwidth, 0 + (self.rect.h - slot.rect.h)//2))
                count = self.font.render(str(slot.count), True, (170, 170, 170))
                crect = count.get_rect()
                self.image.blit(count, (x * self.xwidth + self.width - crect.width - 10, self.width - crect.height - 5))
        self.screen.blit(self.image, self.pos)

    def rms(self, method:str, *values):
        ret = {}
        for index, slot in enumerate(self.slots):
            ret[index] = slot.__getattribute__(method)(*values)
        return ret

    def choice(self, event):
        if event.type == pg.KEYDOWN:
            if str(chr(event.key)) in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
                self.hotslot = int(str(chr(event.key)))-1
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 5:
                self.hotslot = (self.hotslot+1)%9
            elif event.button == 4:
                self.hotslot = (self.hotslot-1) if self.hotslot-1 > -1 else 8

    def clear(self, count:int=-1, slot='useing'):
        if slot.__class__ != int: slot = self.hotslot
        if count > -1:
            self.slots[slot].count -= count
        else:
            self.slots[slot].count = 0
            self.slots[slot].id = 0

    def set(self, id:int, slot:int, count:int=1):
        self.slots[slot].reID(id)
        self.slots[slot].count = count

    def normalize(self):
        self.rms('normalize')

    def get_hotslot(self):
        return self.slots[self.hotslot]
    
    def add_air(self, id:int, count:int=1):
        first = count
        for slot in self.slots:
            if slot.id == 0:
                slot.reID(id)
                slot.count = count
                return True
        if first != count:
            return count
        return False

    def add(self, id:int, count:int=1):
        for slot in self.slots:
            if slot.use == 'block':
                if slot.id == id and slot.count < 64:
                    slot.count += count
                    if slot.count > 64:
                        count = slot.count - 64
                        slot.count.normalize()
                        continue
                    return True
        return False

class Inventory:
    def __init__(self, pos, hotbar:HotBar):
        self.pos = pos
        self.hotbar = hotbar
        self.screen = self.hotbar.screen
        self.original_image = pg.image.load('files/textures/inventory.png').convert_alpha()
        rect = self.original_image.get_rect()
        self.original_image = pg.transform.scale(self.original_image, (rect.w*2, rect.h*2))
        self.rect = self.original_image.get_rect()
        self.image = self.original_image.copy()
        self.active = False
        self.slots = {'hotbar':self.hotbar.slots, 'inventory':[Slot(0) for _ in range(27)], 'armor':
        {'head':Slot(0), 'legs':Slot(0), 'chest':Slot(0), 'feet':Slot(0)}} # head - голова, legs - штаны, chest - нагрудник, feet - ботинки
        self.width = 36
        self.font = self.hotbar.font
        self.move_slot = Slot(0)
        self.move_slot.last = None

        self.set(6, 0, 64)
        self.set(7, 1, 64)

    def set(self, id:int, slot:int, count:int=1):
        self.slots['inventory'][slot].reID(id)
        self.slots['inventory'][slot].count = count
    
    def add(self, id:int, count:int=1):
        hb = self.hotbar.add(id, count)
        if hb: return True
        for slot in self.slots['inventory']:
            if slot.use == 'block':
                if slot.id == id and slot.count < 64:
                    slot.count += count
                    return True
        hb = self.hotbar.add_air(id, count)
        if hb: return True
        elif hb.__class__ == int: count = hb
        for slot in self.slots['inventory']:
            if slot.id == 0:
                slot.reID(id)
                slot.count = count
                return True
        return False

    def open(self):
        self.active = True

    def close(self):
        self.move_slot.last = None
        self.active = False

    def OO(self):
        if self.active: self.close()
        else: self.open()

    def draw(self):
        if self.active:
            self.image = self.original_image.copy()
            for c, slot in enumerate(self.slots['inventory']):
                if slot.id != 0:
                    pos = (c%9*36+24, c//9*36+175)
                    self.image.blit(slot.image, pos)
                    if slot.count > 1:
                        count = self.font.render(str(slot.count), True, (75, 75, 75))
                        crect = count.get_rect()
                        self.image.blit(count, (pos[0] + self.width - crect.width - 12, pos[1] + self.width - crect.height - 12))
            for x, slot in enumerate(self.slots['hotbar']):
                if slot.id != 0:
                    pos = (x*36+24, 290)
                    self.image.blit(slot.image, pos)
                    if slot.count > 1:
                        count = self.font.render(str(slot.count), True, (75, 75, 75))
                        crect = count.get_rect()
                        self.image.blit(count, (pos[0] + self.width - crect.width - 12, pos[1] + self.width - crect.height - 12))
            for y, slot in enumerate(self.slots['armor'].values()):
                if slot.id != 0:
                    pos = (24, y*36 + 24)
                    self.image.blit(slot.image, pos)
            self.screen.blit(self.image, self.pos)
            if self.move_slot.last != None:
                mpos = pg.mouse.get_pos()
                self.screen.blit(self.move_slot.image,
                 (mpos[0] + self.move_slot.rect.w + 3,
                 mpos[1] + self.move_slot.rect.h + 3))

    def move(self, rc=False):
        if self.active:
            mpos = pg.mouse.get_pos()
            slot_x = (mpos[0] - 12 - self.pos[0]) // 36
            slot_y = (mpos[1] - 163 - self.pos[1]) // 36
            if 0 <= slot_x < 9 and 0 <= slot_y < 3:
                slot = self.slots['inventory'][slot_x + slot_y * 9]
            else:
                slot = (mpos[0] - 12 - self.pos[0]) // 36
                if not 0 <= slot < 9 or not 278 <= mpos[1]-self.pos[1] <= 314: slot = None
                else: slot = self.slots['hotbar'][slot]
            if self.move_slot.last == None:
                if slot != None and slot.id != 0:
                    self.move_slot.reID(slot.id)
                    self.move_slot.last = slot
                    if rc and slot.count > 1:
                        self.move_slot.count = slot.count//2
                        slot.count -= self.move_slot.count
                    else:
                        self.move_slot.count = slot.count
                        slot.reID(0)
            elif slot != None:
                if slot == self.move_slot.last:
                    if rc:
                        if slot.id == 0: slot.reID(self.move_slot.id)
                        else: slot.count += 1
                        self.move_slot.count -= 1
                        self.move_slot.normalize()
                        if self.move_slot.id == 0: self.move_slot.last = None
                        return
                    else:
                        if slot.id == 0: slot.reID(self.move_slot.id)
                        else: slot.count += 1
                        slot.count = self.move_slot.count + slot.count - 1
                elif slot.id == self.move_slot.id:
                    if rc:
                        self.move_slot.count -= 1
                        slot.count += 1
                        self.move_slot.normalize()
                        if self.move_slot.id == 0: self.move_slot.last = None
                    else:
                        slot.count += self.move_slot.count
                        self.move_slot.last.reID(self.move_slot.id)
                        self.move_slot.last.count = slot.count - 64 if slot.count - 64 > 0 else 0
                        self.move_slot.last.normalize()
                        slot.normalize()
                else:
                    save = (slot.id, slot.count)
                    if rc and save[0] == 0:
                        slot.reID(self.move_slot.id)
                        self.move_slot.count -= 1
                        self.move_slot.normalize()
                        if self.move_slot.id == 0: self.move_slot.last = None
                        return
                    slot.reID(self.move_slot.id)
                    slot.count = self.move_slot.count
                    if self.move_slot.last.id == 0:
                        self.move_slot.last.reID(save[0])
                        self.move_slot.last.count = save[1]
                    elif save[0] != 0:
                        slot.reID(0)
                        slot.normalize()
                        self.move_slot.last = slot
                        self.move_slot.reID(save[0])
                        self.move_slot.count = save[1]
                        return
                self.move_slot.last = None
            else:
                self.move_slot.last = None

if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((700, 700))
    run = True
    hb = HotBar((0, 0), screen)
    inv = Inventory((100, 100), hb)
    inv.open()
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1: inv.move()
                elif event.button == 3: inv.move(True)
        inv.draw()
        pg.display.update()
    pg.quit()