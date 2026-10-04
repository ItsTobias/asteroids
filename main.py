import sys
import pygame
from constants import *
from logger import *
from player import Player
from asteroid import Asteroid
from astroidfield import AsteroidField
from shot import Shot

def reset_game(updatable, drawable, asteroids, shots):
    updatable.empty()
    drawable.empty()
    asteroids.empty()
    shots.empty()

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    return player, asteroid_field

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

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
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

        log_state()

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

                        player, asteroid_field = reset_game(
                            updatable,
                            drawable,
                            asteroids,
                            shots
                        )
                                            

        if game_over == False:
            updatable.update(dt)

            for asteroid in asteroids:
                if player.collision_with(asteroid):
                    log_event("player_hit")

                    print("Game over!")
                    print(str(int(score)))

                    if score > highscore:
                        save_highscore(score)
                        highscore = score

                    game_over = True
            
            for asteroid in asteroids:
                for shot in shots:
                    if shot.collision_with(asteroid):
                        log_event("asteroid_shot")
                        shot.kill()
                        if asteroid.radius == ASTEROID_RARE_RADIUS:
                            score += ASTEROID_RARE_POINTS
                        else:
                            score += int(ASTEROID_MIN_RADIUS / asteroid.radius * 10)
                        asteroid.split()
                        break
            
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

                for object in drawable:
                    object.draw(screen)

            pygame.display.flip()


if __name__ == "__main__":
    main()

    
    
    
    
    
    
    
    
    
    
    
    
    # game_over = False

    # while True:
    #     dt = clock.tick(FPS) / 1000
        
    #     log_state()

    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             return

    #     if game_over == False:
            
    #         updatable.update(dt)
            
    #         screen.blit(background, (0, 0))
    #         screen.blit(dark_overlay, (0, 0))

    #         score_text = font.render(f"Score: {int(score)}", True, COLOR_SCORE)
    #         screen.blit(score_text, (10, 10))

    #         highscore_text = font.render(f"Highscore: {int(highscore)}", True, COLOR_SCORE)
    #         screen.blit(highscore_text, (10, 45))
            
    #         for object in drawable:
    #             object.draw(screen)

    #         for asteroid in asteroids:
    #             if player.collision_with(asteroid):
    #                 while True:
    #                     log_event("player_hit")
    #                     print("Game over!")
    #                     mouse_x, mouse_y = pygame.mouse.get_pos()
    #                     print(mouse_x, mouse_y)
    #                     print(str(int(score)))
    #                     if score > highscore:
    #                         save_highscore(score)

    #                     died_text = font_large.render(f"You died with a score of: {score}", True, COLOR_DIED_TEXT)
    #                     died_text_rect = died_text.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    #                     screen.blit(death_screen, (0, 0))
    #                     screen.blit(died_text, died_text_rect)
    #                     pygame.display.flip()

                        
                        

    #             for shot in shots:    
    #                 if shot.collision_with(asteroid):
    #                     log_event("asteroid_shot")
    #                     shot.kill()
    #                     if asteroid.radius == ASTEROID_RARE_RADIUS:
    #                         score += ASTEROID_RARE_POINTS
    #                     else:
    #                         score += int(ASTEROID_MIN_RADIUS / asteroid.radius * 10)
    #                     asteroid.split()


    #     pygame.display.flip()

# if __name__ == "__main__":
#     main()