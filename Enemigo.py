import pygame
import math
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, posicion):
        super().__init__()
        imagen = pygame.image.load("alien.png")
        self.image = pygame.transform.scale(imagen, (50, 50))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.topleft = posicion
        self.speed = 2  # Velocidad de movimiento del enemigo
        self.hitbox = (self.rect.x + 17, self.rect.y + 2, 31, 57) 
        self.frecuencia = 0
        self.angle = 0
        
    def move_towards_planet(self, planeta):
        angle = math.atan2(planeta.rect.centery - self.rect.centery, planeta.rect.centerx - self.rect.centerx)
        self.rect.x += self.speed * math.cos(angle)
        self.rect.y += self.speed * math.sin(angle)
        # self.angle = math.degrees(angle)  # Actualiza el ángulo en grados

    def update(self):
        self.mask = pygame.mask.from_surface(self.image)
        self.mask = pygame.mask.from_surface(self.image)
        pass
    # def update(self):
    def set_difficulty(vidas, dificultad):
        # global vidas_iniciales, frecuencia_enemigos
        if dificultad == 1: 
            dificultad = 6
        elif dificultad == 2:  # fácil
            dificultad = 4
