import random, module.objects as objects
from module.settings import *

class Generator:
    def generate(self, seed, blocks_id, player):
        random.seed(seed)
        self.blocks_id = blocks_id
        self.player = player
        self.chanks = []
        self.procent = random.randint(0, 100)
        self.wood_procent = random.randint(0, 100)
        self.cave_procent = 0
        self.caves = []
        self.add_y = 0
        for self.i in range(1, 61):
            self.generate_chank()
            print(str(round(self.i/60*100)) + '%')
        return self.chanks

    def generate_chank(self):
        self.block_list = []
        self.block_pos_list = []
        for self.x in range(CSIZE):
            self.generate_relef()
            # self.change_relef()
            # self.generate_trees()
            # self.create_caves()
            # self.generate_caves()

        lst = []
        for indx, coord in enumerate(self.block_pos_list):
            coord[0] = coord[0] * BSIZE
            coord[1] = (coord[1]-6) * -BSIZE
            block = self.blocks_id[self.block_list[indx]](*coord, self.player)
            lst.append(block)
            chank = objects.Chank(lst)
            chank.change_pos(move_x=-26+self.i)
            self.chanks.append(chank)

    def generate_relef(self):
        self.block_pos_list.append([self.x-CSIZE//2, DEFAULT_Y+self.add_y])
        self.block_list.append(2)
        for y in range(3):
            self.block_pos_list.append([self.x-CSIZE//2, DEFAULT_Y+self.add_y+y-3])
            self.block_list.append(1)
        for y in range(DEFAULT_Y+self.add_y-4):
            self.block_pos_list.append([self.x-CSIZE//2, DEFAULT_Y+self.add_y-y-4])
            self.block_list.append(3)
        self.block_pos_list.append([self.x-CSIZE//2, 0])
        self.block_list.append(5)

    def change_relef(self):
        self.procent += random.randint(-2, 7)
        self.cave_procent += random.randint(-2, 4)
        self.wood_procent += random.randint(2, 10)
        if self.procent > 100: self.procent = 100
        if self.wood_procent > 100: self.wood_procent = 100
        if self.cave_procent > 100: self.cave_procent = 100

        if random.randint(1, 100) - self.procent <= 0:
            if self.add_y >= 6: add = -1
            elif self.add_y <= 0: add = 1
            else: add = random.choice((1, -1))
            if 7 - random.randint(1, 100) > 0: add *= 2
            self.add_y += add
            procent = 0

    def generate_trees(self):
        if self.wood_procent - random.randint(1, 100) >= 0:
            if not 3 <= self.x <= 15:
                self.wood_procent //= 4
            else:
                wood_size = DEFAULT_WOOD_SIZE + random.randint(0, 2)
                for y in range(wood_size):
                    self.block_pos_list.append([self.x - CSIZE//2, DEFAULT_Y+self.add_y+1+y])
                    self.block_list.append(9)
                for y in range(5):
                    for x2 in range(5):
                        if y >= 3 and (x2 == 0 or x2 == 4): continue
                        pos = [x2+self.x-CSIZE//2-2, DEFAULT_Y+self.add_y+wood_size+(y-1)]
                        if not pos in self.block_pos_list:
                            self.block_pos_list.append(pos)
                            self.block_list.append(10)
                self.wood_procent = -30

    def create_caves(self):
        if self.cave_procent - random.randint(1, 100) >= 0:
            self.cave_procent = 0
            self.caves.append([self.x-CSIZE//2, self.add_y+DEFAULT_Y, random.randint(1, 4), random.randint(25, 75), 0, random.randint(0, 100)])

    def generate_caves(self):
        for indx, cave_state in enumerate(self.caves):
            cave_state[0] += 1
            if cave_state[1] > DEFAULT_Y + self.add_y:
                del self.caves[indx]
                continue
            cave_state[5] += random.randint(-2, 4)
            if cave_state[5] - random.randint(1, 100) >= 0:
                if cave_state[2] > 4: cave_state[2] -= random.randint(1, 2)
                elif cave_state[2] <= 1: cave_state[2] += random.randint(1, 2)
                else: cave_state[2] += random.randint(-1, 1)
                cave_state[5] = random.randint(-5, 10)
            elif cave_state[1] >= (DEFAULT_Y+self.add_y) - 10:
                cave_state[3] += random.randint(2, 8)
                cave_state[4] += random.randint(1, 3)
            elif cave_state[1] > 7:
                cave_state[4] += random.randint(2, 8)
                cave_state[3] += random.randint(1, 3)
            else: cave_state[4] += random.randint(7, 12)
            for y in range(1, cave_state[2]+1):
                if [cave_state[0], y+cave_state[1]-cave_state[2]] in self.block_pos_list:
                    index = self.block_pos_list.index([cave_state[0], y+cave_state[1]-cave_state[2]])
                    if self.block_list[index] == 5: continue
                    del self.block_pos_list[index]
                    del self.block_list[index]
                # print(self.block_pos_list[indx])
                    # print([cave_state[0], y+cave_state[1]-cave_state[2]])
                    # print(y, cave_state[1], cave_state[2])
                # pg.time.delay(200)
                    # self.block_list[index] = 4
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