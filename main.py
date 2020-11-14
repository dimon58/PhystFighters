import sys

import pygame
from pygame.draw import rect

from settings import *

pygame.font.init()
pygame.mixer.pre_init()
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class Overlay:
    pass


class App:
    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock = clock
        self.tasks = []

    def draw(self, dt):
        pass

    def run_once(self):
        pass

    def run_tasks(self):
        for task in self.tasks:
            task()

    def run(self):
        self.run_once()
        alive = True
        while alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.run_tasks()
            self.draw(self.clock.get_time() / 1000)
            self.clock.tick()
            pygame.display.set_caption('{:.1f}'.format(self.clock.get_fps()))


class LoadingScreen(App):
    def __init__(self, screen, clock):
        super(LoadingScreen, self).__init__(screen, clock)
        self.BGCOLOR = (100, 100, 254)
        # self.font = pygame.font.Font('19833.otf', SCREEN_HEIGHT // 4)
        print(pygame.font.get_fonts())
        self.font = pygame.font.SysFont('maturascriptcapitals', SCREEN_HEIGHT // 4)
        self.temp = self.font.render('Physt Fighter', False, (0, 0, 255))
        self.rect = self.temp.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.textsurface = pygame.Surface(self.rect.size).convert_alpha()
        self.textsurface.fill(self.BGCOLOR)
        self.textsurface.blit(self.temp, (0, 0))
        self.textsurface.set_colorkey((0, 0, 255))

        self.music = pygame.mixer.Sound('Jojo-s_Bizarre_Adventure_OST_-_Awaken_Pillar_Men_Theme_62681965.mp3')
        self.position = 0
        self.colors = [(212, 6, 6), (238, 156, 0), (227, 255, 0), (6, 191, 0), (0, 26, 152)]
        self.speed = 100
        self.numpolos = 5 * len(self.colors)
        self.lenpolos = 100
        self.lenpolos = SCREEN_WIDTH / (self.numpolos - 1)
        print(self.lenpolos)
        self.tempsurface = pygame.Surface(self.rect.size)

    def run_once(self):
        self.music.play()

    def prepare_text(self):
        """
        Рисую большой полосатый прямоугольник и верчу ео относительно центра
        Жрет фпс очень сильно
        :return:
        """
        # TODO: Переделать. Рисовать параллелограммы
        temp_surface = pygame.Surface(self.rect.size).convert_alpha()
        polosi = pygame.Surface((self.textsurface.get_width(), self.textsurface.get_width()))
        temp_surface.fill((100, 100, 100))
        for polosa in range(self.numpolos):
            rect(polosi, self.colors[polosa % len(self.colors)],
                 ((self.lenpolos * polosa + self.position) % (SCREEN_WIDTH + self.lenpolos) - self.lenpolos, 0,
                  self.lenpolos, polosi.get_height()))
        t = pygame.transform.rotate(polosi, -45)
        temp_surface.blit(t, t.get_rect(center=temp_surface.get_rect().center).topleft)
        temp_surface.blit(self.textsurface, (0, 0))
        return temp_surface

    def draw(self, dt):
        self.screen.fill(self.BGCOLOR)
        self.position += self.speed * dt
        temp = self.prepare_text()
        self.screen.blit(temp, self.rect.topleft)

        pygame.display.update()


loop = LoadingScreen(screen, clock)

loop.run()
