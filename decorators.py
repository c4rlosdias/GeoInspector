import bpy
import mathutils
import gpu
from gpu_extras.batch import batch_for_shader

class BoxDecorator:

    is_installed = False
    handlers = []
   
    @classmethod
    def install(cls, context, corners, edges):
        # if cls.is_installed:
        #     cls.uninstall()
        handler = cls()
        props = context.scene.gei_props
        color = props.decorator_color
        cls.handlers.append(
            bpy.types.SpaceView3D.draw_handler_add(
                handler.draw_solid_cube, (context, corners, color), "WINDOW", "POST_VIEW"
            )
        )
        cls.is_installed = True
        props.box_is_hide = False

    @classmethod
    def uninstall(cls, context):
        props = context.scene.gei_props
        for handler in cls.handlers:
            try:
                bpy.types.SpaceView3D.draw_handler_remove(handler, "WINDOW")
            except Exception:
                pass
        cls.handlers.clear()
        cls.is_installed = False
        props.box_is_hide = True
        

    def draw_solid_cube(self, context, corners, color=(1, 1, 1, 0.2)):
        """
        Desenha uma caixa sólida (faces preenchidas) usando os vértices fornecidos em 'corners'.
        'corners' deve ser uma lista de 8 vetores (x, y, z) na ordem padrão de cubo.
        'color' é RGBA.
        """
        shader = gpu.shader.from_builtin("UNIFORM_COLOR")
        shader.bind()
        shader.uniform_float("color", color)
        # Cube faces definition (each face is composed by 2 triangles)
        faces = [
            [0, 1, 3, 2],  # Direita
            [4, 5, 7, 6],  # Esquerda
            [0, 1, 7, 6],  # Frente
            [4, 5, 3, 2],  # Trás
            [6, 0, 2, 4],  # Superior
            [7, 1, 3, 5],  # Inferior
        ]
        # Para cada face, desenhar dois triângulos
        triangles = []
        for f in faces:
            triangles.extend([
                corners[f[0]], corners[f[1]], corners[f[2]],
                corners[f[0]], corners[f[2]], corners[f[3]],
            ])
        batch = batch_for_shader(shader, "TRIS", {"pos": triangles})
        batch.draw(shader)