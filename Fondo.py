import pygame
# Fondo 
class Fondo(pygame.sprite.Sprite):
    def __init__(self, posicion) -> None:
        super().__init__()
        image = pygame.image.load("background.jpg")
        pantalla = pygame.display.get_surface()
        self.image = pygame.transform.scale(image, (pantalla.get_width(), pantalla.get_height()))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)    