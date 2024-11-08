from model import *


class Scene:
    def __init__(self, app):
        self.rotating_advanced_cube = None
        self.rotating_advanced_cube_2 = None
        self.rotating_cube = None
        self.app = app
        self.objects = []
        self.load()
        self.skybox = AdvancedSkybox(app)

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object

        for x in range(-6, 12, 6):
            add(AdvancedCube(app, pos=(-x, 2, 8), scale=(3, 2, 1), tex_id=100, normal_id=105))
        for z in range(-4, 14, 6):
            add(AdvancedCube(app, pos=(8, 2, -z), scale=(1, 2, 3), tex_id=0, normal_id=5))
        for x in range(-4, 10, 6):
            add(AdvancedCube(app, pos=(-x, 2, -10), scale=(3, 2, 1), tex_id=1, normal_id=6))
        for z in range(-6, 10, 6):
            add(AdvancedCube(app, pos=(-10, 2, -z), scale=(1, 2, 3), tex_id=2, normal_id=7))

        n, s = 80, 2
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                add(AdvancedCube(app, pos=(x, -1, z), tex_id=4, normal_id=5))

        add(Skull(app, pos=(0, 0, 0), scale=(0.1, 0.1, 0.1)))

        add(AdvancedCube(app, pos=(0, 6, 6), scale=(1, 1, 1), tex_id=100, normal_id=105))

        add(Cube(app, pos=(4, 6, 6), scale=(1, 1, 1), tex_id=100))

        self.rotating_advanced_cube = RotatingAdvancedCube(app, pos=(3, 6, 0), scale=(1, 1, 1), tex_id=4, normal_id=9)
        add(self.rotating_advanced_cube)
        self.rotating_cube = RotatingCube(app, pos=(7, 6, 0), scale=(1, 1, 1), tex_id=300)
        add(self.rotating_cube)

    def update(self):
        # Moving objects
        self.rotating_advanced_cube.rot.xyz = self.app.time
        self.rotating_cube.rot.xyz = self.app.time
        pass
