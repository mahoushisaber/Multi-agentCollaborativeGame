import pygame

class ScoreSprite(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        # self.image.fill(color)
        self.value = 0
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.image = self.font.render('Score: ' + str(self.value), True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
    
    def update(self):
        self.image = self.font.render('Score: ' + str(self.value), True, (255, 255, 255))