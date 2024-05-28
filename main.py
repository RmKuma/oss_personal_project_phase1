import numpy as np
from PIL import Image
from gym import spaces
from gym.utils import seeding
import sys, math, random, tqdm, os, gym, pygame, Box2D
from Box2D.b2 import (world, polygonShape, circleShape, staticBody, dynamicBody)



class Elastic2D(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 60
    }

    def __init__(self, **kwargs):
        self._seed()

        pygame.display.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)  # size, flags, depth
        self.screen.fill((0, 0, 0, 0))
        pygame.display.set_caption('Simple pygame example')
        self.clock = pygame.time.Clock()
        self.world = world(gravity=(0,0))
        
        self.walls = None
        self.objects = None

        self.colors = kwargs['colors']
        self.numofobjs =  kwargs['numofobjs']
        self.objs = kwargs['objs']
        self.sizes = kwargs['sizes']

        # Defin Draw Functions
        def my_draw_polygon(polygon, body, fixture):
            vertices = [(body.transform * v) * PPM for v in polygon.vertices]
            vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]
            pygame.draw.polygon(self.screen, body.userData["color"], vertices)
        polygonShape.draw = my_draw_polygon

        def my_draw_circle(circle, body, fixture):
            position = body.transform * circle.pos * PPM
            position[1] = SCREEN_HEIGHT - position[1]
            pygame.draw.circle(self.screen, body.userData["color"], [int(x) for x in position], int(circle.radius * PPM))
        circleShape.draw = my_draw_circle

        # GYM attributes
        high = np.array([np.inf] * 8)  
        self.observation_space = spaces.Box(-high, high)
        self.action_space = spaces.Discrete(17)

        self.reset()

    def _seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _destroy(self):
        if not self.walls: return

        for wall in self.walls:
            self.world.DestroyBody(wall)
        self.walls = None

        for obj in self.objects:
            self.world.DestroyBody(obj)
        self.objects = None

    def get_random_position_and_angle(self, obj_positions):
        sqrt2 = 1.414215

        while True:
            angle = random.random() * 3.1415
            size = random.randint(self.sizes[0], self.sizes[1])
            min_x, min_y = int(sqrt2 * size + 2), int(sqrt2 * size + 2) 
            max_x, max_y = int((SCREEN_WIDTH // PPM) - sqrt2 * size - 1), int((SCREEN_HEIGHT // PPM) - sqrt2 * size - 1)
            x_candidate, y_candidate= random.randint(min_x, max_x), random.randint(min_y, max_y)
        
            overlapped = False
            for obj_pos in obj_positions:
                if (x_candidate - obj_pos[0])**2 + (y_candidate - obj_pos[1])**2 < 8:
                    overlapped = True
            if not overlapped:
                break
        return  (x_candidate, y_candidate), angle, size
    
    def get_object_infos(self):
        _tmp = []
        for body in self.world.bodies:
            if body.userData["shape"] != "wall":
                _tmp.append(self.objs.index(body.userData["shape"]))
        return np.array(_tmp, dtype=np.int32)

    def reset(self):
        while True: 
            self._destroy()
            
            # create walls for boudary
            self.walls = []
            for pos, size in WALLS:
                self.walls.append(self.world.CreateStaticBody(position=pos, shapes=polygonShape(box=size)))
            for wall in self.walls:
                wall.userData = {}
                wall.userData["color"] = (255, 255, 255, 255)    
                wall.userData["shape"] = 'wall'
            
            # create various objects 
            self.objects = []
            obj_pos = []
            shapes = []
            for idx in range(self.numofobjs):
                while True:
                    obj = random.choice(self.objs)
                    if obj not in shapes:
                        break
                shapes.append(obj)

                pos, angle, size = self.get_random_position_and_angle(obj_pos)
                obj_pos.append(pos)
                temp_body = self.world.CreateDynamicBody(position=pos, angle=angle)
                temp_body.userData = {}
                temp_body.userData["shape"] = obj
                temp_body.userData["size"] = size
                if len(self.objects) == 0:
                    #temp_body.userData["color"] = (255, 0, 0, 255)  
                    temp_body.userData["color"] = (0, 255, 0, 255)  
                else:
                    temp_body.userData["color"] = random.choice(self.colors)

                if obj == "square":
                    temp_fixture = temp_body.CreatePolygonFixture(box=(size*3/4, size*3/4), density=1, friction=FRICTION, restitution=RESTITUTION)
                elif obj == "rectangle":
                    temp_fixture = temp_body.CreatePolygonFixture(box=(size, size/2), density=1, friction=FRICTION, restitution=RESTITUTION)
                elif obj == "triangle":
                    temp_fixture = temp_body.CreatePolygonFixture(shape=polygonShape(vertices=[(x*size , y*size) for (x, y) in TRIANGLE_POLY]),
                                density=1, friction=FRICTION, restitution=RESTITUTION)
                elif obj == "righttri1":
                    temp_fixture = temp_body.CreatePolygonFixture(shape=polygonShape(vertices=[(x*size , y*size) for (x, y) in RIGHT_TRAINBLE_POLY1]),
                                density=1, friction=FRICTION, restitution=RESTITUTION)
                elif obj == "righttri2":
                    temp_fixture = temp_body.CreatePolygonFixture(shape=polygonShape(vertices=[(x*size , y*size) for (x, y) in RIGHT_TRAINBLE_POLY2]),
                                density=1, friction=FRICTION, restitution=RESTITUTION)
                elif obj == "hexagon":
                    temp_fixture = temp_body.CreatePolygonFixture(shape=polygonShape(vertices=[(x*size , y*size) for (x, y) in HEXAGON_POLY]),
                                density=1, friction=FRICTION, restitution=RESTITUTION)
                elif obj == "cross":
                    temp_fixture = temp_body.CreatePolygonFixture(shape=polygonShape(vertices=[(x*size , y*size) for (x, y) in CROSS_POLY_PART1]),
                                density=1, friction=FRICTION, restitution=RESTITUTION)
                    temp_fixture = temp_body.CreatePolygonFixture(shape=polygonShape(vertices=[(x*size , y*size) for (x, y) in CROSS_POLY_PART2]),
                                density=1, friction=FRICTION, restitution=RESTITUTION)
                elif obj == "isotri1":
                    temp_fixture = temp_body.CreatePolygonFixture(shape=polygonShape(vertices=[(x*size , y*size) for (x, y) in ISO_TRIANGLE_POLY1]),
                                density=1, friction=FRICTION, restitution=RESTITUTION)
                elif obj == "isotri2":
                    temp_fixture = temp_body.CreatePolygonFixture(shape=polygonShape(vertices=[(x*size , y*size) for (x, y) in ISO_TRIANGLE_POLY2]),
                                density=1, friction=FRICTION, restitution=RESTITUTION)
                elif obj == "diamond":
                    temp_fixture = temp_body.CreatePolygonFixture(shape=polygonShape(vertices=[(x*size , y*size) for (x, y) in DIAMOND_POLY]),
                                density=1, friction=FRICTION, restitution=RESTITUTION)
                elif obj == "halfsquaretriangle":
                    temp_fixture = temp_body.CreatePolygonFixture(shape=polygonShape(vertices=[(x*size , y*size) for (x, y) in HAFL_SQUARE_TIRANGLE_POLY]),
                                density=1, friction=FRICTION, restitution=RESTITUTION)
                elif obj == "trapezoid":
                    temp_fixture = temp_body.CreatePolygonFixture(shape=polygonShape(vertices=[(x*size , y*size) for (x, y) in TRAPEZOID_POLY]),
                                density=1, friction=FRICTION, restitution=RESTITUTION)
                
                
                elif obj == "mixed1":
                    for sub_obj in MIXED1_POLY:
                        temp_fixture = temp_body.CreatePolygonFixture(
                            shape=polygonShape(vertices=[(x*size*0.9 , y*size*0.9) for (x, y) in sub_obj]),
                            density=1, friction=FRICTION, restitution=RESTITUTION)
                
                elif obj == "mixed2":
                    for sub_obj in MIXED2_POLY:
                        temp_fixture = temp_body.CreatePolygonFixture(
                            shape=polygonShape(vertices=[(x*size*0.9 , y*size*0.9) for (x, y) in sub_obj]),
                            density=1, friction=FRICTION, restitution=RESTITUTION)

                elif obj == "mixed3":
                    for sub_obj in MIXED3_POLY:
                        temp_fixture = temp_body.CreatePolygonFixture(
                            shape=polygonShape(vertices=[(x*size*0.9 , y*size*0.9) for (x, y) in sub_obj]),
                            density=1, friction=FRICTION, restitution=RESTITUTION)

                else:   # circle
                    temp_fixture = temp_body.CreateCircleFixture(radius=size, density=1, friction=FRICTION, restitution=RESTITUTION)
                                
                self.objects.append(temp_body)

            # Ensure all objects are existed in boundary walls 
            object_disappeared = False
            for obj in self.world.bodies:
                if not (obj.userData["shape"] == "wall"):
                    if not (1 < obj.position[0] < ((SCREEN_WIDTH // PPM) - 1) and 1 < obj.position[1] < ((SCREEN_HEIGHT // PPM) - 1)):
                        object_disappeared = True
            if not object_disappeared:  break

        for i in range(1000):
            self.world.Step(TIME_STEP, 6, 2)

        return self.render(mode="rgb_array")

    def get_one_frame_data(self):
        pygame.display.flip()
        self.clock.tick(TARGET_FPS)
        self.screen.fill((0,0,0,0))
        for body in self.world.bodies:
            for fixture in body.fixtures:
                fixture.shape.draw(body, fixture)
        img = self.render(mode="rgb_array")

        datas = np.zeros((self.numofobjs * 4))
        obj = 0
        for body in self.world.bodies:
            if body.userData["shape"] != "wall":
                datas[obj * 4] = (body.transform.angle + PI)/(PI * 2)
                datas[obj * 4 + 1] = body.transform.position.x / (SCREEN_WIDTH//PPM)
                datas[obj * 4 + 2] = body.transform.position.y / (SCREEN_HEIGHT//PPM)
                datas[obj * 4 + 3] = body.userData["size"]/ 5
                obj += 1
        
        return img, datas

    def step(self, action):
        
        imgs = []
        datas = []

        img, data = self.get_one_frame_data()
        imgs.append(img)
        datas.append(data)

        self.objects[0].ApplyForceToCenter([int(action[0]*POWER), int(action[1] * POWER)], True)
        
        for i in range(24):
            for _ in range(1):
                self.world.Step(TIME_STEP, 10, 10)            
            img, data = self.get_one_frame_data()
            imgs.append(img)
            datas.append(data)

        # Stop all objects
        for body in self.world.bodies:
            body.linearVelocity = (0., 0.)
            body.angularVelocity = 0.

        reward = 0
        done = False
        return imgs, reward, done, {"datas":datas}

    def render(self, mode='human', close=False):
        if mode == "sensor":
            datas = np.zeros((self.numofobjs * 4))
            obj = 0
            for body in self.world.bodies:
                if body.userData["shape"] != "wall":
                    datas[obj * 4] = (body.transform.angle + PI)/(PI * 2)
                    datas[obj * 4 + 1] = body.transform.position.x / (SCREEN_WIDTH//PPM)
                    datas[obj * 4 + 2] = body.transform.position.y / (SCREEN_HEIGHT//PPM)
                    datas[obj * 4 + 3] = body.userData["size"]/ 5
                    obj += 1
            return datas
        else:
            string_image = pygame.image.tostring(self.screen, 'RGB')
            temp_surf = pygame.image.fromstring(string_image,(SCREEN_WIDTH, SCREEN_HEIGHT),'RGB' )
            img_arr = pygame.surfarray.array3d(temp_surf).swapaxes(0,1)
            return img_arr

