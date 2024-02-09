import pygame, sys, random
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()


#Tạo biến cho trò chơi
screen = pygame.display.set_mode((432,768))
clock = pygame.time.Clock() #cài FPS
game_font = pygame.font.Font('04B_19.TTF', 40)
gravity = 0.25  #Trọng lực
brid_movement = 0
game_active = True
score = 0
hight_score = 0

#Chèn back ground
bg = pygame.image.load('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)
#Chèn nền dưới
floor = pygame.image.load('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
#Tạo chim
brid_down = pygame.transform.scale2x(pygame.image.load('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/assets/yellowbird-downflap.png')).convert_alpha()
brid_mid = pygame.transform.scale2x(pygame.image.load('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/assets/yellowbird-midflap.png')).convert_alpha()
brid_up = pygame.transform.scale2x(pygame.image.load('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/assets/yellowbird-upflap.png')).convert_alpha()
brid_list = [brid_down, brid_mid, brid_up]  #0 1 2
brid_index = 0
brid = brid_list[brid_index]
# brid = pygame.image.load('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/assets/yellowbird-midflap.png').convert_alpha()
# brid = pygame.transform.scale2x(brid)   #cho con chim to x2
brid_rect = brid.get_rect(center = (100, 384))  #Tạo khung bao quanh con chim
#tạo timer cho bird
bridflap = pygame.USEREVENT+1
pygame.time.set_timer(bridflap, 200)

#Tạo ống
pipe_surface = pygame.image.load('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/assets\pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
#Tạo timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)  #1,2s sẽ tạo 1 ống mới
pipe_hight = [200,300,400]
#Tạo màn hình kết thúc
game_over_surface = pygame.transform.scale2x(pygame.image.load('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/assets/message.png')).convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(216, 384))
#Chèn âm thanh
flap_sound = pygame.mixer.Sound('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('C:/Users/Admin/PycharmProjects/pythonProject/FileGame/sound/sfx_point.wav')
score_sound_coutdown = 100


#Tạo hàm cho trò chơi
def draw_floor():
    screen.blit(floor,(floor_x_pos, 650))
    screen.blit(floor,(floor_x_pos+432, 650))

def create_pipe():
    random_pipe_pos = random.choice(pipe_hight)
    botton_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))    #tạo ống
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos-650))
    return botton_pipe, top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5   #Tạo ống di chuyển về bên trái
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom>=600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False,True) #Lật ống bên trên
            screen.blit(flip_pipe, pipe)

def check_colilísion(pipes):
    for pipe in pipes:
        if brid_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if brid_rect.top<=-75 or brid_rect.bottom>=650:
        return False
    return True

def rotate_brid(brid1):
    new_bird = pygame.transform.rotozoom(brid1, -brid_movement*3, 1)
    return new_bird

def bird_animation():
    new_brid = brid_list[brid_index]
    new_brid_rect = new_brid.get_rect(center=(100, brid_rect.centery))
    return new_brid, new_brid_rect

def score_display(game_state):
    if game_state=='main game':
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)
    if game_state=='game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255,255,255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)

        hight_score_surface = game_font.render(f'Hight Score: {int(hight_score)}', True, (255,255,255))
        hight_score_rect = hight_score_surface.get_rect(center=(216, 630))
        screen.blit(hight_score_surface, hight_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return  high_score


while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                brid_movement=0
                brid_movement=-11   #chọn nút space chim sẽ bay lên 11 ô
                flap_sound.play()

            if event.key == pygame.K_SPACE and game_active==False:
                game_active=True
                pipe_list.clear()
                brid_rect.center= (100, 384)
                brid_movement=0
                score = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())

        if event.type==bridflap:
            if brid_index<2:
                brid_index+=1
            else:
                brid_index = 0
            brid, brid_rect= bird_animation()

    screen.blit(bg,(0, 0))
    if game_active:
        #Chim
        brid_movement +=gravity
        rotated_brid = rotate_brid(brid)
        screen.blit(rotated_brid,brid_rect)
        brid_rect.centery += brid_movement    #con chim và hình chữ nhật di chuyển xuống dưới
        game_active = check_colilísion(pipe_list)
        #Óng
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score+=0.01
        score_display('main game')
        score_sound_coutdown-=1
        if score_sound_coutdown<=0:
            score_sound.play()
            score_sound_coutdown=100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, hight_score)
        score_display(("game_over"))
    #Sàn
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos =0
    floor_x_pos -=1
    pygame.display.update()
    clock.tick(100)     #cài FPS


