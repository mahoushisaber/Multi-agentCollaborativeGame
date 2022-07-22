import pygame

class GroundSprite(pygame.sprite.Sprite):

    def __init__(self, color, rect):
        super().__init__()
        (x1, y1, x2, y2) = rect
        self.image = pygame.Surface([x2 - x1, y2 - y1])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = x1
        self.rect.y = y1

        self.speed_map = dict()

    def update_speed(self, obj, speed: float):
        self.speed_map[obj] = speed

    def get_speed(self, obj) -> float:
        if obj in self.speed_map:
            return self.speed_map[obj]
        return 1.0
