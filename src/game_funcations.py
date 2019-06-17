'''
Created on Jun 16, 2019  2:27:32 PM

@author: chenwei
'''
import sys
import pygame

from bullet import Bullet
from alien import Alien

def check_events(ai_settings, screen, ship, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        # 按下按键
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        # 离开按键
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ai_settings, screen, ship, bullets)
        
                
def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = True
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        ship.moving_bottom = True
    elif event.key == pygame.K_UP or event.key == pygame.K_w:
        ship.moving_top = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
        
def check_keyup_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = False
    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
        ship.moving_bottom = False
    elif event.key == pygame.K_UP or event.key == pygame.K_w:
        ship.moving_top = False
            
def update_screen(ai_settings, screen, ship, aliens, bullets):
    """更新屏幕上的图像并切换到新屏幕"""
    #每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面绘制所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # 让最近绘制的屏幕可见
    pygame.display.flip()
    
def update_bullets(aliens, bullets):
    bullets.update()
    # 删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
#         print(len(bullets))
    coliisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

def fire_bullet(ai_settings, screen, ship, bullets):
    # 创建一颗子弹，将其加入到编组bullets中
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)
        
def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行可以容纳多少个外星人
    # 外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, alien.rect.height, ship.rect.height)
    # 创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # 创建一个外星人并加入当前行
            create_alien(ai_settings, screen, aliens, alien_number, row_number)
        
def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可以容纳多少外星人"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x/(2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并加入当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    
    
def get_number_rows(ai_settings, alien_height, ship_height):
    """计算可以容纳多少行外星人"""
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(available_space_y /(2 * alien_height))
    return number_rows

def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应措施"""
    for alien in aliens:
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
    
def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移并改变方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    
def update_aliens(ai_settings, aliens):
    """更新外星人群中外星人的位置"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    
    
    

