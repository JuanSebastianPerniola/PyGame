import pygame
import math
import random
import time

# Clase balas
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        imagen = pygame.image.load("disparo.png")
        self.image = pygame.transform.scale(imagen, (10, 10))
        self.mask = pygame.mask.from_surface(self.image)
        self.Imagen = self.image
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.velocidad = 5 
    
    def update(self):
        rad_angle = math.radians(self.angle)
        self.rect.x += 5 * math.cos(rad_angle)
        self.rect.y += 5 * math.sin(rad_angle)
        # pantalla.blit(self.image, self.rect.topleft)
class Planeta(pygame.sprite.Sprite):
    def __init__(self, posicion):
        super().__init__()
        imagen = pygame.image.load("venus.png")
        self.image = pygame.transform.scale(imagen, (150, 180))
        self.Imagen = self.image
        self.rect = self.image.get_rect()  # Ya no es necesario, pero lo dejaremos para compatibilidad
        self.rect.topleft = posicion
        self.angle = 0
        self.bullets = pygame.sprite.Group()
        self.mask = pygame.mask.from_surface(self.image)
        self.vidas_iniciales = 3  # Usar self para indicar que es un atributo de la instancia
        self.frecuencia_enemigos = 5  # También aquí
        self.shoot_cooldown = 250 # Cooldown en milisegundos (1.2 segundos)
        self.last_shot_time = 0 
        self.enemigos_eliminados = 0
        self.tiempo_boost = -1000
        
    def movement(self, keys, planeta, bullets_group, all_sprites):
        if keys[pygame.K_LEFT]:
            planeta.angle += 2
        if keys[pygame.K_RIGHT]:
            planeta.angle -= 2 
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time > self.shoot_cooldown:
                self.shoot(bullets_group, all_sprites)
                self.last_shot_time = current_time

    def shoot(self, bullets_group, all_sprites):
        nueva_bala = Bullet(self.rect.centerx, self.rect.centery, self.angle)
        bullets_group.add(nueva_bala)
        all_sprites.add(nueva_bala)
        
    def aumentar_velocidad(self):
        # Aumenta la velocidad de la bala según tu lógica de movimiento
        self.shoot_cooldown = 1
        self.tiempo_boost = time.time()
        
    def disminuir_velocidad(self):
        # Aumenta la velocidad de la bala según tu lógica de movimiento
        self.shoot_cooldown = 250

    def update(self):
        # # si las ponemos asi tambien se mueve (experimentos)
        self.mask =  pygame.mask.from_surface(self.image)
        self.image = pygame.transform.rotate(self.Imagen, -self.angle)
        self.mask = pygame.mask.from_surface(self.image)
        # Actualiza la posición del rectángulo si es necesario
        self.rect = self.image.get_rect(center=self.rect.center)
        if time.time() - self.tiempo_boost > 3:
            self.disminuir_velocidad()
        
    def draw(self, screen):
            screen.blit(self.image, self.rect.topleft)
            
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
        # Calcular el ángulo entre el enemigo y el planeta
        angle = math.atan2(planeta.rect.centery - self.rect.centery, planeta.rect.centerx - self.rect.centerx)
        # Actualizar las coordenadas del enemigo en dirección al planeta
        self.rect.x += self.speed * math.cos(angle)
        self.rect.y += self.speed * math.sin(angle)
        # self.enemigo = self.rect.y and self.rect.x
        pass
    def update(self):
        self.mask =  pygame.mask.from_surface(self.image)
        self.image = pygame.transform.rotate(self.image, +self.angle)
        self.mask = pygame.mask.from_surface(self.image)
        # Actualiza la posición del rectángulo si es necesario
        self.rect = self.image.get_rect(center=self.rect.center)
        pass
    # def update(self):
    def set_difficulty(vidas, dificultad):
        # global vidas_iniciales, frecuencia_enemigos
        if dificultad == 1: 
            # vidas = 3  # difícil
            dificultad = 5
            # frecuencia_enemigos = dificultad
        elif dificultad == 2:  # fácil
            # vidas = 5  # difícil
            # vidas_iniciales = vidas
            dificultad = 3
            # frecuencia_enemigos = dificultad