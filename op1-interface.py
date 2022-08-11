import sys, pygame

pygame.init()

clock = pygame.time.Clock()

size = width, height = 800, 400
gray = 120, 120, 120

screen = pygame.display.set_mode(size)

reel = pygame.image.load("tape_reel.png").convert_alpha()

REEL_SIZE = (300, 300)
reel = pygame.transform.smoothscale(reel, REEL_SIZE)
reel_rect1 = reel.get_rect(center=(200,170))
reel_rect2 = reel.get_rect(center=(600,170))

REEL_POSITION = (50, 20)


def rotate_center(image, rect, angle):
	rotated_image = pygame.transform.rotate(image, angle)
	rect = rotated_image.get_rect(center = rect.center)

	return rotated_image, rect

angle = 0

done = False

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	
	screen.fill(gray)
	angle += 2
	rotated_reel, reel_rect1 = rotate_center(reel, reel_rect1, angle)
	rotated_reel, reel_rect2 = rotate_center(reel, reel_rect2, angle)
	screen.blit(rotated_reel, reel_rect1)
	screen.blit(rotated_reel, reel_rect2)
	pygame.display.flip()
	clock.tick(60)
