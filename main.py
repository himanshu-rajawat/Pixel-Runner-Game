import pygame
from pygame import mixer
from sys import exit
from random import randint

def display_score():
    current_score = int((pygame.time.get_ticks()-start_time)/1000)
    score_surface = test_font.render(f'Score: {current_score}',False,(64,64,64))
    score_rect = score_surface.get_rect(center=(400,50))
    screen.blit(score_surface,score_rect)
    return current_score

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x >-100]
        return obstacle_list
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                mixer.music.pause()
                is_paused = True
                game_over_sound.play()
                return False
    return True

def player_animantion():
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >=2: player_index = 0
        player_surf = player_walk[int(player_index)]

pygame.init()
mixer.init()

# Loading the song
mixer.music.load("audio/music.wav")
jump_sound = mixer.Sound("audio/jump.wav")
game_over_sound = mixer.Sound("audio/game-over.wav")

# Setting the volume
mixer.music.set_volume(0.5)

# Start playing the song
mixer.music.play()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('pygame_project')
clock = pygame.time.Clock()
Score = 0
sky_surface = pygame.image.load('graphics/Sky.png')
ground_surface = pygame.image.load('graphics/ground.png')

obstacles_rect_list = []
snail_surface1 = pygame.image.load('graphics/snail/snail1.png')
snail_surface2 = pygame.image.load('graphics/snail/snail1.png')
snail_frames = [snail_surface1,snail_surface2]
snail_index = 0
snail_surface = snail_frames[snail_index]
player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index= 0
player_surf = player_walk[player_index]
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
fly_surface1 = pygame.image.load('graphics/Fly/fly1.png').convert_alpha()
fly_surface2 = pygame.image.load('graphics/Fly/fly2.png').convert_alpha()
fly_index = 0
fly_frames=[fly_surface1,fly_surface2]
fly_surface = fly_frames[fly_index]
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
test_font = pygame.font.Font(None,50)
player_stand_scaled = pygame.transform.rotozoom(player_stand,0,2)
# score_surface = test_font.render('My game',False,(64,64,64))
# score_rect = score_surface.get_rect(center=(400,50))
player_rect = player_surf.get_rect(bottomleft=(100,300))
is_paused = False
player_stand_rect = player_stand_scaled.get_rect(center = (400,200))
player_gravity = 0
jump_count = 0
game_active = False
start_time = 0
game_name = test_font.render('Pixel Runner',False,(111,196,169))
game_name_rect = game_name.get_rect(center=(400,80))

game_message = test_font.render('Press Space to run',False,(111,196,169))
game_message_rect = game_message.get_rect(center=(400,330))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,300)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,300)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_rect.bottom > 200 and jump_count <1:
                        jump_sound.play()
                        player_gravity = -20
                        jump_count+=1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_gravity=-20
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacles_rect_list.append(snail_surface.get_rect(bottomright = (randint(900,1100),300)))
                else:
                    obstacles_rect_list.append(fly_surface.get_rect(bottomright = (randint(900,1100),210)))
            if event.type == snail_animation_timer:
                if snail_index ==0: snail_index=1
                else: snail_index = 0
                snail_surface = snail_frames[snail_index]
            if event.type == fly_animation_timer:
                if fly_index ==0: fly_index=1
                else: fly_index = 0
                fly_surface = fly_frames[fly_index]
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()
    if game_active:
        if jump_count>0 and player_rect.bottom == 300:
            jump_count=0
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        # screen.blit(snail_surface,snail_rect)
        player_rect.right += 1
        if player_rect.left>800:
            player_rect.right = 0
        Score = display_score()
        #player_rect
        player_gravity+=1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        player_animantion()
        screen.blit(player_surf,player_rect)

        obstacle_list = obstacle_movement(obstacles_rect_list)

        #collision
        game_active = collisions(player_rect,obstacles_rect_list)
        # if player_rect.colliderect(snail_rect):
        #     game_active=False
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand_scaled,player_stand_rect)
        score_message = test_font.render(f'Your Score: {Score}',False,(111,196,169))
        score_message_rect = score_message.get_rect(center=(400,330))
        screen.blit(game_name,game_name_rect)
        obstacles_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0
        if Score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_message,score_message_rect)
        mixer.music.unpause()
    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_pos):
    #     print(pygame.mouse.get_pressed())
    pygame.display.update()
    clock.tick(60)
