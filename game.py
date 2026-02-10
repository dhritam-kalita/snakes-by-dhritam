import pygame
import random
import os
import time
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def save_path(filename):
    base = os.path.join(os.getenv("LOCALAPPDATA"), "SnakesByDhritam")
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, filename)


x = pygame.init()
pygame.mixer.init()

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
mm_bg = (255, 102, 204)

screen_width = 700
screen_height = 500
gameWindow = pygame.display.set_mode((screen_width, screen_height))

font = pygame.font.SysFont(None, 40)

clock = pygame.time.Clock()
pygame.display.set_caption("SnakesByDhritam")
pygame.display.update()

def write_text(text,color,x,y):
    text_formatted = font.render(text, True, color)
    gameWindow.blit(text_formatted, [x, y])

def draw_snake(window, color, lst, size):
    for x,y in lst:
        pygame.draw.rect(window, color, [x,y,size,size])

def game_credits():
    credits_img = pygame.image.load(
        resource_path(os.path.join('assets','images','credits.png'))
    ).convert_alpha()
    credits_img = pygame.transform.scale(credits_img, [screen_width, screen_height])

    temp = True
    while temp:
        gameWindow.blit(credits_img, [0, 0])
        pygame.display.update()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.key == pygame.K_ESCAPE:
                temp = False


def main_menu():

    gameWindow.fill(mm_bg)

    score_file = save_path("highscore.txt")
    with open(score_file, "r") as f:
        hiscore = f.read()


    pygame.mixer.music.load(
        resource_path(os.path.join('assets','music','main_menu.mp3'))
    )
    pygame.mixer.music.play(-1)

    loaded_img = pygame.image.load(
        resource_path(os.path.join('assets','images','main_menu.png'))
    ).convert_alpha()
    loaded_img = pygame.transform.scale(loaded_img,[screen_width,screen_height])

    gameWindow.blit(loaded_img, [0,0])
    gameWindow.blit(
        pygame.font.SysFont('Broadway', 30)
        .render(f"Highscore - {hiscore}",True, red),
        [20,0]
    )
    pygame.display.update()

    temp = True
    while temp:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    temp = False
                if event.key == pygame.K_SPACE:
                    game_credits()
                    gameWindow.blit(loaded_img, [0, 0])
                    gameWindow.blit(
                        pygame.font.SysFont('Broadway', 30)
                        .render(f"Highscore - {hiscore}", True, red),
                        [20, 0]
                    )
                    pygame.display.update()

    pygame.mixer.music.stop()
    pygame.mixer.music.unload()

def game_loop():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()

    score_file = save_path("highscore.txt")

    if not os.path.exists(score_file):
        with open(score_file, "w") as f:
            f.write("0")


    snake_x = random.randint(20, screen_width - 20)
    snake_y = random.randint(20, screen_height - 20)
    snake_size = 15
    food_size = snake_size * 1.2
    food_x = random.randint(20, screen_width - 20)
    food_y = random.randint(20, screen_height - 20)

    snake_len = 1
    len_lst = []
    score = 0
    fps = 30

    velocity_x = 0
    velocity_y = 0
    exit_game = False
    game_over = False

    with open(score_file, "r") as f:
        hiscore = int(f.read())


    main_menu()

    bg_img = pygame.image.load(
        resource_path(os.path.join('assets','images','background.png'))
    )
    bg_img = pygame.transform.scale(bg_img,[screen_width,screen_height])

    food_img = pygame.image.load(
        resource_path(os.path.join('assets','images','apple.png'))
    )
    food_img = pygame.transform.scale(food_img, [food_size, food_size])

    pygame.mixer.music.load(
        resource_path(os.path.join('assets','music','background.mp3'))
    )
    pygame.mixer.music.play(-1)

    point_up_sound = pygame.mixer.Sound(
        resource_path(os.path.join('assets','music','point_up.mp3'))
    )

    game_over_played = False
    while not exit_game:
        if game_over:
            if not game_over_played:
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()

                pygame.mixer.music.load(
                    resource_path(os.path.join('assets','music','game_over.mp3'))
                )
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play()
                time.sleep(3)

                pygame.mixer.music.unload()
                pygame.mixer.music.load(
                    resource_path(os.path.join('assets','music','game_over-later.mp3'))
                )
                pygame.mixer.music.set_volume(0.12)
                pygame.mixer.music.play(-1)

                game_over_played = True

            loaded_game_over_img = pygame.image.load(
                resource_path(os.path.join('assets','images','game_over.png'))
            ).convert_alpha()
            loaded_game_over_img = pygame.transform.scale(
                loaded_game_over_img,[screen_width,screen_height]
            )

            gameWindow.blit(loaded_game_over_img,[0,0])
            gameWindow.blit(
                pygame.font.SysFont('Broadway', 30).render(f"{score}", True, white),
                [200, 157]
            )
            gameWindow.blit(
                pygame.font.SysFont('Broadway', 30).render(f"{hiscore}", True, white),
                [520, 157]
            )

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return
                elif event.type == pygame.QUIT:
                    exit_game = True

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and not velocity_x < 0:
                        velocity_x = 10
                        velocity_y = 0
                    if event.key == pygame.K_LEFT and not velocity_x > 0:
                        velocity_x = -10
                        velocity_y = 0
                    if event.key == pygame.K_UP and not velocity_y > 0:
                        velocity_x = 0
                        velocity_y = -10
                    if event.key == pygame.K_DOWN and not velocity_y < 0:
                        velocity_x = 0
                        velocity_y = +10

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < abs(snake_size) and abs(snake_y - food_y) < abs(snake_size):
                point_up_sound.set_volume(0.2)
                point_up_sound.play()
                score += 10
                snake_len += 3
                food_x = random.randint(20, screen_width - 20)
                food_y = random.randint(20, screen_height - 20)

            if score > hiscore:
                hiscore = score
                with open(score_file, "w") as f:
                    f.write(str(hiscore))


            head = [snake_x, snake_y]
            len_lst.append(head)

            if len(len_lst) > snake_len:
                del len_lst[0]

            if head in len_lst[:-1]:
                game_over = True
            if snake_x < 0 or snake_x > screen_width - snake_size or snake_y < 0 or snake_y > screen_height - snake_size:
                game_over = True

            gameWindow.blit(bg_img,[0,0])
            write_text(f"High Score: {str(hiscore)}",red,200, 5)
            write_text(f"Score: {score}", red, 5,5)
            gameWindow.blit(food_img, [food_x,food_y])
            draw_snake(gameWindow, black, len_lst, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

if __name__ == "__main__":
    while True:
        game_loop()
