import pygame
import random

# Inicializar o Pygame
pygame.init()

# Configurar as dimensões da tela e as cores
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configurar as dimensões e velocidades dos elementos do jogo
BALL_SIZE = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 6
AI_PADDLE_SPEED = 4  # Velocidade da IA
BALL_SPEED_X, BALL_SPEED_Y = 5, 5
WINNING_SCORE = 10

# Criar a janela do jogo
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Função para desenhar a tela
def draw_screen(ball, left_paddle, right_paddle, left_score, right_score):
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    font = pygame.font.Font(None, 74)
    left_text = font.render(str(left_score), True, WHITE)
    screen.blit(left_text, (WIDTH // 4, 10))
    right_text = font.render(str(right_score), True, WHITE)
    screen.blit(right_text, (WIDTH * 3 // 4, 10))
    pygame.display.flip()

# Função para reiniciar a bola
def reset_ball():
    return pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE), BALL_SPEED_X * random.choice((-1, 1)), BALL_SPEED_Y * random.choice((-1, 1))

# Função para exibir o menu
def draw_menu():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    title = font.render("Pong", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

    font = pygame.font.Font(None, 36)
    option1 = font.render("1. Play vs AI", True, WHITE)
    screen.blit(option1, (WIDTH // 2 - option1.get_width() // 2, HEIGHT // 2 - 20))

    option2 = font.render("2. Play vs Player", True, WHITE)
    screen.blit(option2, (WIDTH // 2 - option2.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.flip()

# Configurar a posição inicial dos elementos do jogo
ball, ball_speed_x, ball_speed_y = reset_ball()
left_paddle = pygame.Rect(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
left_score, right_score = 0, 0

# Loop principal do jogo
running = True
clock = pygame.time.Clock()
menu = True
vs_ai = False

while running:
    if menu:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    vs_ai = True
                    menu = False
                elif event.key == pygame.K_2:
                    vs_ai = False
                    menu = False
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += PADDLE_SPEED

        if vs_ai:
            # Movimento da IA com atraso
            if right_paddle.centery < ball.centery and right_paddle.bottom < HEIGHT:
                right_paddle.y += AI_PADDLE_SPEED
            if right_paddle.centery > ball.centery and right_paddle.top > 0:
                right_paddle.y -= AI_PADDLE_SPEED
        else:
            if keys[pygame.K_UP] and right_paddle.top > 0:
                right_paddle.y -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
                right_paddle.y += PADDLE_SPEED

        # Movimento da bola
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Colisões com as paredes
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1
        if ball.left <= 0:
            right_score += 1
            ball, ball_speed_x, ball_speed_y = reset_ball()
        if ball.right >= WIDTH:
            left_score += 1
            ball, ball_speed_x, ball_speed_y = reset_ball()

        # Colisões com os paddles
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_speed_x *= -1

        # Desenhar a tela
        draw_screen(ball, left_paddle, right_paddle, left_score, right_score)

        # Verificar se alguém ganhou
        if left_score == WINNING_SCORE or right_score == WINNING_SCORE:
            winning_text = "Left Player Wins!" if left_score == WINNING_SCORE else "Right Player Wins!"
            font = pygame.font.Font(None, 74)
            text = font.render(winning_text, True, WHITE)
            screen.blit(text, (WIDTH // 4, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(3000)
            left_score, right_score = 0, 0
            ball, ball_speed_x, ball_speed_y = reset_ball()
            menu = True

    # Controlar a velocidade do jogo
    clock.tick(60)

pygame.quit()
