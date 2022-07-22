from tokenize import group
import pygame

ACTION_NOOP = 0
ACTION_UP = 1
ACTION_RIGHT = 2
ACTION_DOWN = 3
ACTION_LEFT = 4

ACTIONS = [ACTION_NOOP, ACTION_UP, ACTION_RIGHT, ACTION_DOWN, ACTION_LEFT]

NUM_ACTIONS = len(ACTIONS)


class PlayerSprite(pygame.sprite.Sprite):

    def __init__(self, color, pos, width, height, main_ground, player_ground, obstacles, speed=5):
        super().__init__()
        self.main_ground = main_ground
        self.player_ground = player_ground
        self.obstacles = obstacles
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.dx = 0
        self.dy = 0
        self.init_pos = pos
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.speed = speed
        self.carrying = None

    def update(self):
        orig_x = self.rect.x
        orig_y = self.rect.y

        self.rect.x += self.dx
        self.rect.y += self.dy

        # move back if the player moved out of movable grounds
        obstacles = pygame.sprite.spritecollide(self, self.obstacles, False, PlayerSprite.obstacle_collide)
        if not self.main_ground.contains(self.rect) or len(obstacles) > 0:
            self.rect.x = orig_x
            self.rect.y = orig_y
        if self.carrying:
            for obstacle in obstacles:
                if isinstance(obstacle, PlayerSprite):
                    self.carrying.carry_by(obstacle)

        self.dx = 0
        self.dy = 0

    def step(self, action):
        if action == ACTION_NOOP:
            return
        ground = pygame.sprite.spritecollideany(
            self, self.player_ground, PlayerSprite.inside_by_middle)
        if ground is None:
            return
        slowdown_factor = ground.get_speed(self)
        delta = self.speed // slowdown_factor
        if action == ACTION_UP:
            self.dy -= delta
        elif action == ACTION_RIGHT:
            self.dx += delta
        elif action == ACTION_DOWN:
            self.dy += delta
        elif action == ACTION_LEFT:
            self.dx -= delta

    def reset(self):
        self.rect.topleft = self.init_pos
        self.carrying = None

    @staticmethod
    def inside_by_middle(player, ground):
        return ground.rect.collidepoint(player.rect.center)

    @staticmethod
    def obstacle_collide(player, obstacle):
        if player == obstacle:
            return False
        return player.rect.colliderect(obstacle.rect)
