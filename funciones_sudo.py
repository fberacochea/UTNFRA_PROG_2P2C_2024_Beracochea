import pygame
import random
from pygame.locals import *
from pygame import mixer
import json

TAM_CELDA = 60  
ANCHO = 9 * TAM_CELDA + 160  
ALTO = 9 * TAM_CELDA  
MITAD_ANCHO_PANTALLA = ANCHO // 2
MITAD_ALTO_PANTALLA = ALTO // 2
##

#
celda_seleccionada = None
ejecutando = True
matriz = []

#FONDO
# Colores
AMARILLO =(255, 255, 0)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
MORADO_OSCURO = (106,49,113)
ROJO = (255, 0, 0)
ROSA =(244, 143, 177)
ROSA_CLARO = (219, 164, 184)
ROSA_PASTEL = (225,179,176)
ROSA_OSCURO = (191, 94, 129)
VERDE= (0, 255, 0)


C_FUENTE = (255, 255, 255)
C_FONDO = (225,179,176)
C_BOTONES = (191, 94, 129)
C_BORDES = (106,49,113)
C_CELDA = (191, 94, 129)
C_TEXTBOX = (219, 164, 184)


MODO_ESCRITURA = "w"
MODO_LECTURA = "r"
MODO_APPEND = "a"
RUTA = "puntaje.txt"


def inicializar_matriz(cant_filas: int, cant_columnas: int, valor_inicial) -> list:
    """
    Crea y devuelve una matriz (lista de listas) con un número especificado de filas y columnas, 
    inicializando todos los elementos con un valor dado.

    Args:
        cant_filas (int): Número de filas de la matriz.
        cant_columnas (int): Número de columnas de la matriz.
        valor_inicial: Valor con el que se inicializarán todos los elementos de la matriz.
    
    Returns:
        list: Una matriz representada como una lista de listas, donde cada elemento tiene el valor especificado.
    
    """
    matriz = []
    for _ in range(cant_filas):
        fila = [valor_inicial] * cant_columnas
        matriz.append(fila)
    return matriz


matriz = inicializar_matriz(9, 9, None)
estados_celdas = inicializar_matriz(9, 9, None)  # Inicializa con None


def es_valido(matriz: list, fila: int, columna: int, numero: int) -> bool:
    """
    Verifica si es válido colocar un número en una posición específica dentro de una matriz,
    siguiendo las reglas de un tablero de Sudoku:

    Args:
        matriz (list): Una matriz 9x9 que representa el tablero de Sudoku.
        fila (int): El índice de la fila donde se desea colocar el número.
        columna (int): El índice de la columna donde se desea colocar el número.
        numero (int): El número a validar.

    Returns:
        bool: True si el número puede colocarse en la posición especificada 
              sin violar las reglas del Sudoku, False en caso contrario.
    """
    retorno = True
    if numero in matriz[fila]:
        retorno = False
    for i in range(9):
        if matriz[i][columna] == numero:
            retorno = False
    inicio_fila = (fila // 3) * 3
    inicio_columna = (columna // 3) * 3
    for i in range(inicio_fila, inicio_fila + 3):
        for j in range(inicio_columna, inicio_columna + 3):
            if matriz[i][j] == numero:
                retorno = False
    return retorno


def llenar_sudoku(matriz: list) -> bool:
    """
    Intenta llenar un tablero de Sudoku de forma recursiva, buscando una solución válida para el Sudoku.

    La función recorre el tablero en busca de una celda vacía y trata de colocar un número entre 1 y 9 en esa celda, asegurándose de que el número no viole las reglas del Sudoku. Si no se encuentra ninguna celda vacía, significa que el Sudoku está completo y se retorna True. Si no se puede encontrar un número válido para una celda, retrocede (backtracking) y prueba con otro número.

    Args:
        matriz (list): Una matriz 9x9 que representa el tablero de Sudoku, donde `None` representa las celdas vacías.

    Returns:
        bool: True si el Sudoku se ha llenado completamente de forma válida, False si no es posible llenar el tablero.

    """
    resultado = False  
    vacio_encontrado = False
    for fila in range(9):
        for columna in range(9):
            if matriz[fila][columna] is None:
                vacio_encontrado = True
                break
        if vacio_encontrado:
            break

    if not vacio_encontrado:
        resultado = True

    if resultado == False:
        numeros = list(range(1, 10))
        random.shuffle(numeros)
        for numero in numeros:
            if es_valido(matriz, fila, columna, numero):
                matriz[fila][columna] = numero
                resultado = llenar_sudoku(matriz)
                if resultado == True:
                    break
                matriz[fila][columna] = None

    return resultado  

    
def dibujar_teclado(pantalla: pygame.Surface, TAM_CELDA: int) -> None:
    """
    Dibuja el teclado en la interfaz de usuario de un Sudoku en la ventana de Pygame. El teclado está ubicado a la derecha del tablero, y permite al usuario seleccionar números del 1 al 9 o usar el botón de "Borrar".

    Args:
        pantalla (pygame.Surface): La superficie de la ventana donde se dibuja el teclado.
        TAM_CELDA (int): El tamaño de cada celda, que también determina el tamaño de las teclas y el botón de borrar.
    """
    # Teclado a la derecha de la pantalla
    ancho_teclado = 3 * TAM_CELDA
    alto_teclado = 4 * TAM_CELDA  # 3 filas de números y una fila para el botón de borrar
    pygame.draw.rect(pantalla, MORADO_OSCURO, (9 * TAM_CELDA, 0, ancho_teclado, alto_teclado))  # Fondo del teclado

    # Dibuja el botón de borrar con color cian
    borrar_rect = pygame.Rect(9 * TAM_CELDA, 0, TAM_CELDA, TAM_CELDA)
    pygame.draw.rect(pantalla, MORADO_OSCURO, borrar_rect) 
    font = pygame.font.Font(None, 45)
    texto = font.render("Borrar", True, BLANCO)
    pantalla.blit(texto, (9 * TAM_CELDA + TAM_CELDA // 4, TAM_CELDA // 4))

    # Dibuja las teclas del 1 al 9
    teclas = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i, tecla in enumerate(teclas):
        fila = i // 3  # Filas de teclas
        columna = i % 3  # Columnas de teclas
        x = 9 * TAM_CELDA + columna * TAM_CELDA
        y = TAM_CELDA + fila * TAM_CELDA
        rect = pygame.Rect(x, y, TAM_CELDA, TAM_CELDA)
        pygame.draw.rect(pantalla, MORADO_OSCURO, rect)
        texto = font.render(tecla, True, BLANCO)
        pantalla.blit(texto, (x + TAM_CELDA // 4, y + TAM_CELDA // 4))


def dibujar_tablero(pantalla: pygame.Surface, matriz: list, TAM_CELDA: int, celda_seleccionada: tuple) -> int:
    """Dibuja el tablero de Sudoku en la pantalla, resaltando la celda seleccionada y mostrando los números con colores que indican su estado. Tambien cuenta la cantidad de números acertados si el número se ingresa en verde.

    Args:
        pantalla (pygame.Surface): La superficie de Pygame donde se dibujará el tablero.
        matriz (list): Una lista bidimensional que representa el estado del tablero de Sudoku.
        TAM_CELDA (int): El tamaño de cada celda del tablero en píxeles.
        celda_seleccionada (tuple): Una tupla que indica la celda seleccionada. Si es "None", no se resalta ninguna celda.
    Returns:
        int: La cantidad de aciertos.
    """
    pantalla.fill(ROSA_PASTEL)  
    aciertos = 0
    for fila in range(len(matriz)):
        for columna in range(len(matriz)):
            rect = pygame.Rect(columna * TAM_CELDA, fila * TAM_CELDA, TAM_CELDA, TAM_CELDA)
            if celda_seleccionada == (fila, columna):
                pygame.draw.rect(pantalla, ROSA_OSCURO, rect)
            pygame.draw.rect(pantalla, BLANCO, rect, 1)
           
            if matriz[fila][columna] is not None:
                font = pygame.font.Font(None, 55)
                if estados_celdas[fila][columna] is True:
                    texto_color = VERDE
                    aciertos += 1
                elif estados_celdas[fila][columna] is False:
                    texto_color = ROJO
                else:
                    texto_color = BLANCO
                texto = font.render(str(matriz[fila][columna]), True, texto_color)
                
                texto_rect = texto.get_rect(center=(columna * TAM_CELDA + TAM_CELDA // 2, fila * TAM_CELDA + TAM_CELDA // 2))
                pantalla.blit(texto, (texto_rect))

    for i in range(1, 9):
        if i % 3 == 0:
            pygame.draw.line(pantalla, MORADO_OSCURO, (i * TAM_CELDA, 0), (i * TAM_CELDA, 9 * TAM_CELDA), 3)
            pygame.draw.line(pantalla, MORADO_OSCURO, (0, i * TAM_CELDA), (9 * TAM_CELDA, i * TAM_CELDA), 3)
    return aciertos


def procesar_click(evento:pygame.event, TAM_CELDA:int, celda_seleccionada:tuple)->tuple:
    """Procesa el clic del usuario y selecciona o desmarca la celda en el tablero.

    Args:
        evento (pygame.event): El evento de clic.
        TAM_CELDA (int): El tamaño de cada celda.
        celda_seleccionada (tuple): La celda seleccionada actualmente.

    Returns:
        tuple: La nueva celda seleccionada (o None si se desmarca).
    """
    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        x, y = evento.pos
        
        tablero_x, tablero_y = 0, 0  
        tablero_ancho = 9 * TAM_CELDA  
        tablero_alto = 9 * TAM_CELDA   
        
        if tablero_x <= x < tablero_x + tablero_ancho and tablero_y <= y < tablero_y + tablero_alto:
            celda_seleccionada = (y // TAM_CELDA, x // TAM_CELDA)
        else:
            celda_seleccionada = None
    
    return celda_seleccionada


def manejar_teclado_virtual(evento: pygame.event, matriz: list, celda_seleccionada: tuple) -> None:
    """
    Maneja los eventos del teclado virtual, permitiendo al usuario seleccionar un número del 1 al 9 o borrar el valor de una celda seleccionada en el tablero de Sudoku.
    La función reacciona a los clics del mouse sobre las teclas numeradas o el botón "Borrar". Si se hace clic sobre una tecla numerada, se ingresa ese número en la celda seleccionada. Si se hace clic sobre el botón "Borrar", se elimina el número de la celda seleccionada.

    Args:
        evento: El evento de Pygame que contiene la información sobre la acción del usuario, como el clic del mouse.
        matriz (list): Una matriz 9x9 que representa el tablero de Sudoku. Las celdas pueden contener números o `None` para celdas vacías.
        celda_seleccionada (tuple): Una tupla con los índices de la celda seleccionada (fila, columna), o `None` si no hay celda seleccionada.

    """
    if evento.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = evento.pos
        for i in range(9):
            fila = i // 3
            columna = i % 3
            tecla_rect = pygame.Rect(9 * TAM_CELDA + columna * TAM_CELDA, TAM_CELDA + fila * TAM_CELDA, TAM_CELDA, TAM_CELDA)
            if tecla_rect.collidepoint(mouse_x, mouse_y) and celda_seleccionada is not None:
                numero = i + 1
                fila, columna = celda_seleccionada
                if matriz[fila][columna] is None:
                    ingresar_numero(matriz,fila,columna,numero)
        borrar_rect = pygame.Rect(9 * TAM_CELDA, 0, TAM_CELDA, TAM_CELDA)
        if borrar_rect.collidepoint(mouse_x, mouse_y) and celda_seleccionada is not None:
            fila, columna = celda_seleccionada
            if estados_celdas[fila][columna] is not None:
                matriz[fila][columna] = None
                estados_celdas[fila][columna] = None


def ingresar_numero(matriz: list, fila: int, columna: int, numero: int) -> bool:
    """
    Intenta ingresar un número en la celda especificada del tablero de Sudoku y actualiza el estado de la celda según si el número es válido o no según las reglas del Sudoku.

    La función primero verifica si el número es válido en la celda seleccionada utilizando
    la función `es_valido`. Luego, si el número es válido, lo coloca en la matriz y actualiza
    el estado de la celda correspondiente en la lista "estados_celdas" a True o False 
    según si el número es válido para esa celda.

    Args:
        matriz (list): Una matriz 9x9 que representa el tablero de Sudoku, donde las celdas pueden contener números o None si están vacías.
        fila (int): El índice de la fila en la que se desea ingresar el número (entre 0 y 8).
        columna (int): El índice de la columna en la que se desea ingresar el número (entre 0 y 8).
        numero (int): El número que se desea ingresar en la celda seleccionada (debe estar entre 1 y 9).

    Returns:
        bool: True si el número es válido y se ha ingresado correctamente en la celda, False si el número no es válido y no se ingresa en la celda.
    """
    es_valido_para_ingresar = es_valido(matriz, fila, columna, numero)
    matriz[fila][columna] = numero
    estados_celdas[fila][columna] = es_valido_para_ingresar
    return es_valido_para_ingresar


def ocultar_numeros(matriz: list, dato_dificultad: str) -> int:
    """
    Oculta una cantidad específica de números en el tablero de Sudoku al establecerlos como `None`.

    Args:
        matriz (list): Matriz del Sudoku.
        cantidad (int): Número de celdas a ocultar.

    Returns: 
        int: La cantidad de celdas ocultadas
    """
    if dato_dificultad == "Facil":
        porcentaje = 20
    elif dato_dificultad == "Moderado":
        porcentaje = 40
    elif dato_dificultad == "Dificil":
        porcentaje = 60
        
    cantidad = (81 * porcentaje) // 100
    filas = len(matriz)
    columnas = len(matriz[0])
    celdas_ocultadas = 0

    while celdas_ocultadas < cantidad:
        fila = random.randint(0, filas - 1)
        columna = random.randint(0, columnas - 1)

        if matriz[fila][columna] is not None:
            matriz[fila][columna] = None
            celdas_ocultadas += 1
    return celdas_ocultadas


def puntaje(intentos_fallidos:int,tiempo:int,nivel:str)->float:
    """Calcula el puntaje final basado en los intentos fallidos, el tiempo transcurrido y el nivel de dificultad.

    Args:
        intentos_fallidos (int): El número de intentos fallidos realizados por el jugador.
        tiempo (int): El tiempo transcurrido en segundos.
        nivel (str): El nivel de dificultad del juego. Puede ser "Facil", "Moderado" o "Dificil".

    Returns:
        float: El puntaje total calculado.
    """
    puntos_base = 1000
    penalizacion=50

    if nivel == "Facil":
        dificultad = 1.0   
    elif nivel == "Moderado":
        dificultad = 1.5
    elif nivel == "Dificil":
        dificultad = 2
    total= (puntos_base -(intentos_fallidos * penalizacion)-(tiempo*10))*dificultad 
    return total


def escribir_texto(texto:str, fuente:pygame.font.Font, color:tuple, pantalla:pygame.Surface, x:int, y:int)->None:
    """Dibuja un texto en una posición específica de la pantalla de Pygame.

    Args:
        texto (str): El texto que se desea mostrar.
        fuente (pygame.font.Font): La fuente utilizada para renderizar el texto.
        color (tuple): El color del texto en formato RGB (por ejemplo, `(255, 255, 255)` para blanco).
        pantalla (pygame.Surface): La superficie de Pygame donde se dibujará el texto.
        x (int): La posición horizontal (en píxeles) donde se dibujará el texto.
        y (int): La posición vertical (en píxeles) donde se dibujará el texto.
        """
    textobj = fuente.render(texto, 1, color)
    textorect = textobj.get_rect()
    textorect.topleft = (x, y)
    pantalla.blit(textobj, textorect)


def poner_musica(ruta):
    """Inicia la reproducción de la música del menú de inicio, deteniendo cualquier música que esté en reproducción actualmente. La música se repite indefinidamente en bucle y se establece un volumen bajo.
    """
    mixer.music.stop()
    mixer.music.load(f"{ruta}")
    mixer.music.play(-1)
    mixer.music.set_volume(0.2)


def tomar_tiempo(pantalla:pygame.Surface,tiempo:int,evento:pygame.event,fuente:pygame.font.Font,reloj:tuple)->int:
    """Actualiza y muestra un temporizador en la pantalla basado en eventos de tiempo personalizados. La función incrementa los segundos en un diccionario "reloj" cuando ocurre un evento de tipo "tiempo". Si los segundos alcanzan 60, se incrementan los minutos. El temporizador se reinicia automáticamente si los minutos alcanzan 60. El tiempo transcurrido se dibuja en la pantalla en formato "Min:Seg".

    Args:
        pantalla (pygame.Surface): La superficie de Pygame donde se dibujará el tiempo.
        tiempo (int): El identificador del evento de tiempo personalizado (por ejemplo, `pygame.USEREVENT`).
        evento(pygame.event): El evento actual del bucle principal de Pygame.
        fuente (pygame.font.Font): La fuente utilizada para renderizar el texto del tiempo.
        reloj (dict): Un diccionario que contiene las claves "minutos" y "segundos" para llevar el registro del tiempo transcurrido. Ejemplo: `{"minutos": 0, "segundos": 0}`.

    Returns:
        int: El número de minutos transcurridos.
    """
    if evento.type == tiempo:
        reloj["segundos"] += 1
    if reloj["segundos"] == 60:
        reloj["segundos"] = 0
        reloj["minutos"] += 1
    if reloj["minutos"] == 60:
        reloj["segundos"] = 0
        reloj["minutos"] = 0
    tiempo_transcurrido= fuente.render((f"{reloj['minutos']:02d}:{reloj['segundos']:02d}"),(250, 250, 250), (0, 0, 0))
    pantalla.blit(tiempo_transcurrido,(630,500))
    return reloj["minutos"]


def contar_error(matriz:list, numero:int,celda:tuple,lista:list)->int:
    """ Verifica si un número en una celda específica del tablero es incorrecto y, de ser así, lo agrega a una lista de errores. Luego, calcula y devuelve el total de errores acumulados.

    Args:
        matriz (list): Una matriz 9x9 que representa el tablero de Sudoku.
        numero (int): El número que se está evaluando.
        celda (tuple): Una tupla `(fila, columna)` que indica la posición de la celda en la matriz.
        lista (list): Una lista donde se almacenan los números incorrectos encontrados.

    Returns:
        int: La cantidad total de errores acumulados en la lista.
        """
    fila,columna = celda
    if matriz[fila][columna] is not None:
            if estados_celdas [fila][columna]is False:
                lista.append(numero)
    errores = len(lista)
    return errores


def ilustrador_errores(pantalla:pygame.Surface,mensaje:int, fuente:pygame.font.Font):
    """
    Dibuja un recuadro en la pantalla para mostrar el número de errores cometidos durante el juego. La función crea un rectángulo con un encabezado "Errores" y muestra el número de errores proporcionado por el parámetro "mensaje".

    Args:
        pantalla (pygame.Surface): La superficie de Pygame donde se dibujará el recuadro de errores.
        mensaje (int): El número de errores que se desea mostrar.
        fuente (pygame.font.Font): La fuente que se utilizará para renderizar el texto.
        """
    pygame.draw.rect(pantalla,ROSA,(600,240,100,38)) 
    escribir_texto("Errores", fuente, BLANCO, pantalla, 605,245)
    contador = fuente.render(f"{mensaje}", True,(BLANCO))
    pantalla.blit(contador,(670,283))


def dibujar_btt_volver(pantalla: pygame.Surface, TAM_CELDA: int) -> tuple[pygame.Rect]:
    """Dibuja un botón "volver" en la pantalla y retorna su rectángulo para manejar colisiones o eventos.

    Args:
        pantalla (pygame.Surface): La superficie de Pygame donde se dibuja el botón.
        TAM_CELDA (int): Tamaño de una celda en píxeles, usado para calcular la posición del botón.

    Returns:
        pygame.Rect: El rectángulo que delimita el botón, útil para detectar clics o colisiones.
    """
    ANCHO_BUTT_VOLVER = ANCHO - 100
    ALTO_BOTON = 7*TAM_CELDA
    butt_img_volver = pygame.image.load("imagenes/boton_volver.png").convert_alpha()

    
    butt_volver = butt_img_volver.get_rect()
    butt_volver.center = (ANCHO_BUTT_VOLVER, ALTO_BOTON)

    pantalla.blit(butt_img_volver, butt_volver)


    return butt_volver


def dibujar_btt_reinicio(pantalla: pygame.Surface, TAM_CELDA: int) -> tuple[pygame.Rect]:
    """Dibuja un botón "reinicio" en la pantalla y retorna su rectángulo para manejar eventos o interacciones.

    Args:
        pantalla (pygame.Surface): La superficie de Pygame donde se dibuja el botón.
        TAM_CELDA (int): Tamaño de una celda en píxeles, usado para calcular la posición del botón.

    Returns:
        pygame.Rect: El rectángulo que delimita el botón, útil para detectar clics o colisiones.
    """
    ANCHO_BUTT_REINICIO = ANCHO - 25
    ALTO_BOTON = 7*TAM_CELDA
    butt_img_reinicio = pygame.image.load("imagenes/boton_reinicio.png").convert_alpha()
    
    butt_reinicio = butt_img_reinicio.get_rect()
    butt_reinicio.center = (ANCHO_BUTT_REINICIO, ALTO_BOTON)

    pantalla.blit(butt_img_reinicio, butt_reinicio)

    return butt_reinicio


def contar_puntaje(intentos_fallidos:int,tiempo:int,nivel:str)->float:
    """Calcula el puntaje total basado en los intentos fallidos, el tiempo transcurrido, y el nivel de dificultad del juego.

    Args:
        intentos_fallidos (int): Número de intentos fallidos por parte del jugador.
        tiempo (int): Tiempo transcurrido en segundos.
        nivel (str): Nivel de dificultad, puede ser "Facil", "Moderado" o "Dificil".

    Returns:
        float: El puntaje total calculado.    
    """
    puntos_base = 1000
    penalizacion=50

    if nivel == "Facil":
        dificultad = 1.0   
    elif nivel == "Moderado":
        dificultad = 1.5
    elif nivel == "Dificil":
        dificultad = 2
    total= (puntos_base -(intentos_fallidos * penalizacion)-(tiempo*10))*dificultad 
    return total


def elegir_mayor_puntuacion(lista_jugadores:list,puntaje:int,jugador1:str)->list:
    """Administra una lista de jugadores, actualizando sus puntuaciones para mantener un máximo de 5 jugadores con las mejores puntuaciones.
    Si la lista tiene menos de 5 jugadores, se agrega el nuevo jugador con su puntuación.
    Si ya hay 5 jugadores, el jugador con la puntuación más baja será reemplazado si la nueva puntuación es mayor.
    Si el jugador consigue una puntuacion negativa, se queda con un puntaje de valor 0.

    Args:
        lista_jugadores (list): Lista de diccionarios, donde cada diccionario representa un jugador con las claves "nombre" y "puntuacion".
        puntaje (int): Puntuación del jugador a agregar o comparar.
        jugador (str): Nombre del jugador a agregar.
    Returns:
        devuelve una lista hasta de 5 jugadores con el puntaje mas alto.
    """
    jugador = jugador1.strip("\r")
    minimo_puntaje = None
    jugador_poco_puntaje = None
    puntaje = int(puntaje)
    if puntaje < 0:
        puntaje = 0
    if len(lista_jugadores) < 5: 
        lista_jugadores.append({"nombre": jugador, "puntuacion": puntaje})
    else:
        for gamer in lista_jugadores:
            if minimo_puntaje == None or gamer["puntuacion"] < minimo_puntaje:
                minimo_puntaje = gamer["puntuacion"]
                jugador_poco_puntaje = gamer
        
        if minimo_puntaje < puntaje:
            lista_jugadores.append({"nombre": jugador, "puntuacion": puntaje})
            lista_jugadores.remove(jugador_poco_puntaje)
    
    
    return lista_jugadores


def ilustrar_puntos(lista_jugadores:list,pantalla:pygame.Surface,altura:int = 100)->None:
    """Dibuja los nombres y puntuaciones de los jugadores en la pantalla usando Pygame.

    Args:
        lista_jugadores (list): Lista de diccionarios, donde cada diccionario contiene al menos las claves "nombre" (str) y "puntuacion" (int o float).
        pantalla (pygame.Surface): Superficie de Pygame donde se dibujarán los textos.
        altura (int): Posición inicial en el eje Y para comenzar a dibujar los textos.
    """
    for gamer in lista_jugadores:
        font = pygame.font.Font(None, 32) 
        texto_participantes = font.render(f"{gamer['nombre']}:  {gamer['puntuacion']}", True, (250, 250, 250))
        pantalla.blit(texto_participantes,( 280, altura))
        altura += 40


def ordenar_lista(lista_jugadores: list):
    """Ordena una lista de jugadores en orden descendente según su puntuación.

    Args:
        lista_jugadores (list): Lista de diccionarios, donde cada diccionario representa a un jugador con al menos una clave "puntuacion" que contiene un valor numérico.
    """
    for i in range(len(lista_jugadores)-1):
        for j in range(i + 1, len(lista_jugadores)):
            if lista_jugadores[i]["puntuacion"] < lista_jugadores[j]["puntuacion"]:
                aux = lista_jugadores[i]
                lista_jugadores[i] = lista_jugadores[j]
                lista_jugadores[j] = aux


def guardar_puntajes(lista:list[dict], ruta:str):
    """"Recibe una lista y la guarda en un archivo txt
    
    Args:
        lista(list[dict]):Lista de diccionarios, donde cada diccionario representa a un jugador con al menos una clave "puntuacion" que contiene un valor numérico.
        ruta(str):recibe por parametro el nombre del txt o la ruta de direccion donde se encuentra
    """
    with open (ruta,MODO_ESCRITURA)as archivo:
            json.dump(lista,archivo, indent = 4)


def cargar_puntajes(ruta:str)->list[dict]:
    """"Carga el archivo txt previamente guardado o tambien lo inicializa con una lista vacia en caso de que no exista o tenga un error en la lectura.
    Args:
        ruta(str):recibe por parametro el nombre del txt o la ruta de direccion donde se encuentra.
    Returns:
        devuelve un lista de diccionario,ya sea vacio o un diccionario guardado.
    """
    datos = []
    try:
        with open(ruta, MODO_LECTURA) as archivo:
            
            datos= json.load(archivo)
    except json.decoder.JSONDecodeError:
        pass
    except FileNotFoundError:
        pass
    return datos