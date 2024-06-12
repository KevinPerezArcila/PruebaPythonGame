import random, time, pygame, sys

class Meteorito:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.estado = "normal"
        self.imagen_normal = pygame.image.load('imagenes/meteorito.png')
        self.ancho = self.imagen_normal.get_width()
        self.alto = self.imagen_normal.get_height()
        self.imagen_impactado = pygame.image.load('imagenes/meteorito_impactado.png')
        self.imagen_destruido = pygame.image.load('imagenes/meteorito_destruido.png')
        self.velecidad = 1.5
        self.imagen_actual = self.imagen_normal

    def impactar(self):
        if self.estado == "normal":
            self.estado = "impactado"
            self.imagen_actual = self.imagen_impactado
        elif self.estado == "impactado":
            self.estado = "destruido"
            self.imagen_actual = self.imagen_destruido

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen_actual, (self.x, self.y))

    def colliderect(self, other_rect):
        self_rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        return self_rect.colliderect(other_rect)

def movimiento_nave(teclas_juego, x_nave, y_nave, mov_nave, nave, control_wasd):
    if control_wasd:
        if teclas_juego[pygame.K_w]:
            y_nave -= mov_nave
        if teclas_juego[pygame.K_s] and y_nave + nave.get_height() < 530:
            y_nave += mov_nave
        if teclas_juego[pygame.K_a]:
            x_nave -= mov_nave
        if teclas_juego[pygame.K_d]:
            x_nave += mov_nave
    else:
        if teclas_juego[pygame.K_UP]:
            y_nave -= mov_nave
        if teclas_juego[pygame.K_DOWN] and y_nave + nave.get_height() < 530:
            y_nave += mov_nave
        if teclas_juego[pygame.K_LEFT]:
            x_nave -= mov_nave
        if teclas_juego[pygame.K_RIGHT]:
            x_nave += mov_nave
    if x_nave < 0:
        x_nave = 0
    if x_nave > pantalla.get_width() - nave.get_width():
        x_nave = pantalla.get_width() - nave.get_width()
    if y_nave < 0:
        y_nave = 0
    if y_nave + nave.get_height() > 530:
        y_nave = 530 - nave.get_height()
    return x_nave, y_nave

def eventos_disparo_salida ():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            #nuevo_rayo = Rayo(x_nave + nave.get_width() / 2 - 1, y_nave)
            #rayos.append(nuevo_rayo)
            return True
    return False


class Rayo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 5
        self.imagen = pygame.Surface((3, 10))
        self.imagen.fill((255, 255, 255))

    def actualizar(self):
        self.y -= self.velocidad

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))



def iniciar_gameplay(pantalla, gameplay, nave, control_wasd, meteorito):

    x_nave = (pantalla.get_width() - nave.get_width()) / 2
    y_nave = 465 #480 limite
    mov_nave = 2

    meteoritos = []
    tiempo_ult_meteorito = time.time()
    juego_terminado = False

    #mov_meteorito = 1

    rayos = []

    while not juego_terminado:
        pantalla.blit(gameplay, (0, 0))
        pantalla.blit(nave, (x_nave, y_nave))

        tiempo_actual = time.time()

        rect_nave = pygame.Rect(x_nave, y_nave, nave.get_width(), nave.get_height())

        if eventos_disparo_salida():
            nuevo_rayo = Rayo(x_nave + nave.get_width() / 2 - 1, y_nave)
            rayos.append(nuevo_rayo)

        teclas_juego = pygame.key.get_pressed()
        x_nave, y_nave = movimiento_nave(teclas_juego, x_nave, y_nave, mov_nave, nave, control_wasd)

        if tiempo_actual - tiempo_ult_meteorito > 1.5:
            if len(meteoritos) < 5:
                x_meteorito = random.randint(0, pantalla.get_width() - meteorito.get_width())
                y_meteorito = -meteorito.get_height()
                nuevo_meteorito = Meteorito(x_meteorito, y_meteorito)
                meteoritos.append(nuevo_meteorito)
            tiempo_ult_meteorito = tiempo_actual

        for meteorito_pos in meteoritos[:]:
            #pantalla.blit(meteorito, meteorito_pos)
            meteorito_pos.dibujar(pantalla)
            #pantalla.blit(meteorito_pos.imagen_actual, (meteorito_pos.x, meteorito_pos.y))
            #meteorito_pos.y += 1.5
            if meteorito_pos.velecidad < 3:
                meteorito_pos.velecidad += 0.01
            meteorito_pos.y += meteorito_pos.velecidad

            if meteorito_pos.estado != "destruido":
                for rayo in rayos:
                    if pygame.Rect(meteorito_pos.x, meteorito_pos.y, meteorito_pos.imagen_normal.get_width(),
                                   meteorito_pos.imagen_normal.get_height()).colliderect(
                        pygame.Rect(rayo.x, rayo.y, 3, 10)):
                        meteorito_pos.impactar()
                        rayos.remove(rayo)
            else:
                meteoritos.remove(meteorito_pos)

            if meteorito_pos.colliderect(rect_nave):
                juego_terminado = True


            if meteorito_pos.y > 560:
                #meteoritos.remove(meteorito_pos)
                juego_terminado = True

        if x_nave < 0:
            x_nave = 0
        if x_nave > pantalla.get_width() - nave.get_width():
            x_nave = pantalla.get_width() - nave.get_width()
        if y_nave < 0:
            y_nave = 0
        if y_nave + nave.get_height() > 530:
            y_nave = 530 - nave.get_height()

        #y_meteorito += mov_meteorito
        for rayo in rayos:
            rayo.actualizar()
            rayo.dibujar(pantalla)

        pygame.display.update()
    menu(pantalla, menu_inicial, menu_opciones, gameplay, nave, meteorito)

def menu(pantalla, menu_inicial, menu_opciones, gameplay, nave, meteorito):
    mostrar_menu = True
    mostrar_opciones = False
    control_wasd = True

    while True:
        if mostrar_menu:
            pantalla.blit(menu_inicial, (0, 0))
        elif mostrar_opciones:
            pantalla.blit(menu_opciones, (0,0))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos

                    if mostrar_menu:
                        boton_iniciar = pygame.Rect(135, 185, 232, 69)
                        if boton_iniciar.collidepoint(mouse_x, mouse_y):
                            mostrar_menu = False
                            mostrar_opciones = False
                            iniciar_gameplay(pantalla, gameplay, nave, control_wasd, meteorito)
                            print("boton_iniciar")

                        boton_opciones = pygame.Rect(135, 328, 226, 70)
                        if boton_opciones.collidepoint(mouse_x, mouse_y):
                            pantalla.fill((0, 0, 0))
                            mostrar_menu = False
                            mostrar_opciones = True
                            pygame.display.update()
                            print("boton_opciones")

                        boton_salir = pygame.Rect(135, 477, 231, 66)
                        if boton_salir.collidepoint(mouse_x, mouse_y):
                            print("Fin del juego")
                            pygame.quit()
                            sys.exit()

                    elif mostrar_opciones:
                        #boton_volver = pygame.Rect(135,185, 232, 69)
                        print(f"Se hizo clic en la posición ({mouse_x}, {mouse_y})") #Me ayuda a comprobar donde esta mi mouse a la horad e dar clic

                        boton_mov_awsd = pygame.Rect(337, 202, 101, 60)
                        if boton_mov_awsd.collidepoint(mouse_x, mouse_y):
                            control_wasd = True
                            print("awsd")

                        boton_mov_flechas = pygame.Rect(337, 390, 69, 59)
                        if boton_mov_flechas.collidepoint(mouse_x, mouse_y):
                            control_wasd = False
                            print("flechas")

                        boton_mov_guardar = pygame.Rect(138, 551, 229, 65)
                        if boton_mov_guardar.collidepoint(mouse_x, mouse_y):
                            mostrar_menu = True
                            mostrar_opciones = False
                            pygame.display.update()
                            print("guardar")

if __name__ == '__main__':
    pygame.init()
    pantalla = pygame.display.set_mode((506, 650))
    pygame.display.set_caption('Menú del Juego')
    menu_inicial = pygame.image.load('imagenes/menu.png')
    menu_opciones = pygame.image.load('imagenes/menu_opciones.png')
    gameplay = pygame.image.load('imagenes/gameplay v2.png')
    nave = pygame.image.load('imagenes/nave.png')
    meteorito = pygame.image.load('imagenes/meteorito.png')
    mostrar_fondo_gameplay = False
    fin = False


    # Mostrar el menú inicial
    menu(pantalla, menu_inicial, menu_opciones, gameplay, nave, meteorito)

    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin = True

    print('Fin del juego')
    pygame.quit()
    sys.exit()
