import bpy
import mathutils
from .decorators import BoxDecorator
from .data import *
import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.selector as selector
import bonsai.tool as tool
import multiprocessing

# Get the object's bounding box
#

class Operator_Draw_Box(bpy.types.Operator):
    """Draw clearance box """
    bl_idname = "bim.draw_box"
    bl_label = "Relate Voids to Elements"
    bl_options = {"REGISTER", "UNDO"}


    def execute(self, context): 
        context = bpy.context
        props = context.scene.my_props
        objs = context.selected_objects
        color = props.decorator_color
        sides = ['front', 'back', 'right', 'left', 'top', 'bottom']

        if len(objs)>0:
            obj = objs[0]
            
            for side in sides:
                dist_side = getattr(props, f'{side}_dist')
                if dist_side > 0:
                    corners, edges, minpt, maxpt = get_box(obj, dist_side, side, color)
                    BoxDecorator.install(context, corners, edges)                  
            context.area.tag_redraw()
        return {"FINISHED"}
    
class Operator_Remove_Box(bpy.types.Operator):
    """Remove clearance box"""
    bl_idname = "bim.remove_box"
    bl_label = "Remove clearance box"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context): 
        BoxDecorator.uninstall()
        context.area.tag_redraw()
        return {"FINISHED"}
    
class Operator_Search(bpy.types.Operator):
    """Search components in free area """
    bl_idname = "bim.search"
    bl_label = "Search components in free area"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context): 
        context = bpy.context
        props = context.scene.my_props
        objs = context.selected_objects
        color = props.decorator_color
        sides = ['front', 'back', 'right', 'left', 'top', 'bottom']
        components = {}

        if len(objs)>0:
            tree = get_tree()
            obj = objs[0]
            for side in sides:
                dist_side = getattr(props, f'{side}_dist')
                if dist_side > 0:
                    corners, edges, minpt, maxpt = get_box(obj, dist_side, side, color)
                    elements = tree.select_box((minpt,maxpt), completely_within=True)
                    print(f'elements: {elements}')
                    components[side] = elements
            #components = set(components)
            props.components.clear()
            for side, elements in components.items():
                new_component = props.components.add()
                new_component.side = side
                for element in elements:                    
                    new_item = new_component.elements.add()
                    new_item.type = element.is_a()
                    new_item.name = element.Name
                    new_item.ifc_id = element.id()
                    new_item.side = side
                    obj = tool.Ifc.get_object_by_identifier(element.id())
                    if obj:
                        obj.select_set(True)

            
        return {"FINISHED"}
    
class Operator_select_object(bpy.types.Operator):
    """Search components in free area """
    bl_idname = "bim.select_object"
    bl_label = "Select object"
    bl_options = {"REGISTER", "UNDO"}
    ifc_id : bpy.props.IntProperty(name='ifc_id')

    def execute(self, context):
        obj = tool.Ifc.get_object_by_identifier(self.ifc_id)
        if obj:
            obj.select_set(True)
        return {"FINISHED"}