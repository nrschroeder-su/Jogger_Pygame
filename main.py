import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surface.get_rect(center = (600,100))
    screen.blit(score_surface,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            
            if obstacle_rect.bottom == 800:
                screen.blit(enemy_surface,obstacle_rect)
            else:
                 screen.blit(bat_surface,obstacle_rect)
            
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -200]
            
        return obstacle_list
    else: return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True
                
def player_animation():
    global player_surface, player_index
    
    if player_rect.bottom < 700:
        player_surface = player_walk_1
    else:
        player_index += 0.08
        if player_index >= len(player_walk): player_index = 0
        player_surface = player_walk[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((1200, 1000))
pygame.display.set_caption('Jogger')
clock = pygame.time.Clock()
test_font = pygame.font.Font('fonts/gameplayed.ttf', 60)
game_active = False
start_time = 0
score = 0
background_music = pygame.mixer.Sound('audio/ingame_music.mp3')
background_music.play(loops = -1)
background_music.set_volume(.15)

sky_surface = pygame.image.load('graphics/sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Toast
enemy_frame_1 = pygame.image.load('graphics/toast_1.png').convert_alpha()
enemy_frame_2 = pygame.image.load('graphics/toast_2.png').convert_alpha()
enemy_frame_1 = pygame.transform.rotozoom(enemy_frame_1,0,1.25)
enemy_frame_2 = pygame.transform.rotozoom(enemy_frame_2,0,1.25)
enemy_frames = [enemy_frame_1, enemy_frame_2]
enemy_frame_index = 0
enemy_surface = enemy_frames[enemy_frame_index]

# Bat
bat_frame_1 = pygame.image.load('graphics/bat_sprite_1.png').convert_alpha()
bat_frame_2 = pygame.image.load('graphics/bat_sprite_2.png').convert_alpha()
bat_frame_1 = pygame.transform.rotozoom(bat_frame_1,0,2.5)
bat_frame_2 = pygame.transform.rotozoom(bat_frame_2,0,2.5)
bat_frames = [bat_frame_1,bat_frame_2]
bat_frame_index = 0
bat_surface = bat_frames[bat_frame_index]

obstacle_rect_list = []

# Player
player_walk_1 =pygame.image.load('graphics/player/my_player2.png').convert_alpha()
player_walk_2 =pygame.image.load('graphics/player/my_player3.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0

player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (100,799))
player_gravity = 0

jump_sound = pygame.mixer.Sound('audio/game_jump2.mp3')
jump_sound.set_volume(0.35)

# Intro screen
player_stand = pygame.image.load('graphics/player/my_player2.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (600,500))

# Intro screen text
game_name = test_font.render('Jogger', False,'black')
game_name_rect = game_name.get_rect(center = (600,300))

game_message = test_font.render('Press Spacebar to Run', False, 'black')
game_message_rect = game_message.get_rect(center = (600,700))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

enemy_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_animation_timer, 500)

bat_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(bat_animation_timer, 200)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 800:
                    player_gravity = -20
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 800:
                    player_gravity = -24
                    jump_sound.play()
                
        else: 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
        if game_active:       
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(enemy_surface.get_rect(bottomright = (randint(1250,1450),800)))
                else:
                    obstacle_rect_list.append(bat_surface.get_rect(bottomright = (randint(1250,1450),640)))
                    
            if event.type == enemy_animation_timer:
                if enemy_frame_index == 0: enemy_frame_index = 1
                else: enemy_frame_index = 0
                enemy_surface = enemy_frames[enemy_frame_index]
                
            if event.type == bat_animation_timer:    
                if bat_frame_index == 0: bat_frame_index = 1
                else: bat_frame_index = 0
                bat_surface = bat_frames[bat_frame_index]
                    
    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,800))
        score = display_score()
        
        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 800: player_rect.bottom = 800
        player_animation()
        screen.blit(player_surface, player_rect)
        
        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        
        # Collision
        game_active = collisions(player_rect,obstacle_rect_list)
        
    else:
        screen.fill((94,128,160))
        screen.blit(player_stand, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (100,800)
        player_gravity = 0
        
        score_message = test_font.render(f'Your Score: {score}', False, 'black')
        score_message_rect = score_message.get_rect(center = (600,700))
        screen.blit(game_name,game_name_rect)
        
        if score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)
        
    pygame.display.update()
    clock.tick(60)