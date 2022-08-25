import pygame


class Reel:
    REEL_SIZE = (300, 300)
    IMAGE_FILE = "img/tape_reel.png"

    def __init__(self, center_x: int = 125, center_y: int = 125, angle: float = 0) -> None:
        img = pygame.image.load(self.IMAGE_FILE).convert_alpha()
        self.init_img = pygame.transform.smoothscale(img, self.REEL_SIZE)
        self.img = pygame.transform.rotate(self.init_img, angle)
        self.angle = angle
        self.rect = self.img.get_rect(center=(center_x, center_y))

    def rotate(self, forward=True, speed=2):
        if forward:
            self.angle += speed
        else:
            self.angle -= speed
        self.img = pygame.transform.rotate(self.init_img, self.angle)
        self.rect = self.img.get_rect(center=self.rect.center)

