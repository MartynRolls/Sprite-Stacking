import pygame
from math import pi, sin, cos, sqrt
from numpy import arctan2


# Preparing method for splitting sprite sheet into correct parts
def prepare_sheet(directory, width, height):
    slices = []
    sheet = pygame.image.load(directory).convert_alpha()
    for i in range(sheet.get_width() // width):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(sheet, (0, 0), (i * width, 0, (i + 1) * width, height))
        slices.append(image)
    return slices


# Initialising game
pygame.init()

size = 500
screen = pygame.display.set_mode((size, size))
clock = pygame.time.Clock()
pygame.display.set_caption('Sprite Stacking')

# Setting car variables
car_x = size / 2
car_y = size / 2
car_angle = 0
car = prepare_sheet('Sprites/PurpleCar.png', 16, 16)
marks = []

# Main loop
while True:
    # Checking events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    # Checking key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        angle = car_angle * pi / 1800 + pi / 2
        car_y -= 5 * sin(angle)
        car_x += 5 * cos(angle)
        if keys[pygame.K_d]:
            car_angle -= 45
        if keys[pygame.K_a]:
            car_angle += 45

    # Correcting car angle
    if car_angle > 3600:
        car_angle -= 3600
    elif car_angle < 0:
        car_angle += 3600

    screen.fill('white')

    # Drawing tyre markings
    for mark in marks:
        angle = mark[1] / 10 + 90
        angle -= car_angle / 10
        image = pygame.transform.rotate(car[1], angle)
        image = pygame.transform.scale_by(image, (4, 4))

        x, y = mark[0]
        x, y = x - car_x, y - car_y
        m, a = sqrt(x ** 2 + y ** 2), arctan2(y, x)
        a += car_angle * pi / 1800
        x, y = m * cos(a), m * sin(a)
        x, y = x + (size - image.get_width()) // 2, y + (size - image.get_height()) // 2
        screen.blit(image, (x, y))

    # Adding / Removing tyre marks
    marks.append([(car_x, car_y), car_angle])
    if len(marks) > 100:
        marks.pop(0)

    # Drawing car, layer by layer
    for i, layer in enumerate(car):
        angle = 90
        image = pygame.transform.rotate(layer, angle)
        image = pygame.transform.scale_by(image, (4, 4))

        x, y = size - image.get_width(), size - image.get_height()
        x, y = x // 2, y // 2 - i * 4
        screen.blit(image, (x, y))

    pygame.display.flip()
    clock.tick(60)
