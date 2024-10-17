from model import *


class Scene:
    def __init__(self, app):
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
            add(Cube(app, pos=(-x, 2, 8), scale=(3, 2, 1)))
        for z in range(-4, 14, 6):
            add(Cube(app, pos=(8, 2, -z), scale=(1, 2, 3)))
        for x in range(-4, 10, 6):
            add(Cube(app, pos=(-x, 2, -10), scale=(3, 2, 1)))
        for z in range(-6, 10, 6):
            add(Cube(app, pos=(-10, 2, -z), scale=(1, 2, 3)))

        n, s = 10, 2
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                add(Cube(app, pos=(x, -1, z)))
        add(Skull(app, pos=(0, 0, 0), scale=(0.1, 0.1, 0.1)))

    def update(self):
        # Moving objects
        pass