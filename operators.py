import bpy
from .decorators import BoxDecorator
from . import data
import webbrowser
import bonsai.tool as tool
import json

#============================================================================================
# Check Free Area
#============================================================================================

class Operator_Load_Rules(bpy.types.Operator):
    """ """
    bl_idname = "gei.load_rules"
    bl_label = "Load rules"
    bl_description = "Load rules"
    bl_options = {"REGISTER", "UNDO"}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context): 
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                dados = json.load(f)
            print(dados)
            props = context.scene.gei_props
            props.show_rule = False
            data.load_rules(context, dados)
        except Exception as e:
            bpy.ops.wm.error_message('INVOKE_DEFAULT', message=str(e))
            return {"CANCELLED"}

        return {"FINISHED"}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return{'RUNNING_MODAL'}

class Operator_Save_Rules(bpy.types.Operator):
    """ """
    bl_idname = "gei.save_rules"
    bl_label = "Save rules"
    bl_description = "Load rules"
    bl_options = {"REGISTER", "UNDO"}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context): 
        try:
            dados={}
            dados['rules'] = data.save_rules()
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=4)
            print(dados)
            props = context.scene.gei_props
            props.show_rule = False
            
        except Exception as e:
            bpy.ops.wm.error_message('INVOKE_DEFAULT', message=str(e))
            return {"CANCELLED"}

        return {"FINISHED"}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return{'RUNNING_MODAL'}
       
class Operator_Clear_Rules(bpy.types.Operator):
    """ """
    bl_idname = "gei.clear_rules"
    bl_label = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context): 
        props = context.scene.gei_props
        props.show_rule = False
        data.clear_rules()
        return {"FINISHED"}

class Operator_Add_Rule(bpy.types.Operator):
    """ """
    bl_idname = "gei.add_rule"
    bl_label = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context): 
        data.add_rule(context)
        return {"FINISHED"}

class Operator_Show_Hide_Rule(bpy.types.Operator):
    """ """
    bl_idname = "gei.show_hide_rule"
    bl_label = ""
    bl_options = {"REGISTER", "UNDO"}
    
    id : bpy.props.IntProperty(name="id")

    def execute(self, context): 
        props = context.scene.gei_props
        props.show_rule = not props.show_rule            
        return {"FINISHED"}
    
class Operator_Quit_Rule(bpy.types.Operator):
    """ """
    bl_idname = "gei.quit_rule"
    bl_label = ""
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context): 
        props = context.scene.gei_props
        props.show_rule = False
        return {"FINISHED"}
    
class Operator_Save_Rule(bpy.types.Operator):
    """ """
    bl_idname = "gei.save_rule"
    bl_label = ""
    bl_options = {"REGISTER", "UNDO"}

    id : bpy.props.IntProperty(name="id")

    def execute(self, context): 
        try:
            data.save_rule(context, self.id)
        except Exception as e:            
            bpy.ops.wm.error_message('INVOKE_DEFAULT', message=str(e))
            return {"CANCELLED"}
        return {"FINISHED"}

class Operator_Delete_Rule(bpy.types.Operator):
    """ """
    bl_idname = "gei.delete_rule"
    bl_label = ""
    bl_options = {"REGISTER", "UNDO"}

    id : bpy.props.IntProperty(name="id")

    def execute(self, context): 
        try:
            data.delete_rule(context, self.id)
        except Exception as e:            
            bpy.ops.wm.error_message('INVOKE_DEFAULT', message=str(e))
            return {"CANCELLED"}
        return {"FINISHED"}

class Operator_Draw_Box(bpy.types.Operator):
    """Draw clearance box """
    bl_idname = "gei.draw_box"
    bl_label = "Relate Voids to Elements"
    bl_options = {"REGISTER", "UNDO"}


    def execute(self, context):         
        props = context.scene.gei_props
        objs = context.selected_objects
        color = props.decorator_color
        sides = ['front', 'back', 'right', 'left', 'top', 'bottom']
        BoxDecorator.uninstall()
        context.area.tag_redraw()
        if len(objs)>0:
            obj = objs[0]
            
            for side in sides:
                dist_side = getattr(props, f'{side}_dist')
                if dist_side > 0:
                    corners, edges, minpt, maxpt = data.get_box(obj, dist_side, side, color)
                    BoxDecorator.install(context, corners, edges)                  
            context.area.tag_redraw()
        return {"FINISHED"}
    
class Operator_Remove_Box(bpy.types.Operator):
    """Remove clearance box"""
    bl_idname = "gei.remove_box"
    bl_label = "Remove clearance box"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context): 
        BoxDecorator.uninstall()
        context.area.tag_redraw()
        return {"FINISHED"}
    
class Operator_Clear_Distances(bpy.types.Operator):
    """Clear input distances"""
    bl_idname = "gei.clear_distances"
    bl_label = "Clear input distances"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context): 
        props = context.scene.gei_props
        props.front_dist = 0
        props.back_dist = 0
        props.top_dist = 0
        props.bottom_dist = 0
        props.right_dist = 0
        props.left_dist = 0
        return {"FINISHED"}
    
class Operator_Search(bpy.types.Operator):
    """Search components in free area """
    bl_idname = "gei.search"
    bl_label = "Search components in free area"
    bl_options = {"REGISTER", "UNDO"}
   
    def execute(self, context):         
        props = context.scene.gei_props
        color = props.decorator_color 
        model = tool.Ifc.get()
        try:       
            data.check_free_area(color)             
            print(data.results)
            context.area.tag_redraw()
            return {"FINISHED"}
        except Exception as e:
            bpy.ops.wm.error_message('INVOKE_DEFAULT', message=str(e))
            return {"CANCELLED"}
    
    def draw(self, context):
        layout = self.layout
        layout.label(text=self.mensagem, icon='ERROR')

class Operator_select_object(bpy.types.Operator):
    """Search components in free area """
    bl_idname = "gei.select_object"
    bl_label = "Select object"
    bl_options = {"REGISTER", "UNDO"}
    ifc_id : bpy.props.IntProperty(name='ifc_id')

    def execute(self, context):
        obj = tool.Ifc.get_object_by_identifier(self.ifc_id)
        if obj:
            obj.select_set(True)
        return {"FINISHED"}

#============================================================================================
# Geral
#============================================================================================

class ErrorMessage(bpy.types.Operator):
    bl_idname = "wm.error_message"
    bl_label = "Erro!"

    message: bpy.props.StringProperty()
    
    def execute(self, context):
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=600)
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text='ERROR:')

        row = layout.row()
        row.label(text=self.message, icon='ERROR')

class OpenWebpage(bpy.types.Operator):
    bl_idname = "gei.open_webpage"
    bl_label = "Open webpage"

    uri: bpy.props.StringProperty(name='URL', default='https://openbimacademy.com.br')
    
    def execute(self, context):
        webbrowser.open(self.uri)
        return {'FINISHED'}
    
