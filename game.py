import random
import sys
import pygame
import math
from scripts import (
    load_image,
    load_images,
    Animation,
    PhysicsEntity,
    Player,
    Clouds,
    Tilemap,
    particles_module
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

        # Initialize the scroll attribute
        self.scroll = [0, 0]

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
            'particle/leaf': Animation(load_images(BASE_IMG_PATH + 'particles/leaf'), img_dur=20, loop=False),
            'particle/particle': Animation(load_images(BASE_IMG_PATH + 'particles/particle'), img_dur=6, loop=False),
        }

        self.clouds = Clouds(self.assets['clouds'], count=16)

        self.player = Player(self, (50, 50), (8, 15))

        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load('scripts/map.json')

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            else:
                print(spawner['pos'], 'enemy')

        self.particles = []

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    # Use the Particle class from the updated import
                    self.particles.append(particles_module.Particle(self, 'particle', pos, velocity=[-0.1, 0.3],
                                                                    frame=random.randint(0, 20)))
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.player.jump()
                    if event.key == pygame.K_x:
                        self.player.dash()
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
