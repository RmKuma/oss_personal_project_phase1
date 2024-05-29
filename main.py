import pygame
import random
from Box2D import b2World, b2PolygonShape, b2BodyDef, b2_dynamicBody, b2_staticBody

# 게임 설정
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FPS = 60

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Box2D 설정
PPM = 20.0  # pixels per meter
TIME_STEP = 1.0 / FPS
GRAVITY = -10

class WatermelonGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Watermelon Game")
        self.clock = pygame.time.Clock()
        self.world = b2World(gravity=(0, GRAVITY), doSleep=True)
        self.watermelons = []
        self.current_watermelon = None
        self.create_ground()

    def create_ground(self):
        body_def = b2BodyDef()
        body_def.position = (SCREEN_WIDTH / 2 / PPM, 1)
        ground = self.world.CreateBody(body_def)
        ground_shape = b2PolygonShape(box=(SCREEN_WIDTH / 2 / PPM, 1))
        ground.CreateFixture(shape=ground_shape)

    def create_watermelon(self):
        body_def = b2BodyDef()
        body_def.type = b2_dynamicBody
        body_def.position = (SCREEN_WIDTH / 2 / PPM, SCREEN_HEIGHT / PPM)
        watermelon = self.world.CreateBody(body_def)
        shape = b2PolygonShape(box=(0.5, 0.5))
        watermelon.CreateFixture(shape=shape, density=1, friction=0.3)
        self.current_watermelon = watermelon

    def run(self):
        running = True
        watermelon_ready = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and self.current_watermelon and not watermelon_ready:
                        self.watermelons.append(self.current_watermelon)
                        self.current_watermelon = None
                        watermelon_ready = False

            keys = pygame.key.get_pressed()
            if self.current_watermelon and not watermelon_ready:
                if keys[pygame.K_LEFT]:
                    self.current_watermelon.position.x -= 0.2
                if keys[pygame.K_RIGHT]:
                    self.current_watermelon.position.x += 0.2
                if keys[pygame.K_DOWN]:
                    self.current_watermelon.position.y -= 0.2

            if not self.current_watermelon and not watermelon_ready:
                self.create_watermelon()
                watermelon_ready = True

            self.world.Step(TIME_STEP, 10, 10)
            self.screen.fill(WHITE)

            for wm in self.watermelons:
                for fixture in wm.fixtures:
                    shape = fixture.shape
                    vertices = [(wm.transform * v) * PPM for v in shape.vertices]
                    vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]
                    pygame.draw.polygon(self.screen, GREEN, vertices)

            if self.current_watermelon:
                for fixture in self.current_watermelon.fixtures:
                    shape = fixture.shape
                    vertices = [(self.current_watermelon.transform * v) * PPM for v in shape.vertices]
                    vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]
                    pygame.draw.polygon(self.screen, GREEN, vertices)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = WatermelonGame()
    game.run()