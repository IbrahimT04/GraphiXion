import numpy
import pywavefront


class VBO:
    def __init__(self, ctx):
        self.vbos = {}
        self.vbos['cube'] = CubeVBO(ctx)
        self.vbos['advanced_cube'] = AdvancedCubeVBO(ctx)
        self.vbos['skull'] = SkullVBO(ctx)
        self.vbos['skybox'] = SkyBoxVBO(ctx)
        self.vbos['advanced_skybox'] = AdvancedSkyBoxVBO(ctx)

        self.vbos['basic_post_processing'] = QuadVBO(ctx)

    def destroy(self):
        [vbo.destroy() for vbo in self.vbos.values()]


class BaseVBO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = self.get_vbo()
        self.format: str = ''
        self.attrib: list = []

    def get_vertex_data(self): ...

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def destroy(self):
        self.vbo.release()


class CubeVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '2f 3f 3f'
        self.attrib = ['in_texture_coord_0', 'in_normal', 'in_position']

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return numpy.array(data, dtype='f4')

    def get_vertex_data(self):
        vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]
        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        vertex_data = self.get_data(vertices, indices)

        tex_coord = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [(0, 2, 3), (0, 1, 2),
                             (0, 2, 3), (0, 1, 2),
                             (0, 1, 2), (2, 3, 0),
                             (2, 3, 0), (2, 0, 1),
                             (0, 2, 3), (0, 1, 2),
                             (3, 1, 2), (3, 0, 1)]
        tex_coord_data = self.get_data(tex_coord, tex_coord_indices)

        normals = [(0, 0, 1) * 6,
                   (1, 0, 0) * 6,
                   (0, 0, -1) * 6,
                   (-1, 0, 0) * 6,
                   (0, 1, 0) * 6,
                   (0, -1, 0) * 6]
        normals = numpy.array(normals, dtype='f4').reshape(36, 3)

        vertex_data = numpy.hstack([normals, vertex_data])
        vertex_data = numpy.hstack([tex_coord_data, vertex_data])
        return vertex_data


class AdvancedCubeVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '2f 3f 3f 3f 3f'
        self.attrib = ['in_texture_coord_0', 'in_normal', 'in_position', 'in_tangent', 'in_bitangent']

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return numpy.array(data, dtype='f4')

    def get_vertex_data(self):
        vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]
        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        vertex_data = self.get_data(vertices, indices)

        tex_coord = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [(0, 2, 3), (0, 1, 2),
                             (0, 2, 3), (0, 1, 2),
                             (0, 1, 2), (2, 3, 0),
                             (2, 3, 0), (2, 0, 1),
                             (0, 2, 3), (0, 1, 2),
                             (3, 1, 2), (3, 0, 1)]
        tex_coord_data = self.get_data(tex_coord, tex_coord_indices)

        normals = [(0, 0, -1) * 6,
                   (1, 0, 0) * 6,
                   (0, 0, 1) * 6,
                   (-1, 0, 0) * 6,
                   (0, 1, 0) * 6,
                   (0, -1, 0) * 6]
        normals = numpy.array(normals, dtype='f4').reshape(36, 3)

        bitangents = [(0, -1, 0) * 6,
                      (0, 1, 0) * 6,
                      (0, -1, 0) * 6,
                      (0, 1, 0) * 6,
                      (0, 0, -1) * 6,
                      (0, 0, 1) * 6]
        bitangents = numpy.array(bitangents, dtype='f4').reshape(36, 3)

        tangents = [(-1, 0, 0) * 6,
                    (0, 0, -1) * 6,
                    (1, 0, 0) * 6,
                    (0, 0, 1) * 6,
                    (1, 0, 0) * 6,
                    (1, 0, 0) * 6]
        tangents = numpy.array(tangents, dtype='f4').reshape(36, 3)

        final_data = numpy.hstack([tangents, bitangents])
        final_data = numpy.hstack([vertex_data, final_data])
        final_data = numpy.hstack([normals, final_data])
        final_data = numpy.hstack([tex_coord_data, final_data])
        return final_data


class SkullVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attrib = ['in_texture_coord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/12140_Skull_v3_L2.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = numpy.array(vertex_data, dtype='f4')
        return vertex_data


class SkyBoxVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '3f'
        self.attrib = ['in_position']

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return numpy.array(data, dtype='f4')

    def get_vertex_data(self):
        vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]
        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        vertex_data = self.get_data(vertices, indices)
        vertex_data = numpy.flip(vertex_data, 1).copy(order='C')
        return vertex_data


class AdvancedSkyBoxVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '3f'
        self.attrib = ['in_position']

    def get_vertex_data(self):
        z = 0.9999
        vertices = [(-1, -1, z), (3, -1, z), (-1, 3, z)]
        vertex_data = numpy.array(vertices, dtype='f4')
        return vertex_data


class QuadVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '2f 2f'  # 2 floats for position, 2 floats for texture coordinates
        self.attrib = ['in_position', 'in_uv']  # Attribute names for the shader program

    def get_vertex_data(self):
        # Full screen quad vertices: Two triangles covering the entire screen
        # (x, y, u, v) for each vertex
        vertices = numpy.array([
            # positions     # texture coordinates
            -1.0, -1.0, 0.0, 0.0,  # bottom-left corner
            1.0, -1.0, 1.0, 0.0,  # bottom-right corner
            1.0, 1.0, 1.0, 1.0,  # top-right corner
            1.0, 1.0, 1.0, 1.0,  # top-right corner
            -1.0, 1.0, 0.0, 1.0,  # top-left corner
            -1.0, -1.0, 0.0, 0.0  # bottom-left corner
        ], dtype='f4')
        return vertices
