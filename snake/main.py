import pygame
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
ds = pygame.display.set_mode(
    size=[1280, 720],
    flags=RESIZABLE
)
delta = 0

# Actual game canvas
canvas_size = min(ds.get_width(), ds.get_height())
canvas = pygame.Surface([canvas_size, canvas_size])
canvas.fill([100, 255, 100])
canvas_rect = canvas.get_rect()
canvas_rect.center = (ds.get_width() / 2, ds.get_height() / 2)

GRID_AMOUNT_IN_A_ROW = 30
grid_size = canvas_size / GRID_AMOUNT_IN_A_ROW


class Snake:
    snake_tail = [(0, 0), (1, 0), (2, 0)]

    def __init__(self, controller: dict):
        self.controller = controller

    def handle_movement(self, pressed_keys: dict):
        pass


def draw_grid(surface: pygame.Surface):
    for x in range(0, GRID_AMOUNT_IN_A_ROW):
        for y in range(0, GRID_AMOUNT_IN_A_ROW):
            rect = pygame.Rect((x * grid_size), (y * grid_size), grid_size, grid_size)
            pygame.draw.rect(surface, (0, 0, 0), rect, 1)


snake = Snake({
    K_w: 0,
    K_d: 1,
    K_s: 2,
    K_a: 3
})

while True:

    ds.fill([255, 255, 255])

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        elif event.type == VIDEORESIZE:

            ds = pygame.display.set_mode(
                size=event.dict['size'],
                flags=RESIZABLE
            )

            canvas_size = min(ds.get_width(), ds.get_height())
            canvas = pygame.transform.scale(canvas, [canvas_size, canvas_size])
            canvas_rect = canvas.get_rect()
            canvas_rect.center = (ds.get_width() / 2, ds.get_height() / 2)
            grid_size = canvas_size / GRID_AMOUNT_IN_A_ROW

            pygame.display.flip()

    pressed_keys = pygame.key.get_pressed()
    snake.handle_movement(pressed_keys)

    draw_grid(canvas)
    ds.blit(canvas, canvas_rect)
    pygame.display.update()
    delta = clock.tick(60)
