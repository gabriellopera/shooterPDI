import pygame
import cv2
import numpy as np
import imutils
import random
import threading

# Definir los colores
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (255, 0, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()

# Iniciar la captura de video desde la cámara
cap = cv2.VideoCapture(0)

# Verificar si la cámara se abrió correctamente
if not cap.isOpened():
    print("Error al abrir la cámara.")
    exit()

# Bucle para mostrar la captura de video en una ventana de OpenCV
def capture_video():
    while True:
        # Capturar cuadro a cuadro
        ret, frame = cap.read()

        # Verificar si se pudo capturar el cuadro correctamente
        if not ret:
            print("Error al capturar el cuadro.")
            break
        
        # Voltear horizontalmente la imagen
        frame = cv2.flip(frame, 1)
        
        # Redimensionar el cuadro a 400x300 píxeles
        frame = cv2.resize(frame, (400, 300))

        # Convertir el fotograma de BGR a espacio de color HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Definir el rango de color verde en HSV
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([80, 255, 255])

        # Definir el rango de color azul en HSV
        lower_blue = np.array([100, 150, 0])
        upper_blue = np.array([140, 255, 255])

        # Umbralizar la imagen HSV para obtener solo colores verdes
        mask_green = cv2.inRange(hsv, lower_green, upper_green)
        # Umbralizar la imagen HSV para obtener solo colores azules
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

       # Encontrar contornos en la máscara verde
        contours_green, _ = cv2.findContours(mask_green.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
       # Encontrar contornos en la máscara azul
        contours_blue, _ = cv2.findContours(mask_blue.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        # Dibujar contornos y siluetas alrededor de los objetos verdes
        for contour in contours_green:
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)  # Dibuja contorno verde
            # Dibujar silueta alrededor del objeto verde
            rect = cv2.boundingRect(contour)
            x, y, w, h = rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Dibuja rectángulo verde

        # Dibujar contornos y siluetas alrededor de los objetos azules
        for contour in contours_blue:
            cv2.drawContours(frame, [contour], -1, (255, 0, 0), 2)  # Dibuja contorno azul
            # Dibujar silueta alrededor del objeto azul
            rect = cv2.boundingRect(contour)
            x, y, w, h = rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Dibuja rectángulo azul
        
        # Mostrar el cuadro en una ventana
        cv2.imshow('Video', frame)

        # Esperar 1 milisegundo y verificar si se presionó la tecla 'q' para salir del bucle
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # Liberar la captura de video y cerrar la ventana de OpenCV
    cap.release()
    cv2.destroyAllWindows()

# Iniciar el hilo para capturar el video
video_thread = threading.Thread(target=capture_video)
video_thread.start()

# Función para dibujar texto
def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Función para dibujar la barra de escudo
def draw_shield_bar(surface, x, y, percentage):
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGTH
    border = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill)
    pygame.draw.rect(surface, WHITE, border, 2)

# Clase para el jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.shield = 100

    def update(self):
        self.speed_x = 0
        # Obtener el fotograma de video de la cámara
        ret, frame = cap.read()
        if ret:
            # Voltear horizontalmente la imagen
            frame = cv2.flip(frame, 1)
            # Convertir el fotograma de BGR a espacio de color HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Definir el rango de color verde en HSV
            lower_green = np.array([40, 40, 40])
            upper_green = np.array([80, 255, 255])

            # Umbralizar la imagen HSV para obtener solo colores verdes
            mask_green = cv2.inRange(hsv, lower_green, upper_green)

            # Definir el rango de color azul en HSV
            lower_blue = np.array([100, 150, 0])
            upper_blue = np.array([140, 255, 255])

            # Umbralizar la imagen HSV para obtener solo colores azules
            mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

            # Encontrar contornos en la máscara verde
            contours_green = cv2.findContours(mask_green.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours_green = imutils.grab_contours(contours_green)

            # Encontrar contornos en la máscara azul
            contours_blue = cv2.findContours(mask_blue.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours_blue = imutils.grab_contours(contours_blue)

             # Dibujar contornos alrededor de los objetos verdes
            for contour in contours_green:
                 cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)  # Dibuja contorno verde

            # Dibujar rectángulos alrededor de los objetos azules
            for contour in contours_blue:
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Dibuja rectángulo azul
            if len(contours_blue) > 0:
                # player.shoot() se activa si se detecta un objeto de color azul
                self.shoot()

            if len(contours_green) > 0:
                # Obtener el contorno más grande (objeto verde)
                c_green = max(contours_green, key=cv2.contourArea)
                M_green = cv2.moments(c_green)
                if M_green["m00"] != 0:
                    cX_green = int(M_green["m10"] / M_green["m00"])
                    # Mover el jugador basado en la posición X del objeto verde
                    if cX_green < self.rect.centerx:
                        self.speed_x = -8
                    elif cX_green > self.rect.centerx:
                        self.speed_x = 8

        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Clase para el meteorito
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-140, -100)
            self.speedy = random.randrange(1, 10)

# Clase para la bala
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/laser1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  # VELOCIDAD DE LA EXPLOSION

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# Función para mostrar la pantalla de inicio
def show_go_screen():
    screen.blit(background, [0, 0])
    draw_text(screen, "SHOOTER", 65, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "Instrucciones van aquí", 27, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "Press Key", 20, WIDTH // 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# Cargar imágenes de meteoritos
meteor_images = []
meteor_list = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png",
               "assets/meteorGrey_big4.png",
               "assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png", "assets/meteorGrey_small1.png",
               "assets/meteorGrey_small2.png",
               "assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png"]
for img in meteor_list:
    meteor_images.append(pygame.image.load(img).convert())

# ----------------EXPLOSTION IMAGENES --------------
explosion_anim = []
for i in range(9):
    file = "assets/regularExplosion0{}.png".format(i)
    img = pygame.image.load(file).convert()
    img.set_colorkey(BLACK)
    img_scale = pygame.transform.scale(img, (70, 70))
    explosion_anim.append(img_scale)

# Cargar imagen de fondo
background = pygame.image.load("assets/background.png").convert()

# Iniciar música
pygame.mixer.music.load("assets/music.ogg")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops=-1)

# ----------GAME OVER
game_over = True
running = True
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        meteor_list = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            meteor = Meteor()
            all_sprites.add(meteor)
            meteor_list.add(meteor)
        score = 0

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # colisiones - meteoro - laser
    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
    for hit in hits:
        score += 10
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)

    # Checar colisiones - jugador - meteoro
    hits = pygame.sprite.spritecollide(player, meteor_list, True)
    for hit in hits:
        player.shield -= 25
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)
        if player.shield <= 0:
            game_over = True

    screen.blit(background, [0, 0])
    all_sprites.draw(screen)

    # Marcador
    draw_text(screen, str(score), 25, WIDTH // 2, 10)

    # Escudo.
    draw_shield_bar(screen, 5, 5, player.shield)

    pygame.display.flip()

# Liberar la cámara y cerrar la ventana de Pygame
cap.release()
pygame.quit()
