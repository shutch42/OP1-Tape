import pygame
from reel import Reel
from track import Track

pygame.init()

clock = pygame.time.Clock()

size = width, height = 800, 480
gray = 120, 120, 120

pygame.mouse.set_visible(False)
# screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen = pygame.display.set_mode(size)

play_icon = pygame.image.load("img/play.png").convert_alpha()
play_icon = pygame.transform.smoothscale(play_icon, (50, 50))
play_rect = play_icon.get_rect(center=(400, 220))

reel1 = Reel(200, 170, 0)
reel2 = Reel(600, 170, 45)

music = Track()

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
            if play:
                music.play()
            else:
                music.pause()
    
    # Clear screen
    screen.fill(gray)
    
    # Rotate reels if music is playing
    if play:
        reel1.rotate()
        reel2.rotate()
        screen.blit(play_icon, play_rect)
    
    # Render reels
    # FIXME: Tape across and reader need different RGB values
    # pygame.draw.rect(screen, (39.6, 42.7, 47.1), (200, 260, 400, 10))
    # pygame.draw.rect(screen, (80, 82, 85.1), (385, 260, 30, 30))
    screen.blit(reel1.img, reel1.rect)
    screen.blit(reel2.img, reel2.rect)

    # Display stuff
    pygame.display.flip()

    # Move to next frame according to frame rate
    clock.tick(60)
