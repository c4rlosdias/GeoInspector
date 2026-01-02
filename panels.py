import bpy
import os
from .operators import *
from . import previews



# ---------------------------------------------------------------------
# Draw a clearance box
# ---------------------------------------------------------------------

class Panel_Draw_Box(bpy.types.Panel):
    
    bl_label        = "Check free area"
    bl_idname       = "VIEW3D_PT_free_area"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "GeomInspector"    
    #bl_options      = {"DEFAULT_CLOSED"}
    
    def draw(self, context): 
        props = context.scene.my_props              
        layout = self.layout             

        row = layout.row() 
        row.label(text="Search elements:")
        box = layout.box() 
        split=box.split(factor=0.6)
        col_text = split.column()
        col_prop = split.column()
        col_text.label(text='Checked Componentes')
        col_text.label(text='Componentes in  free area')
        col_prop.prop(props, 'source_elements', text='')
        col_prop.prop(props, 'search_elements', text='')

        row = layout.row()
        row.separator()
        row = layout.row()
        row.prop(props, "decorator_color")
        row = layout.row()
        row.separator()

        row = layout.row() 
        row.label(text="Check Free Area dimensions:")
        box = layout.box() 
        split = box.split(factor=0.3)
        col1=split.column()
        col1.alignment='CENTER'
        col2=split.column()
        col2.alignment='CENTER'
        col1.label(text='Distances:')
        col1.prop(props, "top_dist")
        col1.prop(props, "front_dist")
        col1.prop(props, "back_dist") 
        col1.prop(props, "bottom_dist")      
        col1.prop(props, "right_dist")
        col1.prop(props, "left_dist") 
        col1.separator() 
        col1.operator("bim.clear_distances", text="clear distances")
        
        col2.separator()
        
        pcoll = previews.preview_collections["main"]
        col2.template_icon(icon_value=pcoll['dimensions'].icon_id, scale=10)

        row = layout.row()
        row.operator("bim.remove_box", text="Remove boxes")

        if len(context.selected_objects) > 0:
            #row=layout.row()
            row.operator("bim.draw_box", text="Draw boxes")
            row = layout.row()
            row.operator("bim.search", text="Search components in free area")
        
        if len(props.components) > 0:
            row = layout.row()
            row.separator()
            row = layout.row()
            row.label(text='Components in free area:')
            self.layout.template_list(
                "GI_UL_components",
                "",
                props,
                "components",
                props,
                "active_component_index",
                rows=4
            )
        
class GI_UL_components(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if item:
            row = layout.row(align=True)
            row.label(text=item.side, icon="SELECT_SUBTRACT")
            # op = row.operator("bim.select_object", text="", icon="RESTRICT_SELECT_OFF")
            # op.ifc_id = item.ifc_id
            if len(item.elements) > 0:
                layout.template_list(
                    "GI_UL_elements",
                    "",
                    item,
                    "elements",
                    item,
                    "active_element_index",
                    rows=3
                )
               
            else: 
                row.label(text='No elements found!')
            
            

class GI_UL_elements(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if item:
            row = layout.row(align=True)               
            row.label(text=item.type)
            row.label(text=item.name)          
            op = row.operator("bim.select_object", text="", icon="RESTRICT_SELECT_OFF")
            op.ifc_id = item.ifc_id

class Panel_Author(bpy.types.Panel):
    
    bl_label        = "Author"
    bl_idname       = "VIEW3D_PT_author"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "GeomInspector"
    bl_options      = {"DEFAULT_CLOSED"}
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="GromInspector V 0.0.1", icon='MOD_LINEART')
        row = layout.row()
        row.label(text="Carlos dias - Open BIM Academy\u00AE")