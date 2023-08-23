import sys
import pygame
from scripts import (
    load_image,
    load_images,
    Animation,
    PhysicsEntity,
    Player,
    Clouds,
    Tilemap

)


BASE_IMG_PATH = "data/images/"


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('yo game')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
            'decor': load_images(BASE_IMG_PATH + 'tiles/decor'),
            'grass': load_images(BASE_IMG_PATH + 'tiles/grass'),
            'large_decor': load_images(BASE_IMG_PATH + 'tiles/large_decor'),
            'stone': load_images(BASE_IMG_PATH + 'tiles/stone'),
            'player': load_image(BASE_IMG_PATH + 'tiles/1_player.png'),
            'background': load_image(BASE_IMG_PATH + 'background_resized.png'),
            'clouds': load_images(BASE_IMG_PATH + 'clouds'),
            'player/idle': Animation(load_images(BASE_IMG_PATH + 'entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images(BASE_IMG_PATH + 'entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images(BASE_IMG_PATH + 'entities/player/jump')),
            'player/slide': Animation(load_images(BASE_IMG_PATH + 'entities/player/slide')),
            'player/wall_slide': Animation(load_images(BASE_IMG_PATH + 'entities/player/wall_slide')),
        }

        self.clouds = Clouds(self.assets['clouds'], count=16)

        self.player = Player(self, (50, 50), (8, 15))

        self.tilemap = Tilemap(self, tile_size=16)

        self.scroll = [0, 0]

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centerx - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=self.scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Game().run()
    # print(ImageEditor.resize_image("data/images/background.png", new_size=(320, 240), view_image=True))
