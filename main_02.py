import json
import pygame, sys
from funciones_sudo import *
from pygame.locals import *
from pygame import mixer


pygame.init() 
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Sudoku Clasico")

fuente = pygame.font.SysFont('Comic Sans MS', 25)
poner_musica("musica/Menu_inicio.wav")

# funcion del menu principal
def main_menu():
    dificultad = "Facil"
    click = False
    puntaje_conseguido = 0
    
    while True:
        fondo = pygame.transform.scale(pygame.image.load("imagenes/bg_main.png"), (ANCHO, ALTO))
        pantalla.blit(fondo,(0,0))
        escribir_texto("Sudoku Clásico", fuente, C_FUENTE, pantalla, 280, 40)
 
        mx, my = pygame.mouse.get_pos()

        # crea los botones 
        butt_jugar = pygame.Rect(280, 100, 200, 50)
        butt_configurar = pygame.Rect(280, 180, 200, 50)
        butt_puntajes = pygame.Rect(280, 260, 200, 50)
        butt_salir = pygame.Rect(280, 340, 200, 50)

        # Define las funcion cuando cierto boton es presionado
        if butt_configurar.collidepoint((mx, my)):
            if click == True:
                dificultad=configurar()
        if butt_jugar.collidepoint((mx, my)):
            if click == True:
                sudoku(dificultad)
        
        if butt_puntajes.collidepoint((mx, my)):
            if click == True:
                puntajes()
        if butt_salir.collidepoint((mx, my)):
            if click == True:
                pygame.quit()
                sys.exit()
        pygame.draw.rect(pantalla, C_BOTONES, butt_jugar)
        pygame.draw.rect(pantalla, C_BOTONES, butt_configurar)
        pygame.draw.rect(pantalla, C_BOTONES, butt_puntajes)
        pygame.draw.rect(pantalla, C_BOTONES, butt_salir)
 
        # Escribe el texto en el boton
        escribir_texto("JUGAR", fuente, C_FUENTE, pantalla, 330, 110)
        escribir_texto("CONFIGURAR", fuente, C_FUENTE, pantalla, 300, 190)
        escribir_texto("PUNTAJES", fuente, C_FUENTE, pantalla, 310, 270)
        escribir_texto("SALIR", fuente, C_FUENTE, pantalla, 330, 350)


        click = False
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == KEYDOWN:
                if evento.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if evento.type == MOUSEBUTTONDOWN:
                if evento.button == 1:
                    click = True

        pygame.display.update()


def sudoku(dificultad:str = "Facil"):
    poner_musica("musica/Sudoku.wav")
    matriz =inicializar_matriz(9,9,None)
    llenar_sudoku(matriz)  
    celdas_ocultas= ocultar_numeros(matriz,dificultad)
    celda_seleccionada = None
    ejecutando = True    
    listita = []
    errores = 0
    puntaje_conseguido =0
    tiempo = pygame.USEREVENT + 1
    un_segundo = 1000
    pygame.time.set_timer(tiempo,un_segundo)
    reloj = {"minutos": 0, "segundos": 0}
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if butt_volver.collidepoint(evento.pos):
                        ejecutando = False
                        poner_musica(ruta= "musica/Menu_inicio.wav")
                    if butt_reinicio.collidepoint(evento.pos):
                        matriz = inicializar_matriz(9,9,None)
                        llenar_sudoku(matriz)
                        ocultar_numeros(matriz,dificultad)
                        celda_seleccionada = None
                        listita = []
                        errores = 0
                        reloj = {"minutos": 0, "segundos": 0}
                        continue
            if evento.type == pygame.QUIT:
                ejecutando = False
                pygame.quit()
                sys.exit()            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                columna = x // TAM_CELDA
                fila = y // TAM_CELDA
                if 0 <= fila < 9 and 0 <= columna < 9:
                    celda_seleccionada = (fila, columna)
            manejar_teclado_virtual(evento, matriz, celda_seleccionada)
            celda_seleccionada = procesar_click(evento, TAM_CELDA, celda_seleccionada)
            
            if evento.type == pygame.KEYDOWN and celda_seleccionada is not None:
                fila, columna = celda_seleccionada
                if evento.key in range(pygame.K_1, pygame.K_9 + 1):
                    numero = evento.key - pygame.K_0           
                    es_valido_para_ingresar = es_valido(matriz, fila, columna, numero)
                    if matriz[fila][columna] is None:
                        matriz[fila][columna] = numero 
                        estados_celdas[fila][columna] = es_valido_para_ingresar
                        errores = contar_error(matriz,numero,celda_seleccionada,listita)
                elif evento.key == pygame.K_BACKSPACE:
                    if estados_celdas[fila][columna] is not None:
                        matriz[fila][columna] = None
                        estados_celdas[fila][columna] = None
            acierto= dibujar_tablero(pantalla,matriz, TAM_CELDA, celda_seleccionada)
            if acierto == celdas_ocultas:
                victoria(pantalla,BLANCO,NEGRO,puntaje_conseguido)
                ejecutando = False
            
            dibujar_teclado(pantalla, TAM_CELDA)
            transcurso= tomar_tiempo(pantalla,tiempo,evento,fuente,reloj)
            ilustrador_errores(pantalla,errores,fuente)
            puntaje_conseguido = contar_puntaje(errores,transcurso,dificultad)
            butt_volver = (dibujar_btt_volver(pantalla, TAM_CELDA,))
            butt_reinicio = dibujar_btt_reinicio(pantalla, TAM_CELDA)
        pygame.display.flip()

     
def puntajes():
    lista = cargar_puntajes(RUTA)
    ejecutando = True
    poner_musica("musica/Puntajes.wav")
    #elegir_mayor_puntuacion(jugadores,jugador_puntuacion,nombre_jugador_sudoku)
    while ejecutando:
        pantalla.fill((0,0,0))
        fondo = pygame.transform.scale(pygame.image.load("imagenes/bg_scores.jpg"), (ANCHO, ALTO))
        pantalla.blit(fondo,(0,0))
        cont_puntaj = pygame.Rect(260, 80, 200, 300)
        escribir_texto("Puntajes", fuente, (255, 255, 255), pantalla, ANCHO / 2.40, 20)
        pygame.draw.rect(pantalla, (191, 94, 129), cont_puntaj)

        
        for evento in pygame.event.get():
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    if butt_volver.collidepoint(evento.pos):
                        ejecutando = False
                        poner_musica("musica/Menu_inicio.wav")
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
        ordenar_lista(lista)
        ilustrar_puntos(lista,pantalla,100)        
        butt_volver = dibujar_btt_volver(pantalla, TAM_CELDA)
        pygame.display.flip()


def configurar():
    mixer.music.stop()
    ejecutando = True
    nombre_usuario = ""
    click = False
    dificultad = "Facil"
    
    click = False    
    
    while ejecutando:
        fondo = pygame.transform.scale(pygame.image.load("imagenes/bg_scores.jpg"), (ANCHO, ALTO))
        mx, my = pygame.mouse.get_pos()
        pantalla.blit(fondo,(0,0))
        cont_config = pygame.Rect(260, 100, 200, 300)
        bott_facil = pygame.Rect(280, 200, 160, 45)
        bott_moderada = pygame.Rect(280, 260, 160, 45)
        bott_dificil = pygame.Rect(280, 320, 160, 45)
        
        pygame.draw.rect(pantalla, ROSA_OSCURO, cont_config)
        pygame.draw.rect(pantalla, MORADO_OSCURO, bott_facil)
        pygame.draw.rect(pantalla, MORADO_OSCURO, bott_moderada)
        pygame.draw.rect(pantalla, MORADO_OSCURO, bott_dificil)
        escribir_texto("Configuracion", fuente, BLANCO, pantalla, ANCHO / 2.60, 40)
        escribir_texto("Dificultad ", fuente, BLANCO, pantalla, ANCHO / 2.40, 130)
        escribir_texto("Fácil", fuente, BLANCO, pantalla, ANCHO / 2.15, 205)
        escribir_texto("Moderada", fuente, BLANCO, pantalla, ANCHO / 2.30, 265)
        escribir_texto("Dificil", fuente, BLANCO, pantalla, ANCHO / 2.15, 325)
        
        if bott_facil.collidepoint((mx, my)):
            if click == True:
                dificultad = "Facil"
                pygame.draw.rect(pantalla, ROSA_PASTEL, bott_facil)
                escribir_texto("Fácil", fuente, NEGRO, pantalla, ANCHO / 2.15, 205)
        if bott_moderada.collidepoint((mx, my)):
            if click == True:
                dificultad = "Moderado"
                pygame.draw.rect(pantalla, ROSA_PASTEL, bott_moderada)
                escribir_texto("Moderado", fuente, NEGRO, pantalla, ANCHO / 2.30, 265)
        if bott_dificil.collidepoint((mx, my)):
            if click == True:
                dificultad = "Dificil"
                pygame.draw.rect(pantalla, ROSA_PASTEL, bott_dificil)
                escribir_texto("Dificil", fuente, NEGRO, pantalla, ANCHO / 2.150, 325)

                
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == MOUSEBUTTONDOWN:
                    if evento.button == 1:
                        click = True
                        if butt_volver.collidepoint(evento.pos):
                            ejecutando = False
                            poner_musica(ruta= "musica/Menu_inicio.wav")

        butt_volver = dibujar_btt_volver(pantalla, TAM_CELDA)
        pygame.display.flip()
    return dificultad


def victoria(pantalla:pygame.Surface,color_fondo:tuple,color_text:tuple,jugador_puntuacion:int):
    ejecutando = True
    jugadores = cargar_puntajes(RUTA)
    nombre_usuario = ""
    while ejecutando:
        pantalla.fill(color_fondo)
        fondo = pygame.transform.scale(pygame.image.load("imagenes/bg_scores.jpg"), (ANCHO, ALTO))
        pantalla.blit(fondo,(0,0))

        cont_nickname = pygame.Rect(280, 180, 160, 45)
        pygame.draw.rect(pantalla, color_text, cont_nickname)

        escribir_texto("Felicitaciones por completar el sudoku", fuente, color_text, pantalla, ANCHO / 4.5, 60)
        escribir_texto("Ingrese su nombre", fuente, color_text, pantalla, ANCHO / 2.7, 140)
        texto_surface = fuente.render(nombre_usuario, True, BLANCO)
        pantalla.blit(texto_surface, (cont_nickname.x+5, cont_nickname.y+5))

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == KEYDOWN:
                if evento.key == K_RETURN:
                    jugadores_ordenados = elegir_mayor_puntuacion(jugadores, jugador_puntuacion, nombre_usuario)
                    guardar_puntajes(jugadores_ordenados, RUTA)
                    pygame.quit()
                    sys.exit()
                if evento.key == K_BACKSPACE:
                    nombre_usuario = nombre_usuario[:-1]
                
                else:
                    temp_texto = nombre_usuario + evento.unicode
                    texto_surface = fuente.render(temp_texto , True, color_text)
                    if texto_surface.get_width() <= cont_nickname.width - 5: 
                        nombre_usuario = temp_texto 
            
        
        pygame.display.flip()
   
    
main_menu()    

