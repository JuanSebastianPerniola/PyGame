import pygame
import math
import random

# Clase balas
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        imagen = pygame.image.load("disparo.png")
        self.image = pygame.transform.scale(imagen, (10, 10))
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
        self.image = pygame.transform.scale(imagen, (150, 150))
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
        
    def draw(self, screen):
            screen.blit(self.image, self.rect.topleft)
            
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, posicion):
        super().__init__()   
        
        # 0                             # 1
        self.imagenes = [pygame.image.load("alien.png"), pygame.image.load("alien2.png")]
        self.image = pygame.transform.scale(self.imagenes[0], (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = posicion
        self.speed = 2  # Velocidad de movimiento del enemigo
        self.hitbox = (self.rect.x + 17, self.rect.y + 2, 31, 57) 
        self.frecuencia = 2000  # 2000 milisegundos = 2 segundos
        self.angle = 0
        self.last_update = pygame.time.get_ticks()  # Guardar el tiempo actual

    def move_towards_planet(self, planeta):
        # Calcular el ángulo entre el enemigo y el planeta
        angle = math.atan2(planeta.rect.centery - self.rect.centery, planeta.rect.centerx - self.rect.centerx)
        # Actualizar las coordenadas del enemigo en dirección al planeta
        self.rect.x += self.speed * math.cos(angle)
        self.rect.y += self.speed * math.sin(angle)
        self.enemigo_posicion = (self.rect.y, self.rect.x)

    def update(self):
        now = pygame.time.get_ticks()  # Obtener el tiempo actual

        # Verificar si han pasado 2 segundos desde la última actualización
        if now - self.last_update > self.frecuencia:
            # Cambiar la imagen del enemigo
            self.image = pygame.transform.scale(self.imagenes[1], (50, 50))
            # Actualizar el tiempo de la última actualización
            self.last_update = now

        self.mask = pygame.mask.from_surface(self.image)
        self.image = pygame.transform.rotate(self.image, +self.angle)
        self.mask = pygame.mask.from_surface(self.image)
        # Actualiza la posición del rectángulo si es necesario
        self.rect = self.image.get_rect(center=self.rect.center)

    def set_difficulty(vidas, dificultad):
        # global vidas_iniciales, frecuencia_enemigos
        if dificultad == 1: 
            # vidas = 3  # difícil
            dificultad = 6.6
            # frecuencia_enemigos = dificultad
        elif dificultad == 2:  # fácil
            # vidas = 5  # difícil
            # vidas_iniciales = vidas
            dificultad = 4
            # frecuencia_enemigos = dificultad