import pygame
import os
import time
import random
from enemy import Enemy
from pokemon import Pokemon
from projectile import Projectile
from boss import Boss
clock = pygame.time.Clock()

Screen_x = 800
Screen_y = 600
pygame.init()
pygame.mixer.init()
# C:\Users\KelvinThePig\OneDrive\Máy tính\Game_ap_cs\pokemonChoosing_img
Title_Font = pygame.font.Font("font.ttf", 45)
gameStart_font = pygame.font.Font("font.ttf", 25)
Dicitonary_font = pygame.font.Font("font.ttf", 25)    
GameOver_font = pygame.font.Font("font.ttf", 50)
Replay_font =  pygame.font.Font("font.ttf", 30)
Choosing_font = pygame.font.Font("font.ttf", 40)
outline = Choosing_font.render("Choose your Pokemon", True, (255, 255, 255))  # viền đen
Score_font = pygame.font.Font("font.ttf",25)
Boss_hp_font = pygame.font.Font("font.ttf",20)
# sound effect
jumping_sound = pygame.mixer.Sound(os.path.join("sound_effect","jump_sound.wav"))
gameover_sound = pygame.mixer.Sound(os.path.join("sound_effect","gameover.wav"))
dying_sound = pygame.mixer.Sound(os.path.join("sound_effect","dying.wav"))
background1 = pygame.image.load(os.path.join("background","image1.png"))
background1 = pygame.transform.scale(background1,(Screen_x,Screen_y))
background2 = pygame.image.load(os.path.join("background","image2.png"))
background2 = pygame.transform.scale(background2,(Screen_x,Screen_y))
bossroom = pygame.image.load(os.path.join("bossRoom","bossroom.jpg"))
bossroom = pygame.transform.scale(bossroom,(Screen_x,Screen_y))
option1 = pygame.image.load(os.path.join("pokemonChoosing_img","charmander.png"))

option1 = pygame.transform.scale(option1,(100,100))
option1_rect = option1.get_rect()
option1_rect.topleft = (180,350)
option2 = pygame.image.load(os.path.join("pokemonChoosing_img","pikachu.png"))
option2 = pygame.transform.scale(option2,(100,100))
option2_rect = option2.get_rect()  # Fix: Use option2's rect
option2_rect.topleft = (option1_rect.x+200,350)
option3 = pygame.image.load(os.path.join("pokemonChoosing_img","trecko.png"))
option3 = pygame.transform.scale(option3,(100,100))
option3_rect = option3.get_rect()  # Fix: Use option3's rect
option3_rect.topleft = (option2_rect.x+200,350)
pygame.display.set_caption("POKEMON RUN")
screen = pygame.display.set_mode((Screen_x, Screen_y))
screen.fill((0, 0, 0))
loading_text = GameOver_font.render("Loading...", True, (255, 255, 255))
screen.blit(loading_text, (Screen_x//2 - loading_text.get_width()//2, Screen_y//2))
pygame.display.update()
selected = ""
# images
startTime = 0;
pikachu_running = []
charmander_running = []
trecko_running = []
enemy_image = []
pikachu_running_flip = []
charmander_running_flip = []
trecko_running_flip = []
enemy_image_flip = []
background_image = []
boss_image = []
boss_image_flip = []
spawn_rate = 2000
# load animation
def load_animation(folder_path,x,y):
    background_images = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".gif"):  
            path = os.path.join(folder_path, filename)
            image = pygame.image.load(path).convert_alpha()
            scaled = pygame.transform.scale(image, (x, y))
            background_images.append(scaled)
    return background_images

def load_flipped_animation(folder_path,x,y):
    background_image = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".gif"): 
            path = os.path.join(folder_path, filename)
            image = pygame.image.load(path).convert_alpha()
            flipped = pygame.transform.flip(image, True, False)
            scaled = pygame.transform.scale(flipped, (x, y))
            background_image.append(scaled)
    return background_image
# boss image
# idle

background_image = load_animation("background_img",800,600)
enemy_image = load_animation("enemy_img",80,80)
pikachu_running = load_animation("pikachu_frame",100,100)
charmander_running = load_animation("charmander_frame",150,150)
trecko_running = load_animation("trecko_frame",150,150)
# flip image
enemy_image_flip = load_flipped_animation("enemy_img",80,80)
pikachu_running_flip = load_flipped_animation("pikachu_frame",100,100)
charmander_running_flip = load_flipped_animation("charmander_frame",150,150)
trecko_running_flip = load_flipped_animation("trecko_frame",150,150)
boss_size_x = 500
boss_size_y = 300
boss_hp = 100
boss_max_hp = 100
# boss idle
boss_idle = load_animation("boss_img/boss_idle",boss_size_x,boss_size_y)
boss_flipped_idle = load_flipped_animation("boss_img/boss_idle",boss_size_x,boss_size_y)
# boss move
boss_move = load_animation("boss_img/boss_move",boss_size_x,boss_size_y)
boss_flipped_move = load_flipped_animation("boss_img/boss_move",boss_size_x,boss_size_y)
# boss swing
boss_swing = load_animation("boss_img/boss_swing",boss_size_x,boss_size_y)
boss_flipped_swing = load_flipped_animation("boss_img/boss_swing",boss_size_x,boss_size_y)
# boss attack 1
boss_attack1 = load_animation("boss_img/boss_attack1",boss_size_x,boss_size_y)
boss_flipped_attack1 = load_flipped_animation("boss_img/boss_attack1",boss_size_x,boss_size_y)
# boss attack 2
boss_attack2 = load_animation("boss_img/boss_attack2",boss_size_x,boss_size_y)
boss_flipped_attack2 = load_flipped_animation("boss_img/boss_attack2",boss_size_x,boss_size_y)
# boss regeneration
boss_regeneration = load_animation("boss_img/boss_buff",boss_size_x,boss_size_y)
boss_flipped_regeneration = load_flipped_animation("boss_img/boss_buff",boss_size_x,boss_size_y)
# boss death
boss_death = load_animation("boss_img/boss_death",boss_size_x,boss_size_y)
boss_flipped_death = load_flipped_animation("boss_img/boss_death",boss_size_x,boss_size_y)

boss_attack_right = {
    1 : boss_attack1,
    2 : boss_attack2,
    3 : boss_swing
}
boss_attack_left = {
    1 : boss_flipped_attack1,
    2 : boss_flipped_attack2,
    3 : boss_flipped_swing
}
BUTTON_COLOR = (255, 165, 0)
BUTTON_BORDER_COLOR = None
player = Pokemon(pikachu_running,80,425)
boss = Boss(boss_move,True,False,True,800,270,boss_hp,boss_max_hp)
boss_rect = boss.images[0].get_rect(topleft=(boss.x-boss.images[0].get_width(), boss.y))

highest_score = 0

speed = 20
jump_speed = -40  
gravity = 4   
Score = 0
last_slash_time = 0
boss_cooldown = 2000 
last_boss_attack_time = 0  

y_velocity = 0  
Projectile_speed = 30
enemy_speed = 5
# game status 
isJump = False
start = False
GameOver = False
Dictionary = True
# initiate object
  

cur_background = background1

character = {
    "charmander" : charmander_running,
    "pikachu" : pikachu_running,
    "trecko" : trecko_running
}
character_flip = {
    "charmander" : charmander_running_flip,
    "pikachu" : pikachu_running_flip,
    "trecko" : trecko_running_flip
}
slash_color = {
    "charmander" : pygame.image.load(os.path.join("slash_skill","red_slash.png")).convert_alpha(),
    "pikachu" : pygame.image.load(os.path.join("slash_skill","yellow_slash.png")).convert_alpha(),
    "trecko" : pygame.image.load(os.path.join("slash_skill","green_slash.png")).convert_alpha()
}
slash_color_flip = {
    "charmander": pygame.transform.flip(pygame.image.load(os.path.join("slash_skill", "red_slash.png")).convert_alpha(), True, False),
    "pikachu": pygame.transform.flip(pygame.image.load(os.path.join("slash_skill", "yellow_slash.png")).convert_alpha(), True, False),
    "trecko": pygame.transform.flip(pygame.image.load(os.path.join("slash_skill", "green_slash.png")).convert_alpha(), True, False)
}
player_base = player.bottom


running = True
def render_gradient_text(text, font, start_color, end_color):
    # Render text in white to get the alpha channel
    text_surface = font.render(text, True, (255, 255, 255))
    width, height = text_surface.get_size()
    gradient_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    for y in range(height):
        
        ratio = y / height
        r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
        g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
        b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
        pygame.draw.line(gradient_surface, (r, g, b), (0, y), (width, y))


    text_surface.set_colorkey((0, 0, 0))
    gradient_surface.blit(text_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return gradient_surface

# draw boss hp
def draw_hp_bar(surface, x, y, current_hp, max_hp,width = 400, height = 30,name = "???"):
    hp_ratio = current_hp / max_hp
    current_bar_length = int(hp_ratio * width)
    Boss_hp_text = Boss_hp_font.render(name, True, (255, 255, 255))
    Boss_hp_rect = Boss_hp_text.get_rect()
    Boss_hp_rect.center = (Screen_x // 2 , y + 50)  # Canh giữa, nằm trên thanh máu
    Boss_current_hp_text = Boss_hp_font.render(f"{current_hp}/{max_hp}", True, (255, 255, 255))
    Boss_current_hp_rect = Boss_current_hp_text.get_rect()
    Boss_current_hp_rect.center = (Screen_x // 2, y + 15)

    # Màu sắc (RGB)
    COPPER = (184, 115, 51)  # màu đồng
    NOT_RED = (74, 29, 29)
    RED = (255,0,0)

    # Vẽ viền (khung ngoài)
    pygame.draw.rect(surface, COPPER, (Screen_x//2 - 200, y - 2, width, height), border_radius=4)  # khung copper viền 2px
    
    # Vẽ nền (màu đỏ)
    pygame.draw.rect(surface, NOT_RED, (Screen_x//2 - 200, y, width, height), border_radius=3)

    # Vẽ phần máu còn lại (màu xanh)
    pygame.draw.rect(surface, RED, (Screen_x//2-200, y, current_bar_length, height-4), border_radius=3)
    screen.blit(Boss_hp_text, Boss_hp_rect)
    screen.blit(Boss_current_hp_text, Boss_current_hp_rect)


# fade in 
def fade_in(screen, bg_after, duration=1000):
    fade = pygame.Surface(screen.get_size())
    fade.fill((0, 0, 0))
    

    start = pygame.time.get_ticks()
    while True:
        now = pygame.time.get_ticks()
        elapsed = now - start
        alpha = max(0, 255 - int((elapsed / duration) * 255))
        fade.set_alpha(alpha)

        screen.blit(bg_after, (0, 0))
        screen.blit(fade, (0, 0))
        pygame.display.update()
        clock.tick(60)

        if elapsed >= duration:
            isDone = True
            break
# draw dictionary
def draw_dictionary_window():
    screen.blit(background2, (0, 0))
    btn_option_rects = [
    option1_rect.inflate(10, 10),
    option2_rect.inflate(10, 10),
    option3_rect.inflate(10, 10)
]

    btn_options = [option1, option2, option3]
    color = [0,255,255]
    border_colors = [color] * 3


    mouse_pos = pygame.mouse.get_pos()
    x = Dictionary_rect.centerx - Dictionary_text.get_width() // 2 - 175
    y = Dictionary_rect.centery - Dictionary_text.get_height() // 2 - 100

    # Vẽ nền và viền chữ "Choosing"
    if isDone:
            screen.blit(background2, (0, 0))
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                if Dictionary:
                    screen.blit(outline, (x + dx, y + dy))
            screen.blit(Choosing_text, (x, y))

    # Vẽ các lựa chọn
    if isDone:
        for i in range(3):
            screen.blit(btn_options[i], (btn_option_rects[i].x, btn_option_rects[i].y))
            if btn_option_rects[i].collidepoint(mouse_pos) and border_colors[i] and Dictionary:
                pygame.draw.rect(screen, border_colors[i], btn_option_rects[i], 3, border_radius=8)

pygame.display.update()
isFinish = True
skill_index = 0
skill_start_time = pygame.time.get_ticks()
# draw starting window
def draw_start_window(button_rect, button_dictionary_rect):
    screen.blit(Title, (Screen_x // 2 - Title.get_width() // 2 + 20, Screen_y // 2 - 150))
    screen.blit(startGame_text, (button_rect.centerx - startGame_text.get_width() // 2, button_rect.centery - startGame_text.get_height() // 2))
    screen.blit(Dictionary_text, (button_dictionary_rect.centerx - Dictionary_text.get_width() // 2, button_dictionary_rect.centery - Dictionary_text.get_height() // 2))
# draw game over window
def draw_game_over_window(GameOver_rect):
    if cur_background == bossroom:
        replay = replay_boss_text
        gameover = Gameover_boss_text
    else:
        replay = replay_text
        gameover = GameOver_text
    screen.blit(cur_background, (0, 0))
    screen.blit(gameover, (GameOver_rect.centerx - GameOver_text.get_width() // 2, GameOver_rect.centery - GameOver_text.get_height() // 2))
    screen.blit(replay, (replay_rect.centerx - replay_text.get_width() // 2, replay_rect.centery - replay_text.get_height() // 2))
# drawing 
skill = 0 
def draw_window():
    global skill
    global start
    global GameOver
    global Dictionary
    global isFinish
    global skill_index
    global skill_start_time
    global last_boss_attack_time
    global cur_background
    frame_delay = 100  # hiển thị mỗi frame trong 50ms (~20 FPS)
    frame_index = (pygame.time.get_ticks() // frame_delay) % len(background_image)
    screen.blit(background1, (0, 0))
    if start:
        screen.blit(background1, (0, 0)) 
        if Score >= 500 and not GameOver and boss.images != boss_death:
            cur_background = bossroom
           
            screen.blit(bossroom, (0, 0))
            print("DEBUG: Boss room",boss.x)
            if boss.x > 550 and Score < 1000:
                draw_hp_bar(screen, Screen_x//2 - 100, 100, boss.health, boss.maxHP,400,30,"???")
            else:
                draw_hp_bar(screen, Screen_x//2 - 100, 100, boss.health, boss.maxHP,400,30,"Sylvarath the Eternal")
            if Score <= 600:
                enemies.clear()
                slashes.clear()
                fade_in(screen, bossroom, 1000)
            
           
            if isFinish:     
               
                
                screen.blit(boss.images[int(pygame.time.get_ticks() / 100) % len(boss.images)], (boss.x, boss.y))
                if boss.x - player.x > 200 and not boss.left or boss.x > Screen_x:
                    boss.left = True
                    boss.right = False
                    boss.x -=110
                elif boss.x - player.x < -200 and not boss.right or boss.x < -100:
                    boss.left = False
                    boss.right = True
                    boss.x +=110
                if boss.left:
                    boss.move(-enemy_speed, 0)
                    boss.images = boss_flipped_move
                elif boss.right:
                    boss.move(enemy_speed, 0)
                    boss.images = boss_move
                boss_center = boss.x + boss_size_x // 2
                player_center = player.x + player.width // 2
                now = pygame.time.get_ticks()
                boss_skill = random.randint(1,3)
                if abs(boss_center - player_center) <= 100 and isFinish and now - last_boss_attack_time >= boss_cooldown:
                    boss_skill = random.randint(1,3)
                    skill = boss_skill
                    isFinish = False
                    skill_index = 0
                    skill_start_time = pygame.time.get_ticks()
                    
                    if boss.left:
                        boss.images = boss_attack_left[boss_skill]
                        
                    else:
                        boss.images = boss_attack_right[boss_skill]
                        
                            
                
            else:
                
                now = pygame.time.get_ticks()
                if skill_index < len(boss.images):
                    if now - skill_start_time >= 100:  # delay giữa các frame
                        skill_start_time = now
                        screen.blit(boss.images[skill_index], (boss.x, boss.y))
                        
                        # In ra thông tin chi tiết để debug
                        print("Frame:", skill_index, "Total frames:", len(boss.images))
                        print("Boss position:", boss.x, boss.y)
                        print("Player position:", player.x, player.y)
                        
                        # Điều chỉnh collision box cho mỗi skill
                        if skill == 1:  # Skill 1
                            if boss.left:
                                boss_rect = pygame.Rect(boss.x + 100, boss.y + 100, 200, 200)  # Tăng kích thước box
                            else:
                                boss_rect = pygame.Rect(boss.x + 300, boss.y + 100, 200, 200)
                        elif skill == 2:  # Skill 2
                            if boss.left:
                                boss_rect = pygame.Rect(boss.x + 50, boss.y + 100, 250, 250)  # Tăng kích thước box
                            else:
                                boss_rect = pygame.Rect(boss.x + 250, boss.y + 100, 250, 250)
                        else:  # Skill 3
                            if boss.left:
                                boss_rect = pygame.Rect(boss.x + 150, boss.y + 100, 100, 250)  # Tăng kích thước box
                            else:
                                boss_rect = pygame.Rect(boss.x + 200, boss.y + 100, 100, 250)
                        
                        
                        # 5 voi 9 la frame hop li cua cac skill
                        if skill_index >= 5 and skill_index < 9:  # Giảm số frame xuống
                            if boss_rect.colliderect(player_rect):
                                print("COLLISION DETECTED!")
                                print("Boss rect:", boss_rect)
                                print("Player rect:", player_rect)
                                GameOver = True
                                gameover_sound.play()
                        
                        skill_index += 1
                    else:
                        screen.blit(boss.images[skill_index], (boss.x, boss.y))
                else: # het animation
                    print("skill:",skill)
                    if skill == 1:
                        if boss.left:
                            boss.x -= 200
                        else:
                            boss.x += 200
                                
                    isFinish = True
                    skill_index = 0
                    last_boss_attack_time = pygame.time.get_ticks()
                    screen.blit(boss.images[0], (boss.x, boss.y))
                    
                    # Sau đó cập nhật lại animation như bình thường
                    if boss.left:
                        boss.images = boss_flipped_move
                    elif boss.right:
                        boss.images = boss_move


        for s in slashes:
            
            s_rect = pygame.Rect(s.x, s.y, s.image.get_width(), s.image.get_height())  # tạo khung rect bao quanh hình ảnh (x, y, width, s.height)
           
            if s.left:
                s.move(-Projectile_speed, 0)
            if s.right:
                s.move(Projectile_speed, 0)
            s.draw(screen)
            if s.x > Screen_x or s.x < 0:
                slashes.remove(s)
        for e in enemies:
            if e.left:
                e.move(-enemy_speed, 0)
                img = enemy_image
            if e.right:
                e.move(enemy_speed, 0)
                img = enemy_image_flip
            screen.blit(img[int(pygame.time.get_ticks() / 100) % len(enemy_image)], (e.x, e.y))
            if e.x < 0 or e.x > Screen_x:
                enemies.remove(e)
    if Dictionary:
        selected = ""
        draw_dictionary_window()
    if not start and not Dictionary:
        screen.blit(background_image[frame_index], (0, 0))
        button_rect = startGame_rect.inflate(40, 20)
        button_dictionary_rect = Dictionary_rect.inflate(40, 20)
        mouse_pos = pygame.mouse.get_pos()

        # Set default colors
        color = BUTTON_COLOR
        border_color = BUTTON_BORDER_COLOR
        color_dict = BUTTON_COLOR
        border_color_dict = BUTTON_BORDER_COLOR
        # Check hover
        if button_rect.collidepoint(mouse_pos):
       
            border_color = (0, 255, 255)  
        if button_dictionary_rect.collidepoint(mouse_pos):
            border_color_dict = (0, 255, 255)
        # Draw button rectangle
        pygame.draw.rect(screen, color, button_rect, border_radius=8)
        pygame.draw.rect(screen, color, button_dictionary_rect, border_radius=8)
        # Draw border if color is not None
        if border_color:
            pygame.draw.rect(screen, border_color, button_rect, 3, border_radius=8)
        if border_color_dict:
            pygame.draw.rect(screen, border_color_dict, button_dictionary_rect, 3, border_radius=8)
        # Draw text
        draw_start_window(button_rect, button_dictionary_rect)
        
    if start and not Dictionary:
        Higest_score_text = Score_font.render(f"Highest Score: {highest_score}", True, (255, 255, 255))
        score_text = Score_font.render(f"Score: {Score}", True, (255, 255, 255))
        screen.blit(Higest_score_text, (score_rect.centerx-50, score_rect.centery+30))
        screen.blit(score_text, (score_rect.centerx-50, score_rect.centery-10))

        if not isJump:
            screen.blit(runner[int(pygame.time.get_ticks() / 100) % len(runner)], (player.x, player.y))
        else:
            screen.blit(runner[1], (player.x, player.y)) #jumping image
        
        if GameOver:
            draw_game_over_window(GameOver_rect)
    
    #    not done
    pygame.display.update()
        
# Game button and text
Title = render_gradient_text("POKEMON RUNNER", Title_Font, (255, 223, 0), (255, 69, 58))
startGame_text = gameStart_font.render("Start game", True, (255, 228, 196))
startGame_rect = startGame_text.get_rect()
startGame_rect.topleft = (Screen_x // 2 - startGame_text.get_width() // 2 + 15, Screen_y // 2 - 50 )
button_startgame_rect = startGame_rect.inflate(40, 20)
button_startgame_rect.topleft = (startGame_rect.left - 20, startGame_rect.top -30)
Dictionary_text = Dicitonary_font.render("Dictionary", True, (255, 228, 196))
Dictionary_rect = Dictionary_text.get_rect()
Dictionary_rect.topleft = (Screen_x // 2 - startGame_text.get_width() // 2 + 17, Screen_y // 2  )
button_dictionary_rect = Dictionary_rect.inflate(40, 20)
button_dictionary_rect.topleft = (Dictionary_rect.left - 20, Dictionary_rect.top - 10)
GameOver_text = render_gradient_text("GAME OVER!", Title_Font, (255, 223, 0), (255, 69, 58))
Gameover_boss_text = render_gradient_text("GAME OVER!", Title_Font, (0, 191, 255), (0, 255, 127))
GameOver_rect = GameOver_text.get_rect()
GameOver_rect.topleft = (Screen_x // 2 - GameOver_text.get_width() // 2 + 15, Screen_y // 2-30 )
replay_text = Replay_font.render("Press R to replay", True, (0, 0, 0))
replay_rect = replay_text.get_rect()
replay_rect.topleft = (Screen_x // 2 - replay_text.get_width() // 2 + 15, Screen_y // 2 + 30)
replay_boss_text = Replay_font.render("Press R to replay", True, (255, 255, 25))
Choosing_text = Choosing_font.render("Choose your Pokemon", True, (0, 0, 0))
Choosing_rect = Choosing_text.get_rect()
Choosing_rect.topleft = (Screen_x // 2 - Choosing_text.get_width() // 2 , Screen_y // 2)
score_text = Score_font.render("Score: 0", True, (0, 0, 0))
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY_EVENT, spawn_rate)  # Sự kiện này sẽ xảy ra mỗi 2000ms (2 giây)
# Main game
slashes = [] 
enemies = []
isDone = True
start_time = pygame.time.get_ticks()

while running:
    Start_time = pygame.time.get_ticks()
    player_rect = pygame.Rect(player.x, player.y, player.images[0].get_width()-60, player.images[0].get_height())
    
    pygame.time.delay(60)
    clock.tick(27)
    if selected:
        if player.left:
            runner =character_flip[selected]
            slash_image = slash_color_flip[selected]
        if player.right:
            runner =character[selected]
            slash_image = slash_color[selected]
    # Xử lý khi nhấn vào dictionary và chọn Pokemon
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            # Điều kiện khi nhấn nút "Start Game"
            if button_startgame_rect.collidepoint(event.pos) and Dictionary == False and start == False:
                start = True
                player.x = Screen_x//2 - player.width//2
                player.y = 425
                enemies.clear()
                

                GameOver = False
                fade_in(screen, background1, 1000)
                
                start_time = pygame.time.get_ticks()
            
            # Điều kiện khi nhấn vào Dictionary
            if button_dictionary_rect.collidepoint(event.pos) and start == False and Dictionary == False:
                Dictionary = True  # Chuyển sang màn hình Dictionary
                selected = ""  # Reset lựa chọn Pokémon
                start = False
                print("DEBUG: Returning to Dictionary")
                fade_in(screen, background2, 1000)
                isDone = True  # Đảm bảo không cho phép chọn lại


            # Điều kiện chọn Pokemon khi đang ở trong Dictionary
            if Dictionary and isDone and selected == "":  # Chỉ khi Dictionary đang được hiển thị và chưa chọn Pokémon
                if option1_rect.collidepoint(event.pos):
                    selected = "charmander"
                    Dictionary = False  # Chọn Pokémon và thoát khỏi Dictionary
                    isDone = False
                    print("DEBUG: Chosen Charmander")
                if option2_rect.collidepoint(event.pos):
                    selected = "pikachu"
                    Dictionary = False  # Chọn Pokémon và thoát khỏi Dictionary
                    isDone = False
                    print("DEBUG: Chosen Pikachu")
                if option3_rect.collidepoint(event.pos):
                    selected = "trecko"
                    Dictionary = False  # Chọn Pokémon và thoát khỏi Dictionary
                    print("DEBUG: Chosen Trecko")
                    isDone = False
        if event.type == SPAWN_ENEMY_EVENT:
            if not GameOver and not Dictionary and Score < 500:
                k = random.randint(0,1)
                if k == 0:
                    new_enemy = Enemy(enemy_image,True,False,800,450)
                if k == 1:
                    new_enemy = Enemy(enemy_image,False,True,0,450)
                enemies.append(new_enemy)
    keys = pygame.key.get_pressed()
    
    if start:
        
        Dictionary = False
        Score = (pygame.time.get_ticks() - start_time) // 10 
        if Score >= 300 and Score < 500:
            if Score%50 == 0 and Score > 0:
                enemy_speed += 4
                spawn_rate -= 100
                print("Speed:" , enemy_speed)
        elif Score >= 0 and Score < 300:
            if Score%100 == 0 and Score > 0:
                spawn_rate -= 50
                enemy_speed += 2
                print("Speed:" , enemy_speed)
        
        
       
        if keys[pygame.K_a] and player.x > speed:
            
            player.right = False
            player.left = True
            player.move(-speed, 0)
        if keys[pygame.K_d] and player.x < Screen_x - player.width - speed:
           
            player.right = True
            player.left = False
            player.move(speed, 0)
        if keys[pygame.K_SPACE] and not isJump:
            jumping_sound.play()
            isJump = True
            y_velocity = jump_speed
        if keys[pygame.K_r] and GameOver:
            start_time = pygame.time.get_ticks() 
            boss.x = 800
            
            gameover_sound.stop()
            GameOver = False
            enemies.clear()
            player.x = Screen_x//2 - player.width//2
            last_slash_time = 0
            slashes.clear()
        if Score > highest_score:
            highest_score = Score
    cooldown_time = player.attack_speed
    current_time = pygame.time.get_ticks() + cooldown_time
    if keys[pygame.K_q] and current_time - last_slash_time > cooldown_time:
        if selected == "charmander":
           scaled_image = pygame.transform.scale(slash_image, (100,100 ))
           distance = 0
        else:
            scaled_image = pygame.transform.scale(slash_image, (200,200 ))
            distance = -50
        
        new_slash = Projectile(player.x, player.y  + distance, scaled_image, player.left, player.right)
        slashes.append(new_slash)
        last_slash_time = current_time
    if keys[pygame.K_ESCAPE]:
        boss.x = 800

        gameover_sound.stop()
        start_time = pygame.time.get_ticks()
        start = False
        Dictionary = False
        enemies.clear()
        player.y = 425


    if isJump:
        player.move(0, y_velocity)
        y_velocity += gravity

        # Kiểm tra va chạm với đất
        if player.bottom > player_base:
            player.bottom = player_base
            isJump = False
            y_velocity = 0
    # q
    for e in enemies:
        e_rect = e.images[0].get_rect(topleft=(e.x-50, e.y))
        if player_rect.colliderect(e_rect) and not GameOver:
            start_time = pygame.time.get_ticks()
            enemy_speed = 5
            spawn_rate = 2000
            GameOver = True
            gameover_sound.play()
    for i in slashes:
        i_rect = i.image.get_rect(topleft=(i.x, i.y+10))
        # Lấy frame hiện tại của boss, tùy vào trạng thái đang attack hay idle
        pygame.draw.rect(screen,(255,255,255),i_rect,2)

        for e in enemies[:]:  # Use a copy to avoid modification during iteration
            e_rect = e.images[0].get_rect(topleft=(e.x-50, e.y))
            
            if i_rect.colliderect(e_rect):
                if not GameOver:  # Optional: only play if not game over
                    dying_sound.play()
                enemies.remove(e)
                break  # Stop checking after removing one enemy
    for i in slashes:
        # Update boss_rect trước khi kiểm tra va chạm
        if boss.left:
            boss_rect = pygame.Rect(boss.x + 330, boss.y + 80, 100, 200)
        else:
            boss_rect = pygame.Rect(boss.x + 100, boss.y + 80, 100, 200)
        
        i_rect = i.image.get_rect(topleft=(i.x+10, i.y+10))
        if i_rect.colliderect(boss_rect) and Score >= 500 and boss.images != boss_death :
            print("HIT BOSS!")
            boss.health -= random.randint(10,20)
            slashes.remove(i)
            if boss.health <= 0:
                boss.images = boss_death
            break


       
    draw_window()

pygame.quit()