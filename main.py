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
PPM = 20.0 / (640 // SCREEN_WIDTH) # pixels per meter
TIME_STEP = 1.0 / FPS
GRAVITY = -20
FRICTION = 0.5
RESTITUTION = 0.3

GROUND_COLOR = [240,128,128, 255]


MELONS = [  [0, [255,0,0], 0.3],
            [1, [255,0,0], 0.5],
            [2, [200,100,0], 0.8],
            [3, [0,0,200], 1.2],
            [4, [0,255,0], 2],          ]

class WatermelonGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Watermelon Game")
        self.clock = pygame.time.Clock()
        self.world = b2World(gravity=(0, GRAVITY))
        self.watermelons = []
        self.before_positions = None
        self.current_watermelon = None
        self.create_ground()

    def create_ground(self):
        body_def = b2BodyDef()
        body_def.position = (SCREEN_WIDTH//(PPM * 2), 1)
        ground = self.world.CreateBody(body_def)
        ground_shape = b2PolygonShape(box= (SCREEN_WIDTH//(PPM * 2), 1))
        ground.CreateFixture(shape=ground_shape, friction=FRICTION, restitution=RESTITUTION)

        # Left        
        body_def = b2BodyDef()
        body_def.position = (0, SCREEN_HEIGHT // (PPM * 2))
        ground = self.world.CreateBody(body_def)
        ground_shape = b2PolygonShape(box= (1, SCREEN_HEIGHT // (PPM * 2)))
        ground.CreateFixture(shape=ground_shape, friction=FRICTION, restitution=RESTITUTION)

        # Right
        body_def = b2BodyDef()
        body_def.position = (SCREEN_WIDTH // PPM, SCREEN_HEIGHT // (PPM * 2))
        ground = self.world.CreateBody(body_def)
        ground_shape = b2PolygonShape(box= (1, SCREEN_HEIGHT // (PPM * 2)))
        ground.CreateFixture(shape=ground_shape, friction=FRICTION, restitution=RESTITUTION)


    def create_watermelon(self, position=(SCREEN_WIDTH / 2 / PPM, SCREEN_HEIGHT / PPM), level=1):
        watermelon = self.world.CreateDynamicBody(position=position, angle=0)
        watermelon.userData = {}
        watermelon.userData["level"] = level
        watermelon.userData["color"] = MELONS[level][1]
        watermelon.CreateCircleFixture(radius=MELONS[level][2], density=1, friction=FRICTION, restitution=RESTITUTION)
        return watermelon


    def check_all_melons_stop(self):
        check = True
        cur_positions = [melon.position for melon in self.watermelons]
        for i in range(len(cur_positions)):
            if abs(cur_positions[i].x - self.before_positions[i].x) > 0.7 or  abs(cur_positions[i].y - self.before_positions[i].y) > 0.7:
                check = False
        return check


    def run(self):

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
            
        running = True
        current_watermelon = None
        self.phase = "aim"
        _pos = [SCREEN_WIDTH / 2 / PPM, SCREEN_HEIGHT / PPM - 2]
        _level = random.randint(0,2)


        while running: 
            self.world.Step(TIME_STEP, 10, 10)
            self.screen.fill(WHITE)

            for body in self.world.bodies:
                for fixture in body.fixtures:
                    fixture.shape.draw(body, fixture)

            ### 조준 phase ###
            if self.phase == "aim":
                pygame.draw.circle(self.screen, MELONS[_level][1], [int(_pos[0] * PPM), int( SCREEN_HEIGHT - (_pos[1] * PPM)) ], int(MELONS[_level][2] * PPM))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        print(event.key)
                        if event.key == pygame.K_LEFT:
                            _pos[0] -= 0.3
                        if event.key == pygame.K_RIGHT:
                            _pos[0] += 0.3
                        if event.key == pygame.K_DOWN:
                            print(len(self.watermelons))
                            current_watermelon = self.create_watermelon(_pos, _level)
                            self.watermelons.append(current_watermelon)

                            # go to drop phase
                            self.phase = "drop"
                            self.before_positions = [melon.position for melon in self.watermelons]

            elif self.phase == "drop":
                if self.check_all_melons_stop():
                    self.phase = "aim"
                    _pos = [SCREEN_WIDTH / 2 / PPM, SCREEN_HEIGHT / PPM - 2]
                    _level = random.randint(0,2)
                pass
            
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = WatermelonGame()
    game.run()