import pygame

class DestSprite(pygame.sprite.Sprite):

    def __init__(self, color, pos, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]