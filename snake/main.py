import pygame
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
ds = pygame.display.set_mode(
    size=[1280, 720],
    flags=HWSURFACE | DOUBLEBUF | RESIZABLE
)
delta = 0

# Actual game canvas
canvas_size = min(ds.get_width(), ds.get_height())
canvas = pygame.Surface([canvas_size, canvas_size])
canvas.fill([100, 255, 100])
canvas_rect = canvas.get_rect()
canvas_rect.center = (ds.get_width() / 2, ds.get_height() / 2)

while True:

    ds.fill([255, 255, 255])

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        elif event.type == VIDEORESIZE:

            ds = pygame.display.set_mode(
                size=event.dict['size'],
                flags=HWSURFACE | DOUBLEBUF | RESIZABLE
            )
            canvas_size = min(ds.get_width(), ds.get_height())
            ds.blit(pygame.transform.scale(canvas, [canvas_size, canvas_size]))
            pygame.display.flip()

    ds.blit(canvas, canvas_rect)
    pygame.display.update()
    delta = clock.tick(60)
