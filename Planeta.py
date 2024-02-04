import pygame
import math
import time

# Clase balas
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        imagen = pygame.image.load("bala.png")
        self.image = pygame.transform.scale(imagen, (10, 10))
        self.mask = pygame.mask.from_surface(self.image)
        self.Imagen = self.image
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.velocidad = 5 
    #update balas para agarrar el angulo del planeta y  disparar de esas balas
    #para evitar tener que actualziar cada angle uso una bala 
    def update(self):
        rad_angle = math.radians(self.angle)
        self.rect.x += 5 * math.cos(rad_angle)
        self.rect.y += 5 * math.sin(rad_angle)
        
       
class Planeta(pygame.sprite.Sprite):
    def __init__(self, posicion):
        super().__init__()
        imagen = pygame.image.load("venus.png")
        self.image = pygame.transform.scale(imagen, (150, 150))
        self.Imagen = self.image
        self.rect = self.image.get_rect()  # Ya no es necesario, pero lo dejaremos para compatibilidad
        self.rect.topleft = posicion
        self.angle = 0
        self.bullets = pygame.sprite.Group()
        self.mask = pygame.mask.from_surface(self.image)
        self.vidas_iniciales = 3  # Usar self para indicar que es un atributo de la instancia
        self.frecuencia_enemigos = 5  # También aquí
        self.shoot_cooldown = 250 
        self.last_shot_time = 0 
        self.enemigos_eliminados = 0
        self.tiempo_boost = -1000
        # movimiento/movent
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