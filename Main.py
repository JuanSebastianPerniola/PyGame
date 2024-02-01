import random
import pygame
import Fondo
import Planeta
import Enemigo
import math
import pygame_menu
import time
from pygame.locals import QUIT, KEYDOWN, K_SPACE, K_p, K_ESCAPE

# Iniciar pygame y el método Main
pygame.init()

# Inicializar la pantalla
tamaño = (800, 800)
pantalla = pygame.display.set_mode(tamaño)
pygame.display.set_caption("Invasion a planeta")
font = pygame.font.Font(None, 25)
disparoLoco = pygame.font.Font(None, 50)

# Grupos de sprites
bullets_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()

# Creación de Enemigo y añadirlo al grupo de sprites
# Enemigo = Enemigo.Enemigo((0,0))
fondo = Fondo.Fondo((0, 0))
planeta = Planeta.Planeta((320, 360))
bullet = Planeta.Bullet(-10, -10, -10)
# enemigos.add(Enemigo.Enemigo)
all_sprites.add(fondo, planeta, bullet)

# Posición de vidas y puntaje en pantalla
vidasX, vidasY = 10, 40
font_vida = pygame.font.Font(None, 32)

score_value = 0
font_score = pygame.font.Font(None, 32)
textX, textY = 10, 10

pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

def set_difficulty(value, planeta):
    if value == 1:
        planeta.vidas_iniciales = 3
        Enemigo.frecuencia_enemigos = 10    
    elif value == 2:
        planeta.vidas_iniciales = 5
        Enemigo.frecuencia_enemigos = 5   #

       
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
    boost = False  
    # momento_actual = pygame.time.get_ticks()
    reloj = pygame.time.Clock()
    FPS = 60
    running = True
    pausado = False
    vidas_restantes = planeta.vidas_iniciales  # Utiliza las vidas_iniciales del objeto planeta
    dificultad = planeta.frecuencia_enemigos  # Utiliza la frecuencia_enemigos del objeto planeta
    reinicio_paritda = False
    tiempo_creacion_enemigo = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Obtener las teclas presionadas
        keys = pygame.key.get_pressed()
        planeta.movement(keys, planeta, bullets_group, all_sprites)       
       
        if keys[pygame.K_p]:
            pausado = not pausado
        if not pausado:
            pantalla.fill((255, 255, 255))
            # Dibuja la imagen de fondo antes de actualizar la pantalla
            pantalla.blit(background_image, (0, 0))         
            # Lógica de creación de enemigos basada en temporizador
            
                      
            # Actualizar y dibujar los sprites
            all_sprites.update()
            all_sprites.draw(pantalla)
            
            for enemigo in enemigos:
                if pygame.sprite.collide_mask(enemigo, planeta):
                    vidas_restantes -= 1
                    enemigos.remove(enemigo)
                    all_sprites.remove(enemigo)
            # Mover los enemigos hacia el planeta
            for enemigo in enemigos:
                enemigo.move_towards_planet(planeta)            
            # Colisiones de balas con enemigos
            for bala in bullets_group:
                for enemigo in enemigos:
                    if pygame.sprite.collide_rect(bala, enemigo):
                        enemigos.remove(enemigo)
                        all_sprites.remove(enemigo)
                        bala.kill() 
                        score_value += 1
                        planeta.enemigos_eliminados += 1

            # Verificar si se han eliminado 5 enemigos
            if planeta.enemigos_eliminados >= 1    :
                # ratatata
                planeta.aumentar_velocidad()
                boost = True
                 # Reiniciar contador de enemigos eliminados después de cada 5
                planeta.enemigos_eliminados = 0
                tiempo_boost = time.time()
            if boost:
                textoBUFF = disparoLoco.render("AUNMENTO DE VELOCIDAD", True, (255,255,255)) 
                pantalla.blit(textoBUFF, (pantalla.get_width()//15,pantalla.get_height()//5))
               
            # Verificar si se debe disminuir la velocidad después de 3 segundos
            if boost and time.time() - tiempo_boost > 3:
                planeta.disminuir_velocidad()
                boost = False
                
                
                
           
                
            varDifH = random.randint(0, 250)
            varDifE = random.randint(0, 500) 
            
            if dificultad == 10:             
                if varDifH < dificultad: 
                    # Ajusta estos valores según sea necesario para que los enemigos aparezcan más lejos
                    rango_x = (-500, pantalla.get_width())
                    rango_y = (-500, pantalla.get_height())

                    posicion_x = random.randint(*rango_x)
                    posicion_y = random.randint(*rango_y)
                    posicion = math.sqrt((posicion_x - planeta.rect.centerx)**2 + (posicion_y - planeta.rect.centery)**2)
                    distanciaMin = 700

                    if posicion > distanciaMin:
                        nuevo_enemigo = Enemigo.Enemigo((posicion_x, posicion_y))
                        all_sprites.add(nuevo_enemigo)
                        enemigos.add(nuevo_enemigo)

            if  dificultad == 5:
                if varDifE < dificultad: 
                    posicion_x = random.randint(-500, pantalla.get_width())
                    posicion_y = random.randint(-500, pantalla.get_height())
                    posicion = math.sqrt((posicion_x - planeta.rect.centerx)**2 + (posicion_y - planeta.rect.centery)**2)

                    distanciaMin = 700
                    if  posicion > distanciaMin:
                        nuevo_enemigo = Enemigo.Enemigo((posicion_x, posicion_y))
                        all_sprites.add(nuevo_enemigo)
                        enemigos.add(nuevo_enemigo)    
            
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
