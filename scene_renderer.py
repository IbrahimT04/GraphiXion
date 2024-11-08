import moderngl


class SceneRenderer:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.mesh = app.mesh
        self.scene = app.scene

        # Frame buffer setup for post-processing and shadows
        self.depth_texture = self.mesh.texture.textures['depth_texture']
        self.color_texture = self.mesh.texture.textures['color_texture']

        self.color_fbo = self.ctx.framebuffer(
            color_attachments=[self.color_texture],
            depth_attachment=self.depth_texture
        )

        self.depth_fbo = self.ctx.framebuffer(
            depth_attachment=self.depth_texture
        )
        self.post_processing_vao = self.app.mesh.vao.vaos['basic_post_processing']
        self.post_processing_program = self.post_processing_vao.program

    def render_shadow(self):
        self.depth_fbo.clear()
        self.depth_fbo.use()

        # Temp
        # self.app.ctx.screen.use()  # Switch to default frame buffer (screen)
        # self.app.ctx.clear()  # Clear the screen

        for obj in self.scene.objects:
            obj.render_shadow()

    def main_render(self):
        # self.color_fbo.use()
        # self.color_fbo.clear()

        # Temp
        self.app.ctx.screen.use()  # Switch to default frame buffer (screen)
        self.app.ctx.clear()  # Clear the screen

        for obj in self.scene.objects:
            obj.render()
        self.scene.skybox.render()

    def get_color_texture(self):
        color_texture = self.ctx.texture(self.app.WIN_SIZE, components=4)
        color_texture.repeat_x = False
        color_texture.repeat_y = False
        return color_texture

    def post_render(self):
        self.app.ctx.screen.use()  # Switch back to the default frame buffer (screen)
        self.app.ctx.clear()  # Clear the screen

        # print(f"Color texture size: {self.color_texture.width} x {self.color_texture.height}")  # Debugging

        self.color_texture.use(location=0)
        self.post_processing_program['u_color_0'] = 0

        self.post_processing_vao.render(moderngl.TRIANGLES, vertices=6)

    def render(self):
        self.scene.update()
        self.render_shadow()
        self.main_render()
        # self.post_render()

    def destroy(self):
        self.depth_fbo.release()
        self.color_fbo.release()
