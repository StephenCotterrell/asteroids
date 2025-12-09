import sys
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroidfield import AsteroidField
from asteroid import Asteroid
from shot import Shot


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    player = Player(
        SCREEN_WIDTH / 2,
        SCREEN_HEIGHT / 2,
    )

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    asteroidfield = AsteroidField()

    Shot.containers = (shots, updatable, drawable)

    game_clock = pygame.time.Clock()
    dt = 0

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        dt = game_clock.tick(60) / 1000
        screen.fill("black")
        updatable.update(dt)
        for itrasteroid in asteroids:
            if itrasteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        for itrasteroid in asteroids:
            for shot in shots:
                if shot.collides_with(itrasteroid):
                    log_event("asteroid_shot")
                    shot.kill()
                    itrasteroid.split()

        for thing in drawable:
            thing.draw(screen)
        pygame.display.flip()
        log_state()


if __name__ == "__main__":
    main()
