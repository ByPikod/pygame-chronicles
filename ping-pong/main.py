import sys
import math
from collections.abc import Sequence

import pygame
from pygame.locals import *

WIDTH = 512
HEIGHT = 512


class Entity(pygame.sprite.Sprite):

    def __init__(self, rect: Rect):
        super().__init__()
        self.rect = rect

    def get_width(self) -> int:
        return self.rect.width

    def get_height(self) -> int:
        return self.rect.height

    def get_x(self) -> int:
        return self.rect.x

    def get_y(self) -> int:
        return self.rect.y


class Ball(Entity):
    direction = -90
    speed = 0.2

    def __init__(self, screen_width: int, screen_height: int):

        self.surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        super().__init__(self.surf.get_rect())

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rect.topleft = (
            screen_width / 2 - self.surf.get_width() / 2,
            screen_height / 2 - self.surf.get_height() / 2
        )

        self.location = float(self.rect.top), float(self.rect.left)
        self.image = pygame.image.load("ball.png").convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, self.rect.size)
        self.surf.blit(self.image, (0, 0))

    def handle_movement(self, delta_time, collision_group: list[Entity]):

        collision = self.check_collision(collision_group)
        if collision:
            return

        directionRadian = math.radians(self.direction)
        self.location = (
            self.location[0] + math.sin(directionRadian) * self.speed * delta_time,
            self.location[1] + math.cos(directionRadian) * self.speed * delta_time
        )

        self.rect.topleft = (
            int(self.location[0]),
            int(self.location[1])
        )

    def check_collision(self, collision_group: list[Entity]) -> Entity | None:

        for sprite in collision_group:

            if (
                sprite.get_x() < self.get_x() + self.get_width() and
                sprite.get_x() + sprite.get_width() > self.get_x() and
                sprite.get_y() < self.get_y() + self.get_height() and
                sprite.get_y() + sprite.get_height() > self.get_y()
            ):
                return sprite

        return None


class Player(Entity):

    def __init__(self, controller: dict):

        self.surf = pygame.Surface((20, 120))
        self.surf.fill((0, 0, 0))

        super().__init__(self.surf.get_rect())

        self.controller: dict = controller
        self.speed: float = 0.5
        self.axis: float = 0.0

    def handle_movement(self, keys: Sequence[bool], delta_time: int, screen_height: int):

        if keys[self.controller["up"]]:
            self.axis -= self.speed * delta_time

        if keys[self.controller["down"]]:
            self.axis += self.speed * delta_time

        if self.axis < 0:
            self.axis = 0
        if self.get_height() + self.axis + 10 > screen_height - 50:
            self.axis = screen_height - self.get_height() - 10 - 50
        self.rect.top = 50 + self.axis


class Game:

    def __init__(self, width, height):

        pygame.init()
        pygame.display.set_caption("Ping Pong")

        self.clock = pygame.time.Clock()
        self.display_surface = pygame.display.set_mode((width, height))

        self.startTicks = pygame.time.get_ticks()
        self.mainFont = pygame.font.Font('fredoka-one.ttf', 16)
        self.fps = (0, 0)
        self.delta_time = 0

        self.header = pygame.Surface((self.screen_width(), 40))
        self.header.get_rect().topleft = (0, 0)

        ply1_controller = {
            "up": K_w,
            "down": K_s
        }
        self.ply1 = Player(ply1_controller)
        self.ply1.rect.topleft = (10, 50)

        ply2_controller = {
            "up": K_UP,
            "down": K_DOWN
        }
        self.ply2 = Player(ply2_controller)
        self.ply2.rect.topleft = (self.screen_width() - self.ply2.get_width() - 10, 50)
        self.ball = Ball(self.screen_width(), self.screen_height())

        self.__loop()

    def get_ticks(self) -> int:
        return pygame.time.get_ticks() - self.startTicks

    def calculate_fps(self):

        fps, lastFpsTime = self.fps
        ticks = self.get_ticks()

        if lastFpsTime + 300 < ticks:
            fps = self.clock.get_fps()
            lastFpsTime = ticks
            self.fps = (int(fps), lastFpsTime)

    def screen_width(self) -> int:
        return self.display_surface.get_width()

    def screen_height(self) -> int:
        return self.display_surface.get_height()

    def get_delta_time(self) -> int:
        return self.delta_time

    def __loop(self):

        while True:

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return 0

            self.display_surface.fill((255, 255, 255))
            self.calculate_fps()

            fps_text = self.mainFont.render(f"FPS: {self.fps[0]}", True, (255, 255, 255))
            fps_text_rect = fps_text.get_rect()
            fps_text_rect.topleft = (10, 10)

            keys = pygame.key.get_pressed()

            height = self.screen_height()
            delta_time = self.get_delta_time()

            self.ply1.handle_movement(keys, delta_time, height)
            self.ply2.handle_movement(keys, delta_time, height)
            self.ball.handle_movement(delta_time, (self.ply1, self.ply2))

            self.display_surface.blit(self.header, self.header.get_rect())
            self.display_surface.blit(self.ply1.surf, self.ply1.rect)
            self.display_surface.blit(self.ply2.surf, self.ply2.rect)
            self.display_surface.blit(self.ball.surf, self.ball.rect)
            self.display_surface.blit(fps_text, fps_text_rect)

            pygame.display.update()
            self.delta_time = self.clock.tick(0)


if __name__ == "__main__":
    game = Game(WIDTH, HEIGHT)
    sys.exit(0)
