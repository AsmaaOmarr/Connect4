import pygame
import sys
from Buttom import Button
from MiniMaxOnly import MiniMaxComputer
from MINIMAX_With_Alpha_Beta import Connect4Easy_Medium_Level
from TopLevels.MINIMAX_With_Alpha_Beta_TopLevel import Connect4TopLevel
from TopLevels.MiniMaxOnlyTopLevel import MiniMaxWithMiniMax

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")
BG = pygame.image.load("assets/Background.png")


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


def minimax_With_minimax():
    while True:
        algorithm = MiniMaxWithMiniMax()
        SCREEN.blit(algorithm)
        pygame.display.update()    

def minimax_With_computer():
    while True:
        algorithm = MiniMaxComputer()
        SCREEN.blit(algorithm)
        pygame.display.update()  

def playEasy():
    while True:
        t=2
        algorithm = Connect4Easy_Medium_Level(3)
        SCREEN.blit(algorithm)
        pygame.display.update()  

def playMedium():
    while True:
        t=2
        algorithm = Connect4Easy_Medium_Level(5)
        SCREEN.blit(algorithm)
        pygame.display.update()       

def playard():
    while True:
        algorithm = Connect4TopLevel()
        SCREEN.blit(algorithm)
        pygame.display.update()                 

def MINIMAX_With_Alpha_Beta_pruning():
    pygame.display.set_caption("MINIMAX With Alpha Beta pruning")
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(30).render("MINIMAX With Alpha Beta pruning", True, "#C1FFC1")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        EASY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 200), 
                            text_input="Easy", font=get_font(75), base_color="#C1FFC1", hovering_color="White")
        MEDIUM_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 350), 
                            text_input="Medium", font=get_font(75), base_color="#C1FFC1", hovering_color="White")
        HARD_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 500), 
                            text_input="Hard", font=get_font(75), base_color="#C1FFC1", hovering_color="White")
        BACK_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 650), 
                            text_input="Back", font=get_font(75), base_color="#B4EEB4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [EASY_BUTTON, MEDIUM_BUTTON, HARD_BUTTON,BACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EASY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    playEasy()
                if MEDIUM_BUTTON.checkForInput(MENU_MOUSE_POS):
                    playMedium()
                if HARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                   playard()
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()
  

        pygame.display.update()

def MINIMAXAlgorithmMenu():
    pygame.display.set_caption("MINIMAX")
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MINIMAX", True, "#C1FFC1")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        EASY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="Easy", font=get_font(50), base_color="#C1FFC1", hovering_color="White")
        HARD_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 400), 
                            text_input="Hard", font=get_font(50), base_color="#C1FFC1", hovering_color="White")
        BACK_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 550), 
                            text_input="Back", font=get_font(50), base_color="#B4EEB4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [EASY_BUTTON,HARD_BUTTON, BACK_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if EASY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    minimax_With_computer()
                if HARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                    minimax_With_minimax()    
                if BACK_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()
                

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("CONNECT 4", True, "#C1FFC1")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        MiniMax_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="MiniMax", font=get_font(30), base_color="#C1FFC1", hovering_color="White")
        Alpha_Beta_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="MiniMax With Alpha-Beta pruning ", font=get_font(17), base_color="#C1FFC1", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(50), base_color="#CD2626", hovering_color="White")
        

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [MiniMax_BUTTON, Alpha_Beta_BUTTON,QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MiniMax_BUTTON.checkForInput(MENU_MOUSE_POS):
                    MINIMAXAlgorithmMenu()
                if Alpha_Beta_BUTTON.checkForInput(MENU_MOUSE_POS):
                    MINIMAX_With_Alpha_Beta_pruning()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()    
                

        pygame.display.update()

main_menu()




                