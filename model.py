import numpy
import glm
import numpy as np


class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        self.app = app
        self.pos = pos
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera
        self.vao_name = vao_name

    def update(self): ...

    def get_model_matrix(self):
        m_model = glm.mat4()
        m_model = glm.translate(m_model, self.pos)

        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 0, 1))

        m_model = glm.scale(m_model, self.scale)

        return m_model

    def render(self):
        self.update()
        self.vao.render()


class ExtendedBaseModel(BaseModel):
    def __init__(self, app, vao_name, tex_id, pos, rot, scale):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.depth_texture = None
        self.shadow_vao = None
        self.shadow_program = None
        self.texture = None
        self.on_init()

    def update(self):
        self.texture.use(location=0)
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def update_shadow(self):
        self.shadow_program['m_model'].write(self.m_model)

    def render_shadow(self):
        self.update_shadow()
        self.shadow_vao.render()

    def on_init(self):
        self.program['m_view_light'].write(self.app.light.m_view_light)

        self.program['u_resolution'].write(glm.vec2(self.app.WIN_SIZE))

        self.depth_texture = self.app.mesh.texture.textures['depth_texture']
        self.program['shadowMap'] = 1
        self.depth_texture.use(location=1)

        self.shadow_vao = self.app.mesh.vao.vaos['shadow_' + self.vao_name]
        self.shadow_program = self.shadow_vao.program
        self.shadow_program['m_proj'].write(self.camera.m_proj)
        self.shadow_program['m_view_light'].write(self.app.light.m_view_light)
        self.shadow_program['m_model'].write(self.m_model)

        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use(location=0)

        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

        self.program['light.position'].write(self.app.light.position)
        self.program['light.ambient'].write(self.app.light.ambient_light)
        self.program['light.diffuse'].write(self.app.light.diffuse_light)
        self.program['light.specular'].write(self.app.light.specular_light)


class Cube(ExtendedBaseModel):
    def __init__(self, app, vao_name='cube', tex_id=0, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)


class RotatingCube(Cube):
    def __init__(self, app, vao_name='cube', tex_id=0, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)

    def update(self):
        self.m_model = self.get_model_matrix()
        super().update()


class AdvancedCube(Cube):
    def __init__(self, app, vao_name='advanced_cube', tex_id=4, normal_id=9, pos=(0, 0, 0), rot=(0, 0, 0),
                 scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()
        self.normal_id = normal_id
        self.normal_texture = self.app.mesh.texture.textures[self.normal_id]
        self.program['u_normal_0'] = 2
        self.normal_texture.use(location=2)

        self.ao_id = normal_id + 5
        self.ao_texture = self.app.mesh.texture.textures[self.ao_id]
        self.program['u_ao_0'] = 3
        self.ao_texture.use(location=3)

        self.smoothness_id = normal_id + 10
        self.smoothness_texture = self.app.mesh.texture.textures[self.smoothness_id]
        self.program['u_smoothness_0'] = 4
        self.smoothness_texture.use(location=4)

        self.metallic_id = normal_id + 15
        self.metallic_texture = self.app.mesh.texture.textures[self.metallic_id]
        self.program['u_metallic_0'] = 5
        self.metallic_texture.use(location=5)

        self.height_id = normal_id + 20
        self.height_texture = self.app.mesh.texture.textures[self.height_id]
        self.program['u_height_0'] = 6
        self.height_texture.use(location=6)

    def render(self):
        self.update()

        # Write texture units to the shader program
        self.program['u_texture_0'] = 0
        self.program['u_normal_0'] = 2
        self.program['u_ao_0'] = 3
        self.program['u_smoothness_0'] = 4
        self.program['u_metallic_0'] = 5
        self.program['u_height_0'] = 6

        # Bind the textures to the appropriate texture units
        self.texture.use(location=0)
        self.normal_texture.use(location=2)
        self.ao_texture.use(location=3)
        self.smoothness_texture.use(location=4)
        self.metallic_texture.use(location=5)
        self.height_texture.use(location=6)

        # Render the VAO
        self.vao.render()


class RotatingAdvancedCube(AdvancedCube):
    def __init__(self, app, vao_name='advanced_cube', tex_id=4, normal_id=9, pos=(0, 0, 0), rot=(0, 0, 0),
                 scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, normal_id, pos, rot, scale)

    def update(self):
        self.m_model = self.get_model_matrix()
        super().update()


class Skull(ExtendedBaseModel):
    def __init__(self, app, vao_name='skull', tex_id='skull', pos=(0, 0, 0), rot=(-90, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)


class Skybox(BaseModel):
    def __init__(self, app, vao_name='skybox', tex_id='skybox', pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.texture = None
        self.on_init()

    def update(self):
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))

    def on_init(self):
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)

        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))


class AdvancedSkybox(BaseModel):
    def __init__(self, app, vao_name='advanced_skybox', tex_id='skybox', pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.texture = None
        self.on_init()

    def update(self):
        m_view = glm.mat4(glm.mat3(self.camera.m_view))
        self.program['m_invProjView'].write(glm.inverse(self.camera.m_proj * m_view))

    def on_init(self):
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)
