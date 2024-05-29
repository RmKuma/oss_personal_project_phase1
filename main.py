import pygame
import random
from Box2D import b2World, b2PolygonShape, b2BodyDef, b2_dynamicBody, b2_staticBody
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody)

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
GRAVITY = -20
FRICTION = 0.0
RESTITUTION = 0.3

GROUND_COLOR = [240,128,128, 255]

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
        watermelon = self.world.CreateDynamicBody(position=(SCREEN_WIDTH / 2 / PPM, SCREEN_HEIGHT / PPM), angle=0)
        watermelon.userData = {}
        watermelon.userData["color"] = (0, 255, 0, 255)  
        watermelon.CreateCircleFixture(radius=2, density=1, friction=FRICTION, restitution=RESTITUTION)
        self.current_watermelon = watermelon  
        self.current_watermelon.awake = False


    def run(self):
        running = True
        watermelon_ready = False
        all_watermelons_moved = True

        while running:

            self.world.Step(TIME_STEP, 10, 10)
            self.screen.fill(WHITE)

            def my_draw_polygon(polygon, body, fixture):
                vertices = [(body.transform * v) * PPM for v in polygon.vertices]
                vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]
                pygame.draw.polygon(self.screen, GROUND_COLOR, vertices)
            polygonShape.draw = my_draw_polygon

            def my_draw_circle(circle, body, fixture):
                position = body.transform * circle.pos * PPM
                position[1] = SCREEN_HEIGHT - position[1]
                pygame.draw.circle(self.screen, body.userData["color"], [int(x) for x in position], int(circle.radius * PPM))
            circleShape.draw = my_draw_circle
            
            for body in self.world.bodies:
                for fixture in body.fixtures:
                    fixture.shape.draw(body, fixture)

            if not self.current_watermelon and not watermelon_ready and all_watermelons_moved:

                self.create_watermelon()
                watermelon_ready = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    print(event.key)
                    if event.key == pygame.K_LEFT and drop == False:
                        self.current_watermelon.position.x -= 0.2
                    if event.key == pygame.K_RIGHT and drop == False:
                        self.current_watermelon.position.x += 0.2
                    if event.key == pygame.K_DOWN and self.current_watermelon and watermelon_ready:
                        print("here")
                        self.current_watermelon.awake = True
                        self.watermelons.append(self.current_watermelon)
                        self.current_watermelon = None
                        watermelon_ready = False
                        drop = True
                        all_watermelons_moved = False


            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = WatermelonGame()
    game.run()