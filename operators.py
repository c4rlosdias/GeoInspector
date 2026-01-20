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
    bl_description = "Save rules"
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
        props.active_rule_index = self.id
        item = props.rules[self.id]
        item.show_rule = not item.show_rule 
        props.show_rule = item.show_rule   
        props.active_rule_index = self.id        
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
        try:       
            data.check_free_area(color)             
            print(data.results)
            props.active_rule_index = 0
            return {"FINISHED"}
        except Exception as e:
            bpy.ops.wm.error_message('INVOKE_DEFAULT', message=str(e))
            return {"CANCELLED"}
    


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
    

class Operator_select_results(bpy.types.Operator):
    """"""
    bl_idname = "gei.select_results"
    bl_label = "Select results"
    bl_options = {"REGISTER", "UNDO"}
    ifc_id : bpy.props.IntProperty(name='ifc_id')

    def execute(self, context):
        bpy.ops.object.select_all(action='DESELECT')
        #PBoxDecorator.uninstall(context)
        context.area.tag_redraw()
        props = context.scene.gei_props
        color = props.decorator_color
        sides = data.results[props.active_rule_index][self.ifc_id]
        objs = []        
        obj1 = tool.Ifc.get_object_by_identifier(self.ifc_id)
        if obj1:
            objs.append(obj1)
        for side in sides:
            elements = sides[side]
            for element in elements:
                obj = tool.Ifc.get_object_by_identifier(element.id())
                if obj:
                    objs.append(obj)
        for obj in objs:
            obj.select_set(True)
        
        data.localview(True)
        data.draw_box(props.active_rule_index, obj1, color, context)
        return {"FINISHED"}
    
class Operator_Save_Results(bpy.types.Operator):
    """ """
    bl_idname = "gei.save_results"
    bl_label = "Save results"
    bl_description = "Save results"
    bl_options = {"REGISTER", "UNDO"}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context): 
        try:     
            serializable_results = data.make_serializable(data.results)      
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(serializable_results, f, ensure_ascii=False, indent=4)
            print(data.results)
            
        except Exception as e:
            bpy.ops.wm.error_message('INVOKE_DEFAULT', message=str(e))
            return {"CANCELLED"}

        return {"FINISHED"}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return{'RUNNING_MODAL'}


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
    
