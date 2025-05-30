import pygame, sys, random, math

# Inicializar lib
pygame.init()

def start_text():
    global screen, start, cuenta_regresiva
    if start and not cuenta_regresiva:
        font = pygame.font.SysFont(None, 50)
        texto = font.render("Presiona ESPACIO para empezar", True, white)     
        screen.blit(texto, (ancho // 2 - 270, alto // 2 + 150))

def reset_players():
    global player1, player2
    
    player1.rect.x = 50
    player1.rect.y = alto/2 - player_height/2
    player2.rect.x = 750
    player2.rect.y = alto/2 - player_height/2

def reset_ball_direction():
    global ball_velocity
    speed = ball_velocity * 1.5 

    while True:
        
        angle_deg = random.uniform(20, 70)
        angle_rad = math.radians(angle_deg)

        vel_x = speed * math.cos(angle_rad)
        vel_y = speed * math.sin(angle_rad)

        vel_x *= random.choice([-1, 1])
        vel_y *= random.choice([-1, 1])
        
        if abs(vel_x) < 1: 
            continue

        return vel_x, vel_y

def draw_score():
    global player1_score, player2_score, screen

    font = pygame.font.SysFont(None, 50, True)
    score_p1 = font.render(f"{player1_score}", True, player1_color)  
    score_p2 = font.render(f"{player2_score}", True, player2_color)     
    screen.blit(score_p1, ( 20, 20))
    screen.blit(score_p2, ( ancho - 40, 20))

def count_down():
    global pause, screen, cuenta_regresiva, start

    if cuenta_regresiva or pause:
        time  = (pygame.time.get_ticks() - tiempo_pausa) // 1000
        restante = max(0, 3 - time) 

        font = pygame.font.SysFont(None, 50)
        texto = font.render("Preparate", True, white)
        texto_num = font.render(f"{restante}", True, white)
        
        screen.blit(texto, (ancho // 2 - 85, 20))
        screen.blit(texto_num, (ancho // 2 - 10, 70))

        if restante == 0:
            cuenta_regresiva = False
            pause = False
            start = False

def ball_movement():
    global ball, pause, start
    if not pause and not start:
        ball.move()

def verify_point():
    global player1_score, player2_score, pause, tiempo_pausa, start_time

    if ball.rect.left <= 0: 
        player2_score += 1
        ball.rect.center = (ancho // 2, alto // 2)
        ball.vel_x, ball.vel_y = reset_ball_direction()
        start_time = 0
        pause = True
        tiempo_pausa = pygame.time.get_ticks()
        reset_players()

    if ball.rect.right >= ancho:
        player1_score += 1
        ball.rect.center = (ancho // 2, alto // 2) 
        ball.vel_x, ball.vel_y = reset_ball_direction()
        start_time = 0
        pause = True
        tiempo_pausa = pygame.time.get_ticks()
        reset_players()
 
def dificult_increase():
    global ball, start_time
    start_time = round(start_time, 2)
    match start_time:
        case 8.00:
            ball.vel_x += 1.2 if ball.vel_x > 0 else -1
            ball.vel_y += 1.2 if ball.vel_y > 0 else -1
        case 13.00:
            ball.vel_x += 2.5 if ball.vel_x > 0 else -2
            ball.vel_y += 2.5 if ball.vel_y > 0 else -2
        case 20.00:
            ball.vel_x += 3.5 if ball.vel_x > 0 else -5
            ball.vel_y += 3.5 if ball.vel_y > 0 else -5

# Colores
player1_color = (0,255,255)
player2_color = (255,0,127)
ball_color = (128,255,0)
bg_color = (0,0,0)
white = (255,255,255)

alto = 600
ancho = 800
size = (ancho,alto)

# Propiedades players
velocity = 8
player_height = 150
player_width = 20

# Propiedades pelota 
ball_velocity:float = 6.5

# Crear ventana
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong")

# Contadores de punto
player1_score:int = 0
player2_score:int = 0

class Ball:
    def __init__(self, x, y, radio, color, vel, ):
        self.rect = pygame.Rect(x, y, radio*2, radio*2)
        self.color = color
        self.vel_x = vel * random.choice([-1, 1])
        self.vel_y = vel * random.choice([-1, 1])

    def move(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Rebote con los bordes superior e inferior
        if self.rect.top <= 0 or self.rect.bottom >= alto:
            self.vel_y *= -1
        
        # colision con jugadores
        if self.rect.colliderect(player1.rect) or self.rect.colliderect(player2.rect):
            self.vel_x *= -1

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)


class Player:
    def __init__(self, x, y, alto, ancho, color, vel):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.hitbox = self.rect.inflate(-4, -10)
        self.color = color
        self.vel = vel

    def move(self, up, down):
        global pause, start

        # Sacar lista de teclas presionadas
        keys = pygame.key.get_pressed()

        if not pause and not start:
            if keys[up] and self.rect.top > 0:
                self.rect.y -= self.vel
            if keys[down] and self.rect.bottom < alto:
                self.rect.y += self.vel

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

# Crear objetos
player1 = Player(50, alto/2 - player_height/2, player_height, player_width, player1_color,velocity)
player2 = Player(750, alto/2 - player_height/2, player_height, player_width, player2_color, velocity)
ball = Ball(ancho // 2, alto // 2, 12, ball_color, ball_velocity)

start_time = pygame.time.get_ticks()

# Pausa por punto
pause = False
tiempo_pausa = 0

start = True
cuenta_regresiva = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not cuenta_regresiva:
                cuenta_regresiva = True
                tiempo_pausa = pygame.time.get_ticks()
   
    dificult_increase()
    verify_point()
    ball_movement()

    # Mover Players
    player1.move(pygame.K_w, pygame.K_s)
    player2.move(pygame.K_UP, pygame.K_DOWN)

    # Llenar pantalla con objetos
    screen.fill(bg_color)
    player1.draw(screen)
    player2.draw(screen)
    
    # Pelota
    ball.draw(screen)

    # Render cuenta regresiva
    count_down()
    start_text()

    # Render puntos jugadores
    draw_score()
    
    # Renderizar 
    pygame.display.flip()
    pygame.time.Clock().tick(60)