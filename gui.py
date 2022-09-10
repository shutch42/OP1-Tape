import pygame
from reel import Reel


class GUI:
    SCREEN_SIZE = WIDTH, HEIGHT = 800, 480
    ICON_SIZE = 50, 50
    GRAY = 120, 120, 120
    WHITE = 255, 255, 255

    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        # self.screen = pygame.display.set_mode(self.SCREEN_SIZE, pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)

        self.background = pygame.Surface(self.screen.get_size())

        self.play_icon = pygame.transform.smoothscale(pygame.image.load("img/play.png").convert_alpha(),
                                                      self.ICON_SIZE)

        self.reverse_icon = pygame.transform.smoothscale(pygame.image.load("img/reverse.png").convert_alpha(),
                                                         self.ICON_SIZE)

        self.record_icon = pygame.transform.smoothscale(pygame.image.load("img/record.png").convert_alpha(),
                                                        self.ICON_SIZE)

        self.ff_icon = pygame.transform.smoothscale(pygame.image.load("img/fast-forward.png").convert_alpha(),
                                                    self.ICON_SIZE)

        self.rw_icon = pygame.transform.smoothscale(pygame.image.load("img/rewind.png").convert_alpha(),
                                                    self.ICON_SIZE)

        self.icon_rect = self.play_icon.get_rect(center=(400, 200))

        self.mono_font = pygame.font.Font("fonts/FreeMonoBold.ttf", 34)
        self.clock_text = self.mono_font.render("00:00:00", True, self.WHITE, self.GRAY)
        self.clock_rect = self.clock_text.get_rect(center=(400, 50))

        self.reel1 = Reel(200, 170, 0)
        self.reel2 = Reel(600, 170, 45)

    def clear_screen(self):
        self.background.fill(self.GRAY)

    def rotate_reels(self, forward, high_speed):
        if high_speed:
            speed = 4
        else:
            speed = 2
        self.reel1.rotate(forward, speed)
        self.reel2.rotate(forward, speed)

    def _render_reels(self):
        self.background.blit(self.reel1.img, self.reel1.rect)
        self.background.blit(self.reel2.img, self.reel2.rect)

    def update_clock(self, time):
        self.clock_text = self.mono_font.render(time, True, self.WHITE, self.GRAY)

    def _render_clock(self):
        self.background.blit(self.clock_text, self.clock_rect)

    def render_play(self):
        self.rotate_reels(forward=True, high_speed=False)
        self.background.blit(self.play_icon, self.icon_rect)
        self._render_clock()
        self._render_reels()

    def render_pause(self):
        self._render_clock()
        self._render_reels()

    def render_record(self):
        self.rotate_reels(forward=True, high_speed=False)
        self.background.blit(self.record_icon, self.icon_rect)
        self._render_clock()
        self._render_reels()

    def render_record_reverse(self):
        self.rotate_reels(forward=False, high_speed=False)
        self.background.blit(self.record_icon, self.icon_rect)
        self._render_clock()
        self._render_reels()

    def render_arm_record(self):
        self.background.blit(self.record_icon, self.icon_rect)
        self._render_clock()
        self._render_reels()

    def render_ff(self):
        self.rotate_reels(forward=True, high_speed=True)
        self.background.blit(self.ff_icon, self.icon_rect)
        self._render_clock()
        self._render_reels()

    def render_rw(self):
        self.rotate_reels(forward=False, high_speed=True)
        self.background.blit(self.rw_icon, self.icon_rect)
        self._render_clock()
        self._render_reels()

    def render_reverse(self):
        self.rotate_reels(forward=False, high_speed=False)
        self.background.blit(self.reverse_icon, self.icon_rect)
        self._render_clock()
        self._render_reels()

    def display(self):
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

