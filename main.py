import pygame
import moderngl
import sys
from model import *
from camera import Camera
from lighting import Light
from mesh import Mesh
from scene import Scene
from scene_renderer import SceneRenderer
from vao import VAO  # Import VAO class
from texture import Texture


class GraphicsEngine:
    def __init__(self, win_size=(1600, 900)):
        pygame.init()

        self.WIN_SIZE = win_size

        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

        pygame.display.set_mode(self.WIN_SIZE, flags=pygame.OPENGL | pygame.DOUBLEBUF)

        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)

        self.ctx = moderngl.create_context()
        self.ctx.enable(flags=moderngl.DEPTH_TEST | moderngl.CULL_FACE)

        self.clock = pygame.time.Clock()

        self.time = 0
        self.delta_time = 0

        self.light = Light()

        self.camera = Camera(self)

        self.mesh = Mesh(self)

        self.texture = Texture(self)  # Ensure Texture class is initialized

        self.vaos = VAO(self.ctx)  # Initialize VAO here

        self.scene = Scene(self)

        self.scene_renderer = SceneRenderer(self)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.mesh.destroy()
                self.scene_renderer.destroy()
                pygame.quit()
                sys.exit()

    def render(self):
        # Clear the screen
        self.ctx.clear(color=(0.18, 0.28, 0.28, 1.0))

        # Call the scene renderer to handle rendering
        self.scene_renderer.render()

        # Flip the display buffers
        pygame.display.flip()

    def get_time(self):
        # Get the current time in seconds
        self.time = pygame.time.get_ticks() * 0.001

    def run(self):
        # Main loop
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)


if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()
