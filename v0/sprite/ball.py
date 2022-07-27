import pygame

class BallSprite(pygame.sprite.Sprite):

    def __init__(self, color, pos, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.spwan_pos = pos
        self.carrier = None

    def update(self):
        if self.carrier:
            self.rect.center = self.carrier.rect.center

    def carry_by(self, carrier):
        if self.carrier:
            self.carrier.carrying = None
        self.carrier = carrier
        self.carrier.carrying = self

    def respawn(self):
        self.rect.topleft = self.spwan_pos
        if self.carrier is not None:
            self.carrier.carrying = None
            self.carrier = None
    
    @staticmethod
    def ball_find_carrier(ball, player):
        if ball.owner is player:
            return False
        return ball.rect.collidepoint(player.rect.center)