import random
import pygame
import Fondo
import Planeta
import math
import pygame_menu

from pygame.locals import QUIT, KEYDOWN, K_SPACE, K_p, K_ESCAPE

# Iniciar pygame y el método Main
pygame.init()

# Inicializar la pantalla
tamaño = (800, 800)
pantalla = pygame.display.set_mode(tamaño)
pygame.display.set_caption("Invasion a planeta")
font = pygame.font.Font(None, 25)


# Grupos de sprites
bullets_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()

# Creación de Enemigo y añadirlo al grupo de sprites
Enemigo = Planeta.Enemigo((0,0))
fondo = Fondo.Fondo((0, 0))
planeta = Planeta.Planeta((320, 360))
bullet = Planeta.Bullet(0, 0, 0)
enemigos.add(Enemigo)
all_sprites.add(fondo, planeta, bullet)

# Posición de vidas y puntaje en pantalla
vidasX, vidasY = 10, 40
font_vida = pygame.font.Font(None, 32)

score_value = 0
font_score = pygame.font.Font(None, 32)
textX, textY = 10, 10


def set_difficulty(value, planeta):
    if value == 1:
        planeta.vidas_iniciales = 3
        planeta.frecuencia_enemigos = 1
    elif value == 2:
        planeta.vidas_iniciales = 5
        planeta.frecuencia_enemigos = 1000
       
       
# Función para mostrar el puntaje en pantalla
def show_score(x, y):
    score = font_score.render("Puntuación: " + str(score_value), True, (255, 255, 255))
    pantalla.blit(score, (x, y))

# Función para mostrar las vidas en pantalla
def vidas(x, y):
    vidas = font_vida.render("Vidas: " + str(vidas_restantes), True, (255, 255, 255))
    pantalla.blit(vidas, (x, y))


# Función principal del juego
def start_the_game():
    global score_value, vidas_iniciales, frecuencia_enemigos, vidas_restantes, pausado

    reloj = pygame.time.Clock()
    FPS = 60
    running = True
    pausado = False
    vidas_restantes = planeta.vidas_iniciales  # Utiliza las vidas_iniciales del objeto planeta
    dificultad = planeta.frecuencia_enemigos  # Utiliza la frecuencia_enemigos del objeto planeta
    reinicio_paritda = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:
                # if event.key == K_SPACE:
                    # Crear una nueva bala en la dirección actual del jugador
                if event.key == K_p:
                    pausado = not pausado  # Cambiar el estado de pausado
                # elif event.key == K_ESCAPE: 
                    # if pausado:
                        # pausado = False
                        # menu.mainloop(pantalla)

        # Obtener las teclas presionadas
        keys = pygame.key.get_pressed()
        planeta.movement(keys, planeta, bullets_group, all_sprites)       
       

        if not pausado:
            print(vidas_restantes)
            print(vidas_restantes)
            pantalla.fill((255, 255, 255))

            # Dibuja la imagen de fondo antes de actualizar la pantalla
            pantalla.blit(background_image, (0, 0))

            # Crear enemigos
            if random.randint(0, 300) < dificultad:
                
                random_x = random.randint(-200, pantalla.get_width() + 200)
                random_y = random.randint(-200, pantalla.get_height() + 200)
                distancia_al_planeta = math.sqrt((random_x - planeta.rect.centerx) ** 2 + (random_y - planeta.rect.centery) ** 2)
                #me daba error y me quitaba una vida de gratis 
                # Verificar si la distancia al planeta es mayor que la distancia mínima permitida
                distancia_minima_al_planeta = 500
                if distancia_al_planeta > distancia_minima_al_planeta:
                    nuevo_enemigo = Planeta.Enemigo((random_x, random_y))
                    all_sprites.add(nuevo_enemigo)
                    enemigos.add(nuevo_enemigo)
              
            # Actualizar y dibujar los sprites
            all_sprites.update()
            all_sprites.draw(pantalla)

            # Mover los enemigos hacia el planeta
            for enemigo in enemigos:
                enemigo.move_towards_planet(planeta)

            # Eliminar balas fuera de la pantalla
            bullets_group.update()
            bullets_group.draw(pantalla)

            # Colisiones de balas con enemigos
            for bala in bullets_group:
                for enemigo in enemigos:
                    if pygame.sprite.collide_rect(bala, enemigo):
                        enemigos.remove(enemigo)
                        all_sprites.remove(enemigo)
                        bala.kill() 
                        score_value += 1
                        planeta.enemigos_eliminados += 1

            # Verificar si se han eliminado 10 enemigos
            if planeta.enemigos_eliminados >= 10:
                # Aplicar boost de velocidad en las balas
                bullet.aumentar_velocidad()  
                print("¡Boost de velocidad en las balas!")

                # Reiniciar contador de enemigos eliminados después de cada 10
                planeta.enemigos_eliminados = 0
 
            # Colisión de enemigos con el planeta
            for enemigo in enemigos:
                if pygame.sprite.collide_mask(enemigo, planeta):
                    vidas_restantes -= 1
                    enemigos.remove(enemigo)
                    all_sprites.remove(enemigo)

            # Verificar si el jugador se quedó sin vidas
            if vidas_restantes <= 0:
                if not reinicio_paritda:
                    reinicio_paritda = pygame.time.get_ticks()
                    pantalla.fill((0, 0, 0))
                    texto_game_over = pygame.image.load("gameover.png")
                    x = (pantalla.get_width() - texto_game_over.get_width()) // 2
                    y = (pantalla.get_height() - texto_game_over.get_height()) // 2
                    pantalla.blit(texto_game_over, (x, y))
                    pygame.display.flip()
                    pygame.time.delay(1500)
                    reinicio_paritda = True
                elif pygame.time.get_ticks() - reinicio_paritda >= 2000:
                    vidas_restantes = planeta.vidas_iniciales
                    score_value = 0
                    for enemigo in enemigos:
                        enemigo.kill()  # Elimina el sprite del grupo enemigos y all_sprites
                    enemigos.empty()  # Vacía el grupo enemigos (también puedes omitir esto si usas enemigo.kill())
                    pausado = False
                    reinicio_paritda = False
                    # Volver al menú principal
                    menu.mainloop(pantalla)
                                
        if pausado:
            texto = font.render("PAUSA", True, "White") 
            pantalla.blit(texto,(pantalla.get_width()/2-30, pantalla.get_height()/2-200))
        # Mostrar vidas y puntaje en pantalla
        vidas(vidasX, vidasY)
        show_score(textX, textY)

        # Mostrar mensaje de pausa si el juego está pausado
        
        pygame.display.flip()
        reloj.tick(FPS)

# Carga la imagen que deseas agregar al fondo
background_image_path = 'background.jpg'
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(background_image, tamaño)

# Crea el menú
menu = pygame_menu.Menu('Welcome', 400, 300, theme=pygame_menu.themes.THEME_DARK)

# Agrega un cuadro de texto, un selector y dos botones como en tu código original
menu.add.text_input('Name:', default='-----')
menu.add.selector('Difficulty:', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

# Ejecuta el menú
menu.mainloop(pantalla)

# Salir del juego
pygame.quit()