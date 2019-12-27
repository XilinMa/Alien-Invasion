import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """respond keydown"""
    # move right
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    # move left
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    # fire
    elif event.key == pygame.K_SPACE:
        fire_bullet(bullets, ai_settings, screen, ship)
    # end game by Q
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """respond keyup"""
    # stop move right
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    # stop move left
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, ship, bullets, aliens, stats, sb, play_button):
    # monitor keyboard and mouse event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        # move continuously
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
            # print(event.key)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, ship, stats, sb, play_button, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, ship, stats, sb, play_button, aliens, bullets, mouse_x, mouse_y):
    """start new game when pressing play button and game not active"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # reset game speed
        ai_settings.initialize_dynamic_settings()

        # hide mouse
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        # update score, level and ships rects
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # empty aliens and bullets
        aliens.empty()
        bullets.empty()

        # create new alien fleet and center ship
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()


def fire_bullet(bullets, ai_settings, screen, ship):
    # add a new bullet to group if bullets are not enough
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """calculate numbers per line"""
    available_space_x = ai_settings.screen_width - alien_width * 2
    number_alien_x = int(available_space_x / (alien_width * 2))
    return number_alien_x


def get_number_aliens_rows(ai_settings, alien_height, ship_height):
    """calculate numbers per column"""
    available_space_y = ai_settings.screen_height - alien_height * 3 - ship_height
    number_alien_y = int(available_space_y / (alien_height * 2))
    return number_alien_y


def create_alien(ai_settings, screen, alien_number, aliens, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, aliens, ship):
    """create aliens group"""
    # get numbers per line
    alien = Alien(ai_settings, screen)
    # alien_width = alien.rect.width
    number_alien_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_aliens_rows(ai_settings, alien.rect.height, ship.rect.height)

    # create aliens on several lines
    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            create_alien(ai_settings, screen, alien_number, aliens, row_number)


def update_screen(ai_settings, screen, ship, bullets, aliens, stats, play_button, sb):
    # repaint screen
    screen.fill(ai_settings.bg_color)
    # # display all bullets
    # for bullet in bullets.sprites():
    #     bullet.draw_bullet()
    # draw ship
    ship.blitme()
    # draw aliens
    aliens.draw(screen)

    # show score
    sb.show_score()

    # if not active, draw play button
    if not stats.game_active:
        play_button.draw_button()
    # display all bullets only if game begins
    else:
        for bullet in bullets.sprites():
            bullet.draw_bullet()

    # display latest screen
    pygame.display.flip()


def update_bullets(ai_settings, aliens, bullets, screen, ship, stats, sb):
    bullets.update()

    # delete redundant bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collision(ai_settings, screen, ship, bullets, aliens, stats, sb)


def check_bullet_alien_collision(ai_settings, screen, ship, bullets, aliens, stats, sb):
    """respond bullets and aliens collision"""
    # if collide delete both
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for alien in collisions.values():
            stats.score += ai_settings.alien_points * len(alien)
            sb.prep_score()

        check_high_score(stats, sb)

    # if all aliens die
    if len(aliens) == 0:
        # clear bullets
        bullets.empty()

        # increase speed
        ai_settings.increase_speed()

        # increase level
        stats.level += 1
        sb.prep_level()

        # create new aliens
        create_fleet(ai_settings, screen, aliens, ship)


def check_high_score(stats, sb):
    """update highest score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            # move downward and change direction
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """move downward and change direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, stats, sb, screen, aliens, bullets, ship):
    """check aliens edges and update aliens location"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # check aliens and ship collision
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, aliens, bullets, ship)

    # check aliens reach bottom
    check_aliens_bottom(ai_settings, stats, sb, screen, aliens, bullets, ship)


def ship_hit(ai_settings, stats, sb, screen, aliens, bullets, ship):
    """after ship and aliens collide"""
    if stats.ships_left > 0:
        # ship number -1
        stats.ships_left -= 1

        sb.prep_ships()

        # empty bullets and aliens
        aliens.empty()
        bullets.empty()

        # create new alien fleet and center ship
        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()

        # pause for a second
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, sb, screen, aliens, bullets, ship):
    """if aliens reach bottom then reset"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, sb, screen, aliens, bullets, ship)
            break