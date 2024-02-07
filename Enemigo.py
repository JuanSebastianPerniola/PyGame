import pygame
import math

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, posicion):
        super().__init__()
        imagen = pygame.image.load("alien.png")
        self.image = pygame.transform.scale(imagen, (50, 50))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=posicion)  # Centrar el rectángulo en la posición dada
        self.speed = 2  # Velocidad de movimiento del enemigo
        self.rotation_speed = 2  # Velocidad de rotación del enemigo
        self.angle = 0  # Ángulo de rotación inicial del enemigo
        self.original_image = self.image  # Almacenar una copia de la imagen original para rotaciones
        
    def move_towards_planet(self, planeta):
        angle = math.atan2(planeta.rect.centery - self.rect.centery, planeta.rect.centerx - self.rect.centerx)
        self.rect.x += self.speed * math.cos(angle)
        self.rect.y += self.speed * math.sin(angle)

    def update(self):
        # Actualizar la máscara
        self.mask = pygame.mask.from_surface(self.image)
        # Rotar la imagen del enemigo sobre su propio eje
        self.angle += self.rotation_speed
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        # Ajustar el ángulo para que esté dentro del rango de 0 a 360 grados
        self.angle %= 360
        # Actualizar el rectángulo del enemigo para que coincida con la nueva posición y rotación
        self.rect = self.image.get_rect(center=self.rect.center)
        
    def set_difficulty(vidas, dificultad):
        # Esta función debería ser estática ya que no necesita acceder a atributos de instancia
        # global vidas_iniciales, frecuencia_enemigos
        if dificultad == 1: 
            dificultad = 0.1
        elif dificultad == 2:  # fácil
            dificultad = 4
