import glm


class Light:
    def __init__(self, position=(20, 60, -50), color=(1, 1, 1)):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)
        self.direction = glm.vec3(0, 0, 0)

        self.ambient_light = 0.1 * self.color
        self.diffuse_light = 0.9 * self.color
        self.specular_light = 1.0 * self.color

        self.m_view_light = self.get_view_matrix()

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.direction, glm.vec3(0, 1, 0))
