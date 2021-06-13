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
        image = files.blocks['Grass']
        super().__init__(x, y, player, image)

class Dirt(Block):
    def __init__(self, x, y, player):
        image = files.blocks['Dirt']
        super().__init__(x, y, player, image)

class Stone(Block):
    def __init__(self, x, y, player):
        image = files.blocks['Stone']
        super().__init__(x, y, player, image)

class Bedrock(Block):
    def __init__(self, x, y, player):
        image = files.blocks['Bedrock']
        super().__init__(x, y, player, image, False)

class CobbleStone(Block):
    def __init__(self, x, y, player):
        image = files.blocks['CobbleStone']
        super().__init__(x, y, player, image)