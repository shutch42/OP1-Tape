import pygame


class Reel:
    REEL_SIZE = (250, 250)
    IMAGE_FILE = "img/tape_reel.png"
    REEL_SPEED = 2

    def __init__(self, center_x: int=125, center_y: int=125, angle: float=0) -> None:
        img = pygame.image.load(self.IMAGE_FILE).convert_alpha()
        self.init_img = pygame.transform.smoothscale(img, self.REEL_SIZE)
        self.img = pygame.transform.rotate(self.init_img, angle)
        self.angle = angle
        self.rect = self.img.get_rect(center=(center_x, center_y))

    def rotate(self):
        self.angle += self.REEL_SPEED
        self.img = pygame.transform.rotate(self.init_img, self.angle)
        self.rect = self.img.get_rect(center = self.rect.center)

