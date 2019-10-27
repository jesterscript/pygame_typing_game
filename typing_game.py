import pygame
import random

def load_words_file(filename):
    word_file = open(filename, "r")
    lines_read = word_file.readlines()
    word_file.close()
    return lines_read
def render_text(display_surface, font, text_content, color, position):
    text = font.render(text_content, True, color)
    display_surface.blit(text, position)
def release_wave(count,lines_read,words_on_screen):#count : how many words will be spawned
    for i in range(count):
        randomed = random.randrange(0,len(lines_read)) 
        randomed_word = lines_read[randomed].replace("\n","")
        random_y = random.randrange(0,600)
        words_on_screen.append({"word": randomed_word,"coordinate": (0,random_y)})
def is_word_on_screen(words_on_screen,word):
    for i in range(len(words_on_screen)):
        if word == words_on_screen[i]["word"]:
            return i 
    return -1
def logic():
    #initialization
    lines_read = load_words_file("english_words.txt")# load words from the file
    pygame.init()
    display_surface = pygame.display.set_mode((800, 500))
    pygame.display.set_caption("Typing game")
    clock = pygame.time.Clock()
    run = True
    ended = False
    #game logic
    words_on_screen = []
    #text propertiies
    font = pygame.font.Font("freesansbold.ttf", 32)
    dx = 2 # moving speed for texts
    countdown_timer = 60 
    word_spawn_timer = pygame.time.get_ticks()# used for spawning words
    typing_buffer = []
    current_text = ""
    success_count = 0
    while run:
        countdown_timer = 60 - (pygame.time.get_ticks() / 1000)
        if int(countdown_timer) <= 0:#end game
            display_surface.fill((255,255,255))
            render_text(display_surface,font,"Game Over. Score :  {0} word per minute".format(success_count),(0,0,0),(150,250))
            ended = True
        if not ended:
            display_surface.fill((255,255,255))
            if(pygame.time.get_ticks()-word_spawn_timer > 700):
                word_spawn_timer = pygame.time.get_ticks()
                release_wave(1,lines_read,words_on_screen)
            for word_info in words_on_screen:
                word_info["coordinate"] = (word_info["coordinate"][0] + dx,word_info["coordinate"][1])
                render_text(display_surface,font,word_info["word"],(0,0,0),word_info["coordinate"])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if pygame.key.name(event.key) == "return":
                        index_found = is_word_on_screen(words_on_screen,current_text)
                        if index_found != -1:
                            words_on_screen.pop(index_found)
                            success_count += 1
                        else:
                            print("wrong")
                        typing_buffer = []
                    else:
                        if pygame.key.name(event.key) == "backspace": #if backspace then delete last element of typing buffer
                            if len(typing_buffer) != 0:
                                typing_buffer.pop(len(typing_buffer)-1)
                        else:
                            typing_buffer.append(pygame.key.name(event.key))
                    current_text = "".join(typing_buffer)
            render_text(display_surface,font,current_text,(0,0,0),(20,450))
            render_text(display_surface,font,str(countdown_timer),(0,0,0),(600,450))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(60)
logic()
