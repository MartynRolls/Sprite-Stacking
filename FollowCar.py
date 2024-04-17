import pygame
from math import pi, sin, cos, sqrt, log10
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
camera_distance = 0
camera_angle = 0
car = prepare_sheet('Sprites/WhiteMotorcycle.png', 16, 16)
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
        camera_distance += 1
        if keys[pygame.K_d]:
            car_angle -= 45
            camera_angle -= 1
        if keys[pygame.K_a]:
            car_angle += 45
            camera_angle += 1

    # Moving camera closer to car
    camera_angle *= 0.95
    camera_distance *= 0.95
    if -0.1 < camera_angle < 0.1:
        camera_angle = 0

    # Correcting car angle
    if car_angle > 3600:
        car_angle -= 3600
    elif car_angle < 0:
        car_angle += 3600

    screen.fill('white')

    # Drawing tyre markings
    for mark in marks:
        angle = mark[1] / 10 + 90  # Getting angle
        angle -= car_angle / 10  # Adding car angle on
        if camera_angle > 0: # Adding camera angle on
            angle += 60 * log10(camera_angle + 1)
        elif camera_angle < 0:
            angle -= 60 * log10(abs(camera_angle) + 1)

        image = pygame.transform.rotate(car[1], angle)
        image = pygame.transform.scale_by(image, (4, 4))

        x, y = mark[0]  # Figuring out coordinates
        x, y = x - car_x, y - car_y
        m, a = sqrt(x ** 2 + y ** 2), arctan2(y, x)  # Converting to polar form to rotate round car
        a += car_angle * pi / 1800  # Adding car angle to rotation
        if camera_angle > 0:  # Adding camera angle to rotation
            a -= (60 * log10(camera_angle + 1)) * pi / 180
        elif camera_angle < 0:
            a += (60 * log10(abs(camera_angle) + 1)) * pi / 180
        x, y = m * cos(a), m * sin(a)  # Converting back to rectangular form
        x, y = x + (size - image.get_width()) // 2, y + (size - image.get_height()) // 2  # Centring car
        y -= 30 * log10(camera_distance + 1)
        screen.blit(image, (x, y))

    # Adding / Removing tyre marks
    marks.append([(car_x, car_y), car_angle])
    if len(marks) > 300:
        marks.pop(0)

    # Drawing car, layer by layer
    for i, layer in enumerate(car):
        angle = 90
        if camera_angle > 0:
            angle += 60 * log10(camera_angle + 1)
        elif camera_angle < 0:
            angle -= 60 * log10(abs(camera_angle) + 1)

        image = pygame.transform.rotate(layer, angle)
        image = pygame.transform.scale_by(image, (4, 4))

        x, y = size - image.get_width(), size - image.get_height()
        x, y = x // 2, y // 2 - i * 4
        y -= 30 * log10(camera_distance + 1)
        screen.blit(image, (x, y))

    pygame.display.flip()
    clock.tick(60)
