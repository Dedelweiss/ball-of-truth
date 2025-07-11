import pygame
import numpy as np

# Constantes
WIDTH, HEIGHT = 1080, 1920
FPS = 60
CIRCLE_CENTER = np.array([540, 500])
CIRCLE_RADIUS = 200
BALL_RADIUS = 10
GRAVITY = 0.05
BOUNCINESS = 1  # 1.0 = rebond parfait, < 1 = perte d'énergie

# Classe balle
class Ball:
    def __init__(self, position, velocity):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)

    def update(self):
        # Appliquer la gravité
        self.velocity[1] += GRAVITY

        # Mise à jour de la position
        self.position += self.velocity

        # Vérifier la collision avec le cercle
        direction = self.position - CIRCLE_CENTER
        distance = np.linalg.norm(direction)

        if distance + BALL_RADIUS >= CIRCLE_RADIUS:
            if distance != 0:
                normal = direction / distance
                v_dot_n = np.dot(self.velocity, normal)
                self.velocity = self.velocity - (1 + BOUNCINESS) * v_dot_n * normal
                self.position = CIRCLE_CENTER + normal * (CIRCLE_RADIUS - BALL_RADIUS)

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), self.position.astype(int), BALL_RADIUS + 4)
        pygame.draw.circle(surface, (255, 0, 0), self.position.astype(int), BALL_RADIUS)