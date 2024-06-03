import pygame
import random
from Box2D import b2World, b2PolygonShape, b2BodyDef, b2_dynamicBody, b2_staticBody, b2ContactListener
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
RESTITUTION = 0.4

CURSOR_BOUNDARY = 2
CURSOR_MIN = 0 + CURSOR_BOUNDARY
CURSOR_MAX = SCREEN_WIDTH // PPM - CURSOR_BOUNDARY

GROUND_COLOR = [240,128,128, 255]


MELONS = [  [0, [255,0,0], 0.7],
            [1, [255,0,0], 1.2],
            [2, [200,100,0], 1.9],
            [3, [0,0,200], 2.7],
            [4, [255,99,7], 3.8],   
            [5, [127,255,212], 5],  
            [6, [0,191,255], 7.2],  
            [7, [65,105,225], 9],  
            [8, [238,130,238], 11],         ]

class ContactListener(b2ContactListener):
    def __init__(self):
        b2ContactListener.__init__(self)
        self.collisions = []
        self.to_destroy = []

    def BeginContact(self, contact):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body
        if bodyA.userData["type"] != "wall" and bodyB.userData["type"] != "wall":
            if bodyA.userData["level"] == bodyB.userData["level"]:
                self.to_destroy.append([bodyA, bodyB])

class WatermelonGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Watermelon Game")
        self.clock = pygame.time.Clock()
        self.world = b2World(gravity=(0, GRAVITY))
        self.contact_listener = ContactListener()
        self.world.contactListener = self.contact_listener
        self.watermelons = []
        self.before_positions = None
        self.cursor = [SCREEN_WIDTH / 2 / PPM, SCREEN_HEIGHT / PPM - 2]
        self.create_ground()

    def create_ground(self):
        body_def = b2BodyDef()
        body_def.position = (SCREEN_WIDTH//(PPM * 2), 1)
        ground = self.world.CreateBody(body_def)
        ground.userData = {}
        ground.userData["type"] = "wall"
        ground_shape = b2PolygonShape(box= (SCREEN_WIDTH//(PPM * 2), 1))
        ground.CreateFixture(shape=ground_shape, friction=FRICTION, restitution=RESTITUTION)

        # Left        
        body_def = b2BodyDef()
        body_def.position = (0, SCREEN_HEIGHT // (PPM * 2))
        ground = self.world.CreateBody(body_def)
        ground.userData = {}
        ground.userData["type"] = "wall"
        ground_shape = b2PolygonShape(box= (1, SCREEN_HEIGHT // (PPM * 2)))
        ground.CreateFixture(shape=ground_shape, friction=FRICTION, restitution=RESTITUTION)

        # Right
        body_def = b2BodyDef()
        body_def.position = (SCREEN_WIDTH // PPM, SCREEN_HEIGHT // (PPM * 2))
        ground = self.world.CreateBody(body_def)
        ground.userData = {}
        ground.userData["type"] = "wall"
        ground_shape = b2PolygonShape(box= (1, SCREEN_HEIGHT // (PPM * 2)))
        ground.CreateFixture(shape=ground_shape, friction=FRICTION, restitution=RESTITUTION)


    def create_watermelon(self, position=(SCREEN_WIDTH / 2 / PPM, SCREEN_HEIGHT / PPM), level=1):
        watermelon = self.world.CreateDynamicBody(position=position, angle=0)
        watermelon.userData = {}
        watermelon.userData["type"] = "Fruit"
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
    
    # 커서가 화면 밖으로 나가는 것을 방지하는 함수
    def change_cursor_position(self, val):
        if self.cursor[0] + val < CURSOR_MAX and self.cursor[0] + val > CURSOR_MIN:
            self.cursor[0] += val

    def draw_dotted_line(self, start_pos, end_pos, color, width=3, dash_length=1 * PPM):
        x1, y1 = start_pos[0] * PPM, start_pos[1] * PPM
        x2, y2 = end_pos[0] * PPM, end_pos[1] * PPM
        
        distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5 
        dashes = int(distance / dash_length)
        
        for i in range(dashes):
            print(i)
            start = (x1 + (x2 - x1) * i / dashes , y1 + (y2 - y1) * i / dashes )
            end = (x1 + (x2 - x1) * (i + 0.5) / dashes , y1 + (y2 - y1) * (i + 0.5) / dashes )
            pygame.draw.line(self.screen, color, start, end, width)


    def run(self):

        # pygame에 box2d 오브젝트들을 draw하는 함수
        def my_draw_polygon(polygon, body, fixture):
            vertices = [(body.transform * v) * PPM for v in polygon.vertices]
            vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]
            pygame.draw.polygon(self.screen, GROUND_COLOR, vertices)

        def my_draw_circle(circle, body, fixture):
            position = body.transform * circle.pos * PPM
            position[1] = SCREEN_HEIGHT - position[1]
            pygame.draw.circle(self.screen, body.userData["color"], [int(x) for x in position], int(circle.radius * PPM))
            
        polygonShape.draw = my_draw_polygon
        circleShape.draw = my_draw_circle
            
        running = True
        self.phase = "aim"
        _level = random.randint(0,2)

        while running: 
            self.world.Step(TIME_STEP, 10, 10)
            self.screen.fill(WHITE)
            
            for body in self.world.bodies:
                for fixture in body.fixtures:
                    fixture.shape.draw(body, fixture)

            # 동일 레벨의 두 과일이 부딪힌 경우 ->  더 높은 레벨의 과일을 중간 위치에 생성
            while len(self.contact_listener.to_destroy) != 0:
                _tmp = self.contact_listener.to_destroy[-1]
                self.contact_listener.to_destroy.pop()

                new_level = _tmp[0].userData["level"] + 1
                new_pos = ((_tmp[0].position.x + _tmp[1].position.x) / 2, (_tmp[0].position.y + _tmp[1].position.y) / 2)
                self.world.DestroyBody(_tmp[0])
                self.world.DestroyBody(_tmp[1])
                self.watermelons.append(self.create_watermelon(new_pos, new_level))
                self.before_positions = [melon.position for melon in self.watermelons]

            ### 조준 phase ###
            if self.phase == "aim":
                # 과일 표시
                pygame.draw.circle(self.screen, MELONS[_level][1], [int(self.cursor[0] * PPM), int( SCREEN_HEIGHT - (self.cursor[1] * PPM)) ], int(MELONS[_level][2] * PPM))
                # 조준선 표시
                self.draw_dotted_line((self.cursor[0], self.cursor[1]-35), (self.cursor[0], self.cursor[1]), (255, 181, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        print(event.key)
                        if event.key == pygame.K_LEFT:
                            self.change_cursor_position(-0.3)
                        if event.key == pygame.K_RIGHT:
                            self.change_cursor_position(0.3)
                        if event.key == pygame.K_DOWN:
                            print(len(self.watermelons))
                            self.watermelons.append(self.create_watermelon(self.cursor, _level))

                            # Drop phase 로 변경
                            self.phase = "drop"
                            self.before_positions = [melon.position for melon in self.watermelons]

                # 키를 꾹 누르는 경우 인식
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.change_cursor_position(-0.3)
                if keys[pygame.K_RIGHT]:
                    self.change_cursor_position(0.3)

            ### Drop phase : 수박이 떨어지는 phase
            elif self.phase == "drop":
                if self.check_all_melons_stop():
                    self.phase = "aim"
                    _level = random.randint(0,2)
            
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    game = WatermelonGame()
    game.run()