import math
import random
import Enemigo
import Planeta
import Main
class dificultad():#dificultad creada a mano ajustarlo a que sea mas "naturals"  
                    # sete de dificultad
        vidas_restantes = Planeta.vidas_iniciales  # Utiliza las vidas_iniciales del objeto planeta
        dificultad = Planeta.frecuencia_enemigos  # Utiliza la frecuencia_enemigos del objeto planeta
        def set_difficulty(value, planeta):
            if value == 1:
                planeta.vidas_iniciales = 3
                Enemigo.frecuencia_enemigos = 4
            elif value == 2:
                planeta.vidas_iniciales = 5
                Enemigo.frecuencia_enemigos = 8  
        varDifH = random.randint(0, 150)
        varDifE = random.randint(0, 500) 
        
        if dificultad == 10:             
            if varDifH < dificultad: 
                # Ajusta estos valores según sea necesario para que los enemigos aparezcan más lejos
                rango_x = (-500, Main.pantalla.get_width())
                rango_y = (-500, Main.pantalla.get_height())

                posicion_x = random.randint(*rango_x)
                posicion_y = random.randint(*rango_y)
                posicion = math.sqrt((posicion_x - Planeta.rect.centerx)**2 + (posicion_y - Planeta.rect.centery)**2)
                distanciaMin = 700

                if posicion > distanciaMin:
                    nuevo_enemigo = Enemigo.Enemigo((posicion_x, posicion_y))
                    Main.all_sprites.add(nuevo_enemigo)
                    Main.enemigos.add(nuevo_enemigo)

        if  dificultad == 5:
            if varDifE < dificultad: 
                posicion_x = random.randint(-500, Main.pantalla.get_width())
                posicion_y = random.randint(-500, Main.pantalla.get_height())
                posicion = math.sqrt((posicion_x - Planeta.rect.centerx)**2 + (posicion_y - Planeta.rect.centery)**2)

                distanciaMin = 700
                if  posicion > distanciaMin:
                    nuevo_enemigo = Enemigo.Enemigo((posicion_x, posicion_y))
                    Main.all_sprites.add(nuevo_enemigo)
                    Main.enemigos.add(nuevo_enemigo)