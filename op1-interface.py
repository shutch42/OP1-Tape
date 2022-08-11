import sys, pygame
from reel import Reel

pygame.init()

clock = pygame.time.Clock()

size = width, height = 640, 480
gray = 120, 120, 120

pygame.mouse.set_visible(False)
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

reel1 = Reel(150, 170, 0)
reel2 = Reel(490, 170, 0)

done = False
play = False

while not done:
    for event in pygame.event.get():
        # Check for exit
        if event.type == pygame.QUIT:
            done = True
        
        # Toggle play/pause
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            play = not play
    
    # Clear screen
    screen.fill(gray)
    
    # Rotate reels if music is playing
    if play:
        reel1.rotate()
        reel2.rotate()
    
    # Render reels
    screen.blit(reel1.img, reel1.rect)
    screen.blit(reel2.img, reel2.rect)

    # Display stuff
    pygame.display.flip()

    # Move to next frame according to frame rate
    clock.tick(60)
