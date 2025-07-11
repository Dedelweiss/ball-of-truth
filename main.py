import pygame
import numpy as np
import sys

# Constantes
WIDTH, HEIGHT = 1080, 800
FPS = 60
CIRCLE_CENTER = np.array([540, 500])
CIRCLE_RADIUS = 300
BALL_RADIUS = 10
GRAVITY = 0.3
BOUNCINESS = 0.8

# Tuyaux (x position, width)
PIPES = [(100, 80), (500, 80), (800, 80)]  # Trois tuyaux à différentes positions

class Ball:
    def __init__(self, position, velocity):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.active = True  # Pour désactiver si elle tombe dans un tuyau

    def update(self):
        if not self.active:
            return
        self.velocity[1] += GRAVITY
        self.position += self.velocity

    def draw(self, surface):
        if self.active:
            pygame.draw.circle(surface, (255, 0, 0), self.position.astype(int), BALL_RADIUS)

class Game:
    def __init__(self):
        self.mode = "circle"  # "circle" ou "pipes"
        self.ball = Ball([540, 400], [4, -8])

    def switch_mode(self, mode):
        self.mode = mode
        # Réinitialiser la balle
        self.ball = Ball([540, 400], [4, -8])

    def update(self):
        self.ball.update()
        if self.mode == "circle":
            self.handle_circle_collision()
        elif self.mode == "pipes":
            self.handle_pipes_collision()

    def handle_circle_collision(self):
        direction = self.ball.position - CIRCLE_CENTER
        distance = np.linalg.norm(direction)
        if distance + BALL_RADIUS >= CIRCLE_RADIUS:
            if distance != 0:
                normal = direction / distance
                v_dot_n = np.dot(self.ball.velocity, normal)
                self.ball.velocity = self.ball.velocity - (1 + BOUNCINESS) * v_dot_n * normal
                self.ball.position = CIRCLE_CENTER + normal * (CIRCLE_RADIUS - BALL_RADIUS)

    def handle_pipes_collision(self):
        x, y = self.ball.position
        ball_bottom = y + BALL_RADIUS
        in_pipe = None

        for pipe_x, pipe_w in PIPES:
            if pipe_x <= x <= pipe_x + pipe_w:
                in_pipe = (pipe_x, pipe_w)
                break

        if in_pipe:
            pipe_x, pipe_w = in_pipe
            pipe_left = pipe_x
            pipe_right = pipe_x + pipe_w
            pipe_floor = HEIGHT - 50

            # Collision avec les murs du tuyau
            if x - BALL_RADIUS <= pipe_left:
                self.ball.velocity[0] *= -BOUNCINESS
                self.ball.position[0] = pipe_left + BALL_RADIUS
            elif x + BALL_RADIUS >= pipe_right:
                self.ball.velocity[0] *= -BOUNCINESS
                self.ball.position[0] = pipe_right - BALL_RADIUS

            # Collision avec le sol du tuyau
            if ball_bottom >= pipe_floor:
                self.ball.velocity[1] *= -BOUNCINESS
                self.ball.position[1] = pipe_floor - BALL_RADIUS
        else:
            # Si hors tuyau, balle rebondit sur le sol classique
            if ball_bottom >= HEIGHT - 50:
                self.ball.velocity[1] *= -BOUNCINESS
                self.ball.position[1] = HEIGHT - 50 - BALL_RADIUS


    def draw(self, screen):
        if self.mode == "circle":
            pygame.draw.circle(screen, (255, 255, 255), CIRCLE_CENTER.astype(int), CIRCLE_RADIUS, 4)
        elif self.mode == "pipes":
            pygame.draw.rect(screen, (100, 100, 100), (0, HEIGHT - 50, WIDTH, 50))  # Sol
            for pipe_x, pipe_w in PIPES:
                pygame.draw.rect(screen, (255, 255, 255), (pipe_x, HEIGHT - 700, pipe_w, 800))  # Tuyaux
        self.ball.draw(screen)

# Initialisation
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
game = Game()

# Boucle principale
running = True
while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                game.switch_mode("circle")
            elif event.key == pygame.K_p:
                game.switch_mode("pipes")

    game.update()
    game.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
