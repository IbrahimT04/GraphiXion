import pygame
import moderngl


class Texture:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.textures = {}
        # Object_Textures
        self.textures['skull'] = self.get_texture(path='objects/Skull.jpg')
        self.textures['skybox'] = self.get_texture_cube(dir_path='textures/skybox/', ext='jpg')
        self.textures['depth_texture'] = self.get_depth_texture()
        self.textures['color_texture'] = self.get_color_texture()

        # --- Damaged Walls
        # Texture_map
        self.textures[0] = self.get_texture(path='textures/damaged_wall/1_diffuseOriginal_converted.png')
        self.textures[1] = self.get_texture(path='textures/damaged_wall_2/2_diffuseOriginal.bmp')
        self.textures[2] = self.get_texture(path='textures/damaged_wall_3/3_diffuseOriginal.bmp')
        self.textures[3] = self.get_texture(path='textures/damaged_wall_4/4_diffuseOriginal.bmp')
        self.textures[4] = self.get_texture(path='textures/damaged_wall_5/5_diffuseOriginal.bmp')
        # Normal_map
        self.textures[5] = self.get_texture(path='textures/damaged_wall/1_normal.bmp')
        self.textures[6] = self.get_texture(path='textures/damaged_wall_2/2_normal.bmp')
        self.textures[7] = self.get_texture(path='textures/damaged_wall_3/3_normal.bmp')
        self.textures[8] = self.get_texture(path='textures/damaged_wall_4/4_normal.bmp')
        self.textures[9] = self.get_texture(path='textures/damaged_wall_5/5_normal.bmp')
        # Ambient_Occlusion_map
        self.textures[10] = self.get_texture(path='textures/damaged_wall/1_ao.bmp')
        self.textures[11] = self.get_texture(path='textures/damaged_wall_2/2_ao.bmp')
        self.textures[12] = self.get_texture(path='textures/damaged_wall_3/3_ao.bmp')
        self.textures[13] = self.get_texture(path='textures/damaged_wall_4/4_ao.bmp')
        self.textures[14] = self.get_texture(path='textures/damaged_wall_5/5_ao.bmp')
        # Smoothness_map
        self.textures[15] = self.get_texture(path='textures/damaged_wall/1_smoothness.bmp')
        self.textures[16] = self.get_texture(path='textures/damaged_wall_2/2_smoothness.bmp')
        self.textures[17] = self.get_texture(path='textures/damaged_wall_3/3_smoothness.bmp')
        self.textures[18] = self.get_texture(path='textures/damaged_wall_4/4_smoothness.bmp')
        self.textures[19] = self.get_texture(path='textures/damaged_wall_5/5_smoothness.bmp')
        # Metallic_map
        self.textures[20] = self.get_texture(path='textures/damaged_wall/1_metallic.bmp')
        self.textures[21] = self.get_texture(path='textures/damaged_wall_2/2_metallic.bmp')
        self.textures[22] = self.get_texture(path='textures/damaged_wall_3/3_metallic.bmp')
        self.textures[23] = self.get_texture(path='textures/damaged_wall_4/4_metallic.bmp')
        self.textures[24] = self.get_texture(path='textures/damaged_wall_5/5_metallic.bmp')
        # Height_map
        self.textures[25] = self.get_texture(path='textures/damaged_wall/1_height.bmp')
        self.textures[26] = self.get_texture(path='textures/damaged_wall_2/2_height.bmp')
        self.textures[27] = self.get_texture(path='textures/damaged_wall_3/3_height.bmp')
        self.textures[28] = self.get_texture(path='textures/damaged_wall_4/4_height.bmp')
        self.textures[29] = self.get_texture(path='textures/damaged_wall_5/5_height.bmp')

        # --- Metals
        self.textures[100] = self.get_texture(path='textures/metal_2/2_diffuseOriginal.bmp')
        self.textures[105] = self.get_texture(path='textures/metal_2/2_normal.bmp')
        self.textures[110] = self.get_texture(path='textures/metal_2/2_ao.bmp')
        self.textures[115] = self.get_texture(path='textures/metal_2/2_smoothness.bmp')
        self.textures[120] = self.get_texture(path='textures/metal_2/2_metallic.bmp')
        self.textures[125] = self.get_texture(path='textures/metal_2/2_height.bmp')

        # --- Mud
        self.textures[200] = self.get_texture(path='textures/mud_1/1_diffuseOriginal.bmp')
        self.textures[205] = self.get_texture(path='textures/mud_1/1_normal.bmp')
        self.textures[210] = self.get_texture(path='textures/mud_1/1_ao.bmp')
        self.textures[215] = self.get_texture(path='textures/mud_1/1_smoothness.bmp')
        self.textures[220] = self.get_texture(path='textures/mud_1/1_metallic.bmp')
        self.textures[225] = self.get_texture(path='textures/mud_1/1_height.bmp')

        # --- Meme
        self.textures[300] = self.get_texture(path='textures/meme/memeImage.png')

    def get_depth_texture(self):
        depth_texture = self.ctx.depth_texture(self.app.WIN_SIZE)
        depth_texture.repeat_x = False
        depth_texture.repeat_y = False
        return depth_texture

    def get_color_texture(self):
        # Use 4 components (RGBA) for color texture in post-processing
        color_texture = self.ctx.texture(self.app.WIN_SIZE, components=4)  # 3 for RGB
        color_texture.repeat_x = False
        color_texture.repeat_y = False
        return color_texture

    def get_texture_cube(self, dir_path, ext='jpg'):
        faces = ['right', 'left', 'top', 'bottom'] + ['front', 'back'][::-1]
        textures = []
        for face in faces:
            texture = pygame.image.load(dir_path + f'{face}.{ext}').convert()
            if face in ['right', 'left', 'front', 'back']:
                texture = pygame.transform.flip(texture, flip_x=True, flip_y=False)
            else:
                texture = pygame.transform.flip(texture, flip_x=False, flip_y=True)
            textures.append(texture)

        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_data = pygame.image.tostring(textures[i], 'RGB')
            texture_cube.write(face=i, data=texture_data)

        return texture_cube

    def get_texture(self, path):
        texture = pygame.image.load(path).convert()
        texture = pygame.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pygame.image.tostring(texture, 'RGB'))
        texture.filter = (moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR)

        texture.build_mipmaps()

        texture.anisotropy = 32.0
        return texture

    def destroy(self):
        [tex.release() for tex in self.textures.values()]
