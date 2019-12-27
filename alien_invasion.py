import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


def run_game():
    # initialization and create a screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    # create a play button
    play_button = Button(screen, 'Play')

    # create a ship
    ship = Ship(ai_settings, screen)
    # create a group of bullets
    bullets = Group()
    # create a group of aliens
    aliens = Group()
    gf.create_fleet(ai_settings, screen, aliens, ship)

    # store game states info
    stats = GameStats(ai_settings)
    # score board
    sb = ScoreBoard(ai_settings, screen, stats)

    # start main loop
    while True:
        gf.check_events(ai_settings, screen, ship, bullets, aliens, stats, sb, play_button)

        # stop update items if game over
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, aliens, bullets, screen, ship, stats, sb)
            gf.update_aliens(ai_settings, stats, sb, screen, aliens, bullets, ship)

        gf.update_screen(ai_settings, screen, ship, bullets, aliens, stats, play_button, sb)


run_game()
