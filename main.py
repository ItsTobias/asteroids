import sys
import pygame
from constants import *
# from logger import *
from player import Player
from asteroid import Asteroid
from astroidfield import AsteroidField
from shot import Shot
from supershot import Supershot
from itertools import chain

def reset_game(updatable, drawable, asteroids, shots, supershots):
    updatable.empty()
    drawable.empty()
    asteroids.empty()
    shots.empty()
    supershots.empty()

    fase = 1

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, asteroids)
    asteroid_field = AsteroidField(fase)

    return player, asteroid_field, fase

def load_highscore():
    with open("highscore.txt", "r") as file:
        return int(file.read())

def save_highscore(highscore):
    with open("highscore.txt", "w") as file:
        file.write(str(highscore))

def main():
    pygame.init()

    clock = pygame.time.Clock()
    
    dt = 0.0
    score = 0
    fase = 1

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    supershots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    Supershot.containers = (supershots, updatable, drawable)
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, asteroids)
    asteroid_field = AsteroidField(fase)
    background = pygame.image.load(ACHTERGROND)
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    death_screen = pygame.image.load(DEATH_SCREEN)
    death_screen = pygame.transform.scale(death_screen, (SCREEN_WIDTH, SCREEN_HEIGHT))
    dark_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    dark_overlay.set_alpha(int((100 - BRIGHTNESS_BACKGROUND) * 255 / 99))
    dark_overlay.fill((0, 0, 0))
    font = pygame.font.SysFont("arial", FONT_SIZE)
    font_large = pygame.font.SysFont("arial", 100)
    highscore = load_highscore()
    quit_button = pygame.Rect(248, 549, 786, 89)
    restart_button = pygame.Rect(248, 442, 786, 88)
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    game_over = False

    while True:
        dt = clock.tick(FPS) / 1000

        # log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    if quit_button.collidepoint(event.pos):
                        sys.exit()
                    if restart_button.collidepoint(event.pos): 
                        score = 0
                        game_over = False

                        player, asteroid_field, fase = reset_game(
                            updatable,
                            drawable,
                            asteroids,
                            shots,
                            supershots
                        )
                                            

        if game_over == False:
            updatable.update(dt)
            
            for asteroid in asteroids:
                if player.collision_with(asteroid):
                    # log_event("player_hit")

                    print("Game over!")
                    print(str(int(score)))

                    if score > highscore:
                        save_highscore(score)
                        highscore = score

                    game_over = True
            
            for asteroid in asteroids:
                for shot in chain(shots, supershots):
                    if shot.collision_with(asteroid):
                        # log_event("asteroid_shot")
                        if shot in shots:
                            shot.kill()
                        if asteroid.radius == ASTEROID_RARE_RADIUS:
                            score += ASTEROID_RARE_POINTS
                        else:
                            if asteroid.radius == ASTEROID_MIN_RADIUS:
                                score += POINTS_SMALL_ASTEROID
                            elif asteroid.radius == ASTEROID_MIN_RADIUS * 2:
                                score += POINTS_MEDIUM_ASTEROID
                            elif asteroid.radius == ASTEROID_MIN_RADIUS * 3:
                                score += POINTS_LARGE_ASTEROID
                        asteroid.split()
                        break
                    while score >= fase * SCORE_FOR_FASE_UP:
                        fase += 1
                        asteroid_field.fase = fase

            
            if game_over:
                screen.blit(death_screen, (0, 0))

                died_text = font.render(str(score), True, COLOR_DIED_TEXT)
        

                screen.blit(died_text, (700, 264))


            else:
                screen.blit(background, (0, 0))
                screen.blit(dark_overlay, (0, 0))

                score_text = font.render(f"Score: {int(score)}", True, COLOR_SCORE)
                screen.blit(score_text, (10, 10))

                highscore_text = font.render(f"Highscore: {int(highscore)}", True, COLOR_SCORE)
                screen.blit(highscore_text, (10, 45))

                fase_text = font.render(f"Fase: {fase}", True, COLOR_FASE)
                screen.blit(fase_text, (10, 80))

                fps_text = font.render(f"FPS: {clock.get_fps():.0f}", True, COLOR_FPS)
                screen.blit(fps_text, (SCREEN_WIDTH - 150, 10))



                for object in drawable:
                    object.draw(screen)

            pygame.display.flip()


if __name__ == "__main__":
    main()