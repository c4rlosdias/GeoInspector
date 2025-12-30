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
        cls.handlers.append(
            bpy.types.SpaceView3D.draw_handler_add(
                handler.draw_wire_cube, (context, corners, edges), "WINDOW", "POST_VIEW"
            )
        )
        cls.is_installed = True

    @classmethod
    def uninstall(cls):
        for handler in cls.handlers:
            try:
                bpy.types.SpaceView3D.draw_handler_remove(handler, "WINDOW")
            except Exception:
                pass
        cls.handlers.clear()
        cls.is_installed = False
        
    
    @staticmethod
    def draw_batch(shader, line_shader, shader_type, content_pos, color, indices=None):
        shader = line_shader if shader_type == "LINES" else shader
        batch = batch_for_shader(shader, shader_type, {"pos": content_pos}, indices=indices)        
        shader.uniform_float("color", color)
        batch.draw(shader)

    def draw_wire_cube(self, context, corners, edges):
        line_shader = gpu.shader.from_builtin("POLYLINE_UNIFORM_COLOR")
        line_shader.bind()
        line_shader.uniform_float("viewportSize", (context.region.width, context.region.height))
        shader = gpu.shader.from_builtin("UNIFORM_COLOR")
        gpu.state.line_width_set(2.0)
        for i1,i2, c in edges:
            self.draw_batch(shader, line_shader, "LINES", [corners[i1], corners[i2]], c)
