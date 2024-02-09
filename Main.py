import random
import pygame
import Fondo
import Planeta
import Enemigo
import math
import pygame_menu
import time
from pygame.locals import QUIT, KEYDOWN, K_SPACE, K_p, K_ESCAPE

# Inicializacion de pygame
pygame.init()


# Inicializar la pantalla
tamaño = (800, 800) #tamaño de window en que launchea la pantalla 
pantalla = pygame.display.set_mode(tamaño)  
# titulo del juego 
pygame.display.set_caption("Invasion a planeta")

#fuentes, si tuvieras o quieres descargate una seria font = pygame.font.Font("\rutaDeFuente", size)
font = pygame.font.Font(None, 25)
disparoLoco = pygame.font.Font(None, 50)

# Grupo sprute que nos provide la biblioteca pygame para colisiones 
bullets_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
enemigos = pygame.sprite.Group()

# creamos el fondo  y el planeta en su posicion
fondo = Fondo.Fondo((0, 0))
planeta = Planeta.Planeta((320, 360))
all_sprites.add(fondo, planeta)



# Posicion y creacion de las vidas en pantalla
vidasX, vidasY = 10, 40
font_vida = pygame.font.Font(None, 32)

#puntuacion y su posicon
score_value = 0
font_score = pygame.font.Font(None, 32)
textX, textY = 10, 10

#esconder cursor
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))


# seteo de  de dificultad
def set_difficulty(value, planeta):
    if value == 1:
        planeta.vidas_iniciales = 3
        Enemigo.frecuencia_enemigos = 5
    elif value == 2:
        planeta.vidas_iniciales = 5
        Enemigo.frecuencia_enemigos = 8  

       
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
    
    # boosteo inicializado en false
    boost = False  
    # momento_actual = pygame.time.get_ticks()
    reloj = pygame.time.Clock()
    FPS = 60
    # corre el juego 
    running = True
    # pausar el juego
    pausado = False
    vidas_restantes = planeta.vidas_iniciales  # Utiliza las vidas_iniciales del objeto planeta
    dificultad = planeta.frecuencia_enemigos  # Utiliza la frecuencia_enemigos del objeto planeta
    reinicio_paritda = False
    ultimo_enemigo_tiempo = pygame.time.get_ticks()
    cooldown_creacion_enemigosH = 500 # (chuleta de como funcina los seg en py) : 1000 milisegundos = 1 segundo
    cooldown_creacion_enemigosE = 1000
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        # Obtener las teclas presionadas
        keys = pygame.key.get_pressed()
        # añadimos las keys, planeta, bulets, y el sprite planeta al movemntes asi actualizo las balas
        planeta.movement(keys, planeta, bullets_group, all_sprites)       
        
        # manejamos que si pulsa P pausamos el juego 
        
        if keys[pygame.K_p]:
            pausado = not pausado
            
            
        # if not pausado = corre el juego 
        if not pausado:
            
            # Actualizar y dibujar los sprites
            all_sprites.update()
            all_sprites.draw(pantalla)
            
            # dificultad de manejo con ultimo_enemigoCreado
            # dificultad hardcore?¿
            # dificultad hard
            if vidas_restantes == 3:
                tiempo_actual = pygame.time.get_ticks()
                if tiempo_actual - ultimo_enemigo_tiempo > cooldown_creacion_enemigosH:             
                    for i in range(2):
                           # Ajusta estos valores según sea necesario para que los enemigos aparezcan más lejos
                           rango_x = (-500, pantalla.get_width())
                           rango_y = (-500, pantalla.get_height())
                           posicion_x = random.randint(*rango_x)
                           posicion_y = random.randint(*rango_y)
                            #distancia minima para que no aparzcan al lado del planeta
                           distanciaMin = 500
                           distancia_planeta = math.sqrt((posicion_x - planeta.rect.centerx)**2 + (posicion_y - planeta.rect.centery)**2)
                           
                           ultimo_enemigo_tiempo = tiempo_actual
                           if distancia_planeta > distanciaMin:
                               nuevo_enemigo = Enemigo.Enemigo((posicion_x, posicion_y))
                               all_sprites.add(nuevo_enemigo)
                               enemigos.add(nuevo_enemigo)
                        
            # dificultad  Easssyy
            if vidas_restantes == 5:
                tiempo_actual = pygame.time.get_ticks()
                if tiempo_actual - ultimo_enemigo_tiempo > cooldown_creacion_enemigosE:             
                    for i in range(1):
                           print(dificultad)
                           # Ajusta estos valores según sea necesario para que los enemigos aparezcan más lejos
                           rango_x = (-500, pantalla.get_width())
                           rango_y = (-500, pantalla.get_height())
                           posicion_x = random.randint(*rango_x)
                           posicion_y = random.randint(*rango_y)

                           distanciaMin = 500

                           distancia_planeta = math.sqrt((posicion_x - planeta.rect.centerx)**2 + (posicion_y - planeta.rect.centery)**2)
                           
                           ultimo_enemigo_tiempo = tiempo_actual
                        #creacion de enemigos 
                           if distancia_planeta > distanciaMin:
                               nuevo_enemigo = Enemigo.Enemigo((posicion_x, posicion_y))
                               all_sprites.add(nuevo_enemigo)
                               enemigos.add(nuevo_enemigo)
                        
            # creacion de enemigos y que nos reste una vida 
            for enemigo in enemigos:
                if pygame.sprite.collide_mask(enemigo, planeta):
                    vidas_restantes -= 1
                    enemigos.remove(enemigo)
                    all_sprites.remove(enemigo)
                    if distancia_planeta < 275:
                            enemigo.rotation_speed = 500    
                    
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
            if planeta.enemigos_eliminados >= 5:
                
                # aunmento de velocidad
                planeta.aumentar_velocidad()
                boost = True
                
                # Reiniciar contador de enemigos eliminados después de cada 5
                planeta.enemigos_eliminados = 0
                tiempo_boost = time.time()
            if boost:
                textoBUFF = disparoLoco.render("AUNMENTO DE VELOCIDAD", True, (255,255,255)) 
                pantalla.blit(textoBUFF, (210,pantalla.get_height()//10))
               
            # Boosteo de 3 segundos de ataque aunmentado (velocidad de ataque aunmentada self.shoot)
            if boost and time.time() - tiempo_boost > 3:
                planeta.disminuir_velocidad()
                boost = False
            
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
        pygame.display.flip()
        reloj.tick(FPS)

# Carga la imagen del fondo
# background_image_path = 'background.jpg'
# background_image = pygame.image.load(background_image_path)
# background_image = pygame.transform.scale(background_image, tamaño)

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