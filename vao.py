from vbo import VBO
from shader_program import ShaderProgram


class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}

        self.vaos['cube'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['cube']
        )
        self.vaos['shadow_cube'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['cube']
        )

        self.vaos['advanced_cube'] = self.get_vao(
            program=self.program.programs['enhanced'],
            vbo=self.vbo.vbos['advanced_cube']
        )
        self.vaos['shadow_advanced_cube'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['cube']
        )

        self.vaos['skull'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['skull']
        )

        self.vaos['shadow_skull'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['skull']
        )
        self.vaos['skybox'] = self.get_vao(
            program=self.program.programs['skybox'],
            vbo=self.vbo.vbos['skybox']
        )
        self.vaos['advanced_skybox'] = self.get_vao(
            program=self.program.programs['advanced_skybox'],
            vbo=self.vbo.vbos['advanced_skybox']
        )
        self.vaos['basic_post_processing'] = self.get_vao(
            program=self.program.programs['basic_post_processing'],  # Post-processing shader program
            vbo=self.vbo.vbos['basic_post_processing']  # Fullscreen quad VBO
        )

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attrib)], skip_errors=True)
        return vao

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()
