import pygame
import math

pygame.init()

# Set up the simulation window
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2D Physics Playground")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Define a particle class
class Particle:
    def __init__(self, x, y, radius=10):
        self.x = x
        self.y = y
        self.radius = radius
        self.prev_x = x
        self.prev_y = y

    def update_position(self, dt):
        # Verlet integration to update position
        temp_x = self.x
        temp_y = self.y
        self.x = 2 * self.x - self.prev_x
        self.y = 2 * self.y - self.prev_y + 9.81 * dt**2
        self.prev_x = temp_x
        self.prev_y = temp_y

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

    def reflect(self):
        if self.x <= self.radius or self.x >= width - self.radius:
            self.prev_x = self.x
            self.x = min(max(self.x, self.radius), width - self.radius)

        if self.y <= self.radius:
            self.prev_y = self.y
            self.y = min(max(self.y, self.radius), height - self.radius)


# Define a class for the movable rectangle
class MovableRectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))


particles = []
movable_rectangle = MovableRectangle(width // 3, height - 20, width // 3, 10)  # Initial position of the movable rectangle

running = True
clock = pygame.time.Clock()

while running:
    dt = clock.tick(60) / 1000.0  # Time in seconds since the last update

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            particles.append(Particle(x, y))

    # Update particle positions and reflect from screen borders
    for particle in particles:
        particle.update_position(dt)
        particle.reflect()

    # Move the rectangle with arrow keys (left and right)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        movable_rectangle.x = max(movable_rectangle.x - 5, 10)  # Limit left boundary
    if keys[pygame.K_RIGHT]:
        movable_rectangle.x = min(movable_rectangle.x + 5, width - movable_rectangle.width - 5)  # Limit right boundary


    # Reflect particles from the movable rectangle
    for particle in particles:
        if ((particle.y + particle.radius >= movable_rectangle.y) and (particle.y <= movable_rectangle.y + movable_rectangle.height) and (movable_rectangle.x <= particle.x <= movable_rectangle.x + movable_rectangle.width)):
            particle.prev_y = particle.y
            particle.y = movable_rectangle.y - particle.radius

    # Clear the screen
    screen.fill(WHITE)

    # Draw the movable rectangle
    movable_rectangle.draw()

    # Draw particles
    for particle in particles:
        particle.draw()

    # Update the display
    pygame.display.flip()

pygame.quit()
