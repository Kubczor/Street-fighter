import pygame, sys
from button import Button
from pygame import mixer
from fighter import Fighter
from samuraj import Samuraj
from king import King
from dzikus import Dzikus
from lowca import Lowca

mixer.init()
pygame.init()

#okno
s_WIDTH = 1000
s_HEIGTH = 600

screen = pygame.display.set_mode((s_WIDTH, s_HEIGTH))
pygame.display.set_caption("Fighter")

#FPS
framework = pygame.time.Clock()
FPS = 60

#kolorki
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN =(0, 255, 0)

#wlasciwosci gry
intro_count = 3
last_count_update = pygame.time.get_ticks()
score =[0, 0] #[P1, P2] wynik
round_over = False
round_over_cd = 2000

#definicja wielkosci wojownika
SAMURAJ_SIZE = 200
SAMURAJ_SCALE = 4
SAMURAJ_OFFSET = [90, 75]
SAMURAJ_DATA = [SAMURAJ_SIZE, SAMURAJ_SCALE, SAMURAJ_OFFSET]
KROL_SIZE = 160
KROL_SCALE = 3.5
KROL_OFFSET = [65, 102]
KROL_DATA = [KROL_SIZE, KROL_SCALE, KROL_OFFSET]
DZIKUS_SIZE = 126
DZIKUS_SCALE = 4.5
DZIKUS_OFFSET = [53, 42]
DZIKUS_DATA = [DZIKUS_SIZE, DZIKUS_SCALE, DZIKUS_OFFSET]
LOWCA_SIZE = 150
LOWCA_SCALE = 5
LOWCA_OFFSET = [68, 61]
LOWCA_DATA = [LOWCA_SIZE, LOWCA_SCALE, LOWCA_OFFSET]

#muzyczka efekty miecza
sword_fx = pygame.mixer.Sound("sounds/sword1.wav")
sword2_fx = pygame.mixer.Sound("sounds/sword2.wav")
sword2_fx.set_volume(0.25)
katana_fx = pygame.mixer.Sound("sounds/katana.mp3")
spear_fx = pygame.mixer.Sound("sounds/spear.mp3")

#tło gry
bg_image = pygame.image.load("bg/background.jpg").convert_alpha()
#tekstury postaci
samuraj_sheet = pygame.image.load("samuraj/Sprites/samuraj5.png").convert_alpha()
krol_sheet = pygame.image.load("king/Sprites/krol5.png").convert_alpha()
dzikus_sheet = pygame.image.load("dzikus/Sprites/dzikus2.png").convert_alpha()
lowca_sheet = pygame.image.load("lowca/Sprites/lowca.png").convert_alpha()
#czcionka 
count_font = pygame.font.Font("font/font.ttf", 80)
score_font = pygame.font.Font("font/font.ttf", 30)

#klatki postaci
SAMURAJ_ANIMATION_STEPS = [8, 8, 2, 6, 6, 4, 6]
KROL_ANIMATION_STEPS = [8, 8, 2, 4, 4, 4, 6]
DZIKUS_ANIMATION_STEPS = [10, 8, 3, 7, 6, 3, 11]
LOWCA_ANIMATION_STEPS = [8, 8, 2, 5, 5, 3, 8]

#rysowanie tła
def bg_draw(bg_image):
    bg_scaled = pygame.transform.scale(bg_image, (s_WIDTH, s_HEIGTH))
    screen.blit(bg_scaled, (0,0))

#pasek zdrowia  
def health_bar(health, x ,y):
    ratio = health / 100
    pygame.draw.rect(screen, BLACK, (x-2, y-2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400*ratio, 30))

#pasek ataku specjalnego
def special_bar(special,x,y):
    ratio = special / 50
    pygame.draw.rect(screen, BLACK, (x-2, y-2, 404, 14))
    pygame.draw.rect(screen, GREEN, (x, y, 400*ratio, 10))

#rysowanie odliczania
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))    


def main(fighter_1, fighter_2, score):
    
    pygame.mixer.music.load("sounds/menu.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0, 5000)

    open = True
    #okno
    s_WIDTH = 1000
    s_HEIGTH = 600


    intro_count = 3
    last_count_update = pygame.time.get_ticks()
    #score = [0, 0] #[P1, P2] wynik
    round_over = False
    round_over_cd = 2000
    
    while open:
        framework.tick(FPS)
        #rysowanie tła
        bg_draw(bg_image)
        #pokaz zycie wojownika
        health_bar(fighter_1.health, 20, 20)
        health_bar(fighter_2.health, 580, 20)
        #pokaz atak specjalny
        special_bar(fighter_1.special, 20, 580)
        special_bar(fighter_2.special, 580, 580)
        #rysowanie wyniku
        draw_text(str(score[0]), score_font, RED, 20, 60)
        draw_text(str(score[1]), score_font, RED, 580, 60)

        #ataki specjalne
        fighter_1.special_ability(fighter_2) 
        fighter_2.special_ability(fighter_1)    

        #odliczanie do startu
        if intro_count < 0:
            #poruszanie sie
            fighter_1.move(s_WIDTH, s_HEIGTH, screen, fighter_2, round_over)
            fighter_2.move(s_WIDTH, s_HEIGTH, screen, fighter_1, round_over)
        else:
            if intro_count > 0:
                draw_text(str(intro_count), count_font, RED, 465, 200)
            if intro_count == 0:
                draw_text("FIGHT", count_font, RED, 375, 200)
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()
                
        #zmiany na ekranie
        fighter_1.update()
        fighter_2.update()
        
        #rysowanie postaci
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        #sprawdzanie czy któryś z graczy przegrał
        if round_over == False:
            if fighter_1.alive == False:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif fighter_2.alive == False:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            if fighter_1.alive == False:
                    draw_text("Player2 win", count_font, RED, 300, 200)   
            else:
                    draw_text("Player1 win", count_font, RED, 300, 200)
            if pygame.time.get_ticks() - round_over_time > round_over_cd:
                round_over = False
                intro_count = 3    
                play(score)  
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                open = False
    
        pygame.display.update()







SCREEN = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")
BG2 = pygame.image.load("assets/options.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("font/font2.ttf", size)

def play(score):
    pygame.mixer.music.load("sounds/fight2.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0, 2500)
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("Wybierz wojownika P1.", True, "Red")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(500, 100))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_1 = Button(image=pygame.image.load("assets/samuraj.gif"), pos=(125, 300), 
                            text_input="", font=get_font(20), base_color="White", hovering_color="Green")
        PLAY_2 = Button(image=pygame.image.load("assets/krol.jpeg"), pos=(375, 300), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        PLAY_3 = Button(image=pygame.image.load("assets/dzikus.jpeg"), pos=(625, 300), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        PLAY_4 = Button(image=pygame.image.load("assets/lowca.png"), pos=(875, 300), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK = Button(image=None, pos=(500, 500), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_1.changeColor(PLAY_MOUSE_POS)
        PLAY_1.update(SCREEN)

        PLAY_2.changeColor(PLAY_MOUSE_POS)
        PLAY_2.update(SCREEN)

        PLAY_3.changeColor(PLAY_MOUSE_POS)
        PLAY_3.update(SCREEN)

        PLAY_4.changeColor(PLAY_MOUSE_POS)
        PLAY_4.update(SCREEN)

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_1.checkForInput(PLAY_MOUSE_POS):
                    fighter_1 = Samuraj(1, 200, 310, False, SAMURAJ_DATA, samuraj_sheet, SAMURAJ_ANIMATION_STEPS, katana_fx)
                    play2(fighter_1, score)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_2.checkForInput(PLAY_MOUSE_POS):
                    fighter_1 = King(1, 200, 310, False, KROL_DATA, krol_sheet, KROL_ANIMATION_STEPS, sword_fx)
                    play3(fighter_1, score)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_3.checkForInput(PLAY_MOUSE_POS):
                    fighter_1 = Dzikus(1, 200, 310, False, DZIKUS_DATA, dzikus_sheet, DZIKUS_ANIMATION_STEPS, sword2_fx)
                    play4(fighter_1, score)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_4.checkForInput(PLAY_MOUSE_POS):
                    fighter_1 = Lowca(1, 200, 310, False, LOWCA_DATA, lowca_sheet, LOWCA_ANIMATION_STEPS, spear_fx)
                    play5(fighter_1, score)       
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()
    

def play2(fighter_1, score):
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("Wybierz wojownika P2.", True, "Yellow")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(500, 100))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        # PLAY_1 = Button(image=pygame.image.load("assets/samuraj.gif"), pos=(125, 300), 
        #                     text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        PLAY_2 = Button(image=pygame.image.load("assets/krol.jpeg"), pos=(375, 300), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        PLAY_3 = Button(image=pygame.image.load("assets/dzikus.jpeg"), pos=(625, 300), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        PLAY_4 = Button(image=pygame.image.load("assets/lowca.png"), pos=(875, 300), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        PLAY_BACK = Button(image=None, pos=(500, 500), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        # PLAY_1.changeColor(PLAY_MOUSE_POS)
        # PLAY_1.update(SCREEN)

        PLAY_2.changeColor(PLAY_MOUSE_POS)
        PLAY_2.update(SCREEN)

        PLAY_3.changeColor(PLAY_MOUSE_POS)
        PLAY_3.update(SCREEN)

        PLAY_4.changeColor(PLAY_MOUSE_POS)
        PLAY_4.update(SCREEN)

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_2.checkForInput(PLAY_MOUSE_POS):
                    fighter_2 = King(2, 700, 310, True, KROL_DATA, krol_sheet, KROL_ANIMATION_STEPS, sword_fx)
                    main(fighter_1, fighter_2, score)
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_3.checkForInput(PLAY_MOUSE_POS):
                    fighter_2 = Dzikus(2, 700, 310, True, DZIKUS_DATA, dzikus_sheet, DZIKUS_ANIMATION_STEPS, sword2_fx)
                    main(fighter_1, fighter_2, score)
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_4.checkForInput(PLAY_MOUSE_POS):
                    fighter_2 = Lowca(2, 700, 310, True, LOWCA_DATA, lowca_sheet, LOWCA_ANIMATION_STEPS, spear_fx)
                    main(fighter_1, fighter_2, score) 
                    pygame.quit()
                    sys.exit()     
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    play(score)
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def play3(fighter_1, score):
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("Wybierz wojownika P2.", True, "Yellow")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(500, 100))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_1 = Button(image=pygame.image.load("assets/samuraj.gif"), pos=(125, 300), 
                            text_input="", font=get_font(20), base_color="White", hovering_color="Green")
        # PLAY_2 = Button(image=pygame.image.load("assets/krol.jpeg"), pos=(375, 300), 
        #                     text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        PLAY_3 = Button(image=pygame.image.load("assets/dzikus.jpeg"), pos=(625, 300), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        PLAY_4 = Button(image=pygame.image.load("assets/lowca.png"), pos=(875, 300), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        PLAY_BACK = Button(image=None, pos=(500, 500), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_1.changeColor(PLAY_MOUSE_POS)
        PLAY_1.update(SCREEN)

        # PLAY_2.changeColor(PLAY_MOUSE_POS)
        # PLAY_2.update(SCREEN)

        PLAY_3.changeColor(PLAY_MOUSE_POS)
        PLAY_3.update(SCREEN)

        PLAY_4.changeColor(PLAY_MOUSE_POS)
        PLAY_4.update(SCREEN)

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_1.checkForInput(PLAY_MOUSE_POS):
                    fighter_2 = Samuraj(2, 700, 310, True, SAMURAJ_DATA, samuraj_sheet, SAMURAJ_ANIMATION_STEPS, katana_fx)
                    main(fighter_1, fighter_2, score)
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_3.checkForInput(PLAY_MOUSE_POS):
                    fighter_2 = Dzikus(2, 700, 310, True, DZIKUS_DATA, dzikus_sheet, DZIKUS_ANIMATION_STEPS, sword2_fx)
                    main(fighter_1, fighter_2, score)
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_4.checkForInput(PLAY_MOUSE_POS):
                    fighter_2 = Lowca(2, 700, 310, True, LOWCA_DATA, lowca_sheet, LOWCA_ANIMATION_STEPS, spear_fx)
                    main(fighter_1, fighter_2, score)
                    pygame.quit()
                    sys.exit() 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    play(score)
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def play4(fighter_1, score):
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("Wybierz wojownika P2.", True, "Yellow")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(500, 100))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_1 = Button(image=pygame.image.load("assets/samuraj.gif"), pos=(125, 300), 
                            text_input="", font=get_font(20), base_color="White", hovering_color="Green")
        PLAY_2 = Button(image=pygame.image.load("assets/krol.jpeg"), pos=(375, 300), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        # PLAY_3 = Button(image=pygame.image.load("assets/dzikus.jpeg"), pos=(625, 300), 
        #                     text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        PLAY_4 = Button(image=pygame.image.load("assets/lowca.png"), pos=(875, 300), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK = Button(image=None, pos=(500, 500), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_1.changeColor(PLAY_MOUSE_POS)
        PLAY_1.update(SCREEN)

        PLAY_2.changeColor(PLAY_MOUSE_POS)
        PLAY_2.update(SCREEN)

        # PLAY_3.changeColor(PLAY_MOUSE_POS)
        # PLAY_3.update(SCREEN)

        PLAY_4.changeColor(PLAY_MOUSE_POS)
        PLAY_4.update(SCREEN)

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_1.checkForInput(PLAY_MOUSE_POS):
                    fighter_2 = Samuraj(2, 700, 310, True, SAMURAJ_DATA, samuraj_sheet, SAMURAJ_ANIMATION_STEPS, katana_fx)
                    main(fighter_1, fighter_2, score)
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_2.checkForInput(PLAY_MOUSE_POS):
                    fighter_2 = King(2, 700, 310, True, KROL_DATA, krol_sheet, KROL_ANIMATION_STEPS, sword_fx)
                    main(fighter_1, fighter_2, score)
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_4.checkForInput(PLAY_MOUSE_POS):
                    fighter_2 = Lowca(2, 700, 310, True, LOWCA_DATA, lowca_sheet, LOWCA_ANIMATION_STEPS, spear_fx)
                    main(fighter_1, fighter_2, score)
                    pygame.quit()
                    sys.exit()   
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    play(score)
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def play5(fighter_1, score):
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("Wybierz wojownika P2.", True, "Yellow")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(500, 100))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_1 = Button(image=pygame.image.load("assets/samuraj.gif"), pos=(125, 300), 
                            text_input="", font=get_font(20), base_color="White", hovering_color="Green")
        PLAY_2 = Button(image=pygame.image.load("assets/krol.jpeg"), pos=(375, 300), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        PLAY_3 = Button(image=pygame.image.load("assets/dzikus.jpeg"), pos=(625, 300), 
                            text_input="", font=get_font(75), base_color="White", hovering_color="Green")
        # PLAY_4 = Button(image=pygame.image.load("assets/lowca.png"), pos=(875, 300), 
        #                     text_input="", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK = Button(image=None, pos=(500, 500), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_1.changeColor(PLAY_MOUSE_POS)
        PLAY_1.update(SCREEN)

        PLAY_2.changeColor(PLAY_MOUSE_POS)
        PLAY_2.update(SCREEN)

        PLAY_3.changeColor(PLAY_MOUSE_POS)
        PLAY_3.update(SCREEN)

        # PLAY_4.changeColor(PLAY_MOUSE_POS)
        # PLAY_4.update(SCREEN)

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_1.checkForInput(PLAY_MOUSE_POS):
                    fighter_2 = Samuraj(2, 700, 310, True, SAMURAJ_DATA, samuraj_sheet, SAMURAJ_ANIMATION_STEPS, katana_fx)
                    main(fighter_1, fighter_2, score)
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_2.checkForInput(PLAY_MOUSE_POS):
                    fighter_2 = King(2, 700, 310, True, KROL_DATA, krol_sheet, KROL_ANIMATION_STEPS, sword_fx)
                    main(fighter_1, fighter_2, score)
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_3.checkForInput(PLAY_MOUSE_POS):
                    fighter_2 = Dzikus(2, 700, 310, True, DZIKUS_DATA, dzikus_sheet, DZIKUS_ANIMATION_STEPS, sword2_fx)
                    main(fighter_1, fighter_2, score)
                    pygame.quit()
                    sys.exit()  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main(fighter_1, fighter_2, score)
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG2, (0, 0))
        
    

        OPTIONS_BACK = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(800, 500), 
                            text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color="Black")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    pygame.mixer.music.load("sounds/fight2.wav")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1, 0.0, 2500)
    while True:
        SCREEN.blit(BG, (0, 0))
        score =[0, 0]   
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(500, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(500, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(500, 380), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(500, 510), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play(score)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()