import pygame
import random
import time
from sys import exit
from button import Button # By importing Button we can access methods from the Button class
pygame.init()
clock = pygame.time.Clock()

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

GREEN_ON = (0, 255, 0)
GREEN_OFF = (0, 227, 0)
RED_ON = (255, 0, 0)
RED_OFF = (227, 0, 0)
BLUE_ON = (0, 0, 255)
BLUE_OFF = (0, 0, 227)
YELLOW_ON = (255, 255, 0)
YELLOW_OFF = (227, 227, 0)

# Pass in respective sounds for each color
GREEN_SOUND = pygame.mixer.Sound('music/bell1.mp3') # bell1
RED_SOUND = pygame.mixer.Sound('music/bell2.mp3') # bell2
BLUE_SOUND = pygame.mixer.Sound('music/bell3.mp3') # bell3
YELLOW_SOUND = pygame.mixer.Sound('music/bell4.mp3') # bell4

# Button Sprite Objects
green = Button(GREEN_ON, GREEN_OFF, GREEN_SOUND, 10, 10)
red = Button(RED_ON, RED_OFF, RED_SOUND, 260, 10)
blue = Button(BLUE_ON, BLUE_OFF, BLUE_SOUND, 260, 260)
yellow = Button(YELLOW_ON, YELLOW_OFF, YELLOW_SOUND, 10, 260)

# Variables
colors = ["green", "red", "blue", "yellow"]
cpu_sequence = []
choice = ""
font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 25)
game_on = True
score = 0



'''
Draw timer
'''
def timer():
    starting_time = int((pygame.time.get_ticks() / 1000 - start_time))
    timer_surface = font.render(f"Timer: {starting_time}", False, 'White')
    timer_rect = timer_surface.get_rect(midtop=(250, 150))
    SCREEN.blit(timer_surface, timer_rect)
    return starting_time

'''
Draws game board
'''
def draw_board():
    # Call the draw method on all four button objects
    green.draw(SCREEN)
    red.draw(SCREEN)
    blue.draw(SCREEN)
    yellow.draw(SCREEN)

'''
Chooses a random color and appends to cpu_sequence.
Illuminates randomly chosen color.
'''
def cpu_turn():
    button_map = {
        "green": green,
        "red": red,
        "blue": blue,
        "yellow": yellow,
    }

    choice = random.choice(colors) # pick random color
    cpu_sequence.append(choice) # update cpu sequence
    button_map[choice].update(SCREEN)
'''
Plays pattern sequence that is being tracked by cpu_sequence
'''
def repeat_cpu_sequence():
    if(len(cpu_sequence) != 0):
        for color in cpu_sequence:
            if color == "green":
                green.update(SCREEN)
            elif color == "red":
                red.update(SCREEN)
            elif color == "blue":
                blue.update(SCREEN)
            else:
                yellow.update(SCREEN)
            pygame.time.wait(500)

'''
After cpu sequence is repeated the player must attempt to copy the same pattern sequence.
The player is given 3 seconds to select a color and checks if the selected color matches the cpu
If player is unable to select a color within 3 seconds then the game is over and the pygame windo
'''
def player_turn():
    turn_time = time.time()
    players_sequence = []
    while time.time() <= turn_time + 3 and len(players_sequence) < len(cpu_sequence):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1: # button click occured
                # Grab the current position of mouse here
                pos = pygame.mouse.get_pos()
                if green.selected(pos): # green button was selected
                    green.update(SCREEN) # illuminate button
                    players_sequence.append("green") # add to player sequence
                    check_sequence(players_sequence) # check if player choice was correct
                    turn_time = time.time() # reset timer
                # Check other three options
                if red.selected(pos):
                    red.update(SCREEN)
                    players_sequence.append("red")
                    check_sequence(players_sequence)
                    turn_time = time.time()
                if blue.selected(pos):
                    blue.update(SCREEN)
                    players_sequence.append("blue")
                    check_sequence(players_sequence)
                    turn_time = time.time()
                if yellow.selected(pos):
                    yellow.update(SCREEN)
                    players_sequence.append("yellow")
                    check_sequence(players_sequence)
                    turn_time = time.time()
                
    # If player does not select a button within 3 seconds then the game closes
    if not time.time() <= turn_time + 3:
        game_over()

'''
Checks if player's move matches the cpu pattern sequence
'''
def check_sequence(players_sequence):
    if players_sequence != cpu_sequence[:len(players_sequence)]:
        game_over()

'''
Quits game and closes pygame window
'''
def game_over():
    global game_on
    game_on = False  # Transition to the exit screen

def exit_screen():
    play_again = font.render('Play Again?', False, 'White')
    play_again_rect = play_again.get_rect(midbottom=(250, 400))
    exit_game = font.render('Exit', False, 'White')
    exit_game_rect = exit_game.get_rect(midbottom=(250, 450))
    gameover_img = pygame.image.load('photos/gameover.png').convert_alpha()
    gameover_img = pygame.transform.scale(gameover_img, (360, 360))
    gameover_rect = gameover_img.get_rect(center=(250, 150))
    
    SCREEN.fill('Black')  # Clear the screen
    SCREEN.blit(gameover_img, gameover_rect)
    SCREEN.blit(play_again, play_again_rect)
    SCREEN.blit(exit_game, exit_game_rect)

    # Input handling for restarting or exiting
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()  # Get mouse position
            if exit_game_rect.collidepoint(mouse_pos):  # Check if Exit is clicked
                pygame.quit()
                exit()
            if play_again_rect.collidepoint(mouse_pos):  # Check if Play Again is clicked
                reset_game()  # Restart the game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def main_menu():
    SCREEN.fill('Black')  # Clear the screen
    title = pygame.image.load('photos/simon_says.png')
    title = pygame.transform.scale(title, (450, 220))
    title_rect = title.get_rect(center=(250, 150))

    start_game = font.render('Start Game', False, 'White')
    start_game_rect = start_game.get_rect(center=(250, 300))

    exit_game = font.render('Exit', False, 'White')
    exit_game_rect = exit_game.get_rect(center=(250, 350))

    SCREEN.blit(title, title_rect)
    SCREEN.blit(start_game, start_game_rect)
    SCREEN.blit(exit_game, exit_game_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()  # Get the mouse position
            if start_game_rect.collidepoint(mouse_pos):  # Check if "Start Game" is clicked
                return "start"
            if exit_game_rect.collidepoint(mouse_pos):  # Check if "Exit" is clicked
                pygame.quit()
                exit()
    return "menu"


def reset_game():
    global game_on, cpu_sequence, start_time
    game_on = True
    cpu_sequence = []  # Clear the CPU sequence
    start_time = pygame.time.get_ticks() / 1000  # Reset the timer

# Initialize start time at the beginning of the game
start_time = pygame.time.get_ticks() / 1000

# Initialize start_time globally
start_time = None

# Main Game Loop
menu_active = True
game_on = False
start_time = None

while True:
    if menu_active:
        result = main_menu()
        if result == "start":
            menu_active = False
            game_on = True  # Start the game
            start_time = pygame.time.get_ticks() / 1000  # Initialize the timer
    elif game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Clear the screen and run the game
        SCREEN.fill('Black')
        timer()  # Display the timer
        draw_board()  # Draw the game board
        repeat_cpu_sequence()  # Show the CPU's sequence
        cpu_turn()  # CPU picks a new color
        player_turn()  # Player recreates the sequence
    else:
        exit_screen()  # Show the exit screen

    pygame.display.update()
    clock.tick(60)