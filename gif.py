import pygame
import imageio
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
width, height = 400, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("GIF en Pygame")

# Cargar el gif utilizando imageio
gif_path = 'ruta_del_gif.gif'
gif = imageio.get_reader(gif_path)

# Obtener el tamaño del gif
gif_width, gif_height = gif.get_meta_data()['size']

# Obtener la superficie del gif
gif_surface = pygame.Surface((gif_width, gif_height), pygame.SRCALPHA)

# Temporizador para controlar la velocidad de reproducción del gif
clock = pygame.time.Clock()
frame_delay = int(1000 / gif.get_meta_data()['fps'])

# Bucle principal
running = True
frame = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Obtener el siguiente cuadro del gif
    try:
        img = pygame.image.fromstring(gif.get_next_data(), gif.get_meta_data()['palette'], "RGB")
    except:
        # Reiniciar el gif si llegamos al final
        gif = imageio.get_reader(gif_path)
        continue

    # Dibujar el cuadro en la superficie del gif
    gif_surface.blit(img, (0, 0))

    # Mostrar la superficie del gif en la pantalla
    screen.blit(pygame.transform.scale(gif_surface, (width, height)), (0, 0))
    pygame.display.flip()

    # Controlar la velocidad de reproducción
    clock.tick_busy_loop(1000 / frame_delay)

# Salir de Pygame
pygame.quit()
sys.exit()
