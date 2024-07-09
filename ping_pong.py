import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Screen setup
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Ping Pong')

# Font setup
font = pygame.font.Font(None, 74)
game_over_font = pygame.font.Font(None, 100)
button_font = pygame.font.Font(None, 50)

# Ball setup
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
ball_speed_x = 7
ball_speed_y = 7

# Paddle setup
paddle_width = 10
paddle_height = 100
player = pygame.Rect(screen_width - 20, screen_height / 2 - 50, paddle_width, paddle_height)
opponent = pygame.Rect(10, screen_height / 2 - 50, paddle_width, paddle_height)
paddle_speed = 7

# Score
player_score = 0
opponent_score = 0

# Game state
game_active = False
ready_rect = None
play_again_rect = None

def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, game_active

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

    if ball.left <= 0:
        player_score += 1
        game_active = False

    if ball.right >= screen_width:
        opponent_score += 1
        game_active = False

def player_animation():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= paddle_speed
    if keys[pygame.K_DOWN] and player.bottom < screen_height:
        player.y += paddle_speed

def opponent_animation():
    if opponent.top < ball.y:
        opponent.y += paddle_speed
    if opponent.bottom > ball.y:
        opponent.y -= paddle_speed

def display_score():
    player_text = font.render(str(player_score), True, white)
    screen.blit(player_text, (screen_width / 2 + 20, 10))

    opponent_text = font.render(str(opponent_score), True, white)
    screen.blit(opponent_text, (screen_width / 2 - 40, 10))

def display_game_over():
    game_over_text = game_over_font.render('GAME OVER', True, white)
    screen.blit(game_over_text, (screen_width / 4, screen_height / 3))

    final_score_text = font.render(f'Player: {player_score} Opponent: {opponent_score}', True, white)
    screen.blit(final_score_text, (screen_width / 4 + 30, screen_height / 2))

    play_again_text = button_font.render('Play Again', True, black, green)
    play_again_rect = play_again_text.get_rect(center=(screen_width / 2, screen_height / 1.5))
    screen.blit(play_again_text, play_again_rect)

    return play_again_rect

def display_ready_button():
    ready_text = button_font.render('Ready', True, black, green)
    ready_rect = ready_text.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.blit(ready_text, ready_rect)

    return ready_rect

def reset_game():
    global game_active, ball_speed_x, ball_speed_y
    ball.center = (screen_width / 2, screen_height / 2)
    ball_speed_x *= -1
    game_active = True

def main():
    global game_active, ready_rect, play_again_rect
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ready_rect and ready_rect.collidepoint(event.pos):
                    reset_game()
                if play_again_rect and play_again_rect.collidepoint(event.pos):
                    reset_game()

        screen.fill(black)
        if game_active:
            ball_animation()
            player_animation()
            opponent_animation()
            ready_rect = None
            play_again_rect = None
        else:
            play_again_rect = display_game_over()

        pygame.draw.rect(screen, white, player)
        pygame.draw.rect(screen, white, opponent)
        pygame.draw.ellipse(screen, white, ball)
        pygame.draw.aaline(screen, white, (screen_width / 2, 0), (screen_width / 2, screen_height))

        display_score()

        if not game_active and not play_again_rect:
            ready_rect = display_ready_button()

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
