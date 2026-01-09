import bpy
import os
from .operators import *
from . import data
from . import previews

#============================================================================================
# Check Free Area
#============================================================================================

class Panel_Free_Area(bpy.types.Panel):
    
    bl_label        = "Check free area"
    bl_idname       = "VIEW3D_PT_free_area"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "GeoInspector"    
    #bl_options      = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='OBJECT_HIDDEN')
    
    def draw(self, context): 
        props = context.scene.gei_props
        layout = self.layout
            
        if props.show_rule:
                icon = 'HIDE_ON'
                text = 'Hide rule'
        else:
            icon = 'HIDE_OFF'
            text = 'Show rule'

        row = layout.row()      
        row.operator("gei.load_rules", text='Load Rules')   
        row.operator("gei.save_rules", text='Save Rules') 
        row.operator("gei.clear_rules", text='Clear Rules') 
        row = layout.row() 
         
        row.operator("gei.add_rule", text='Add Rule', icon='EVENT_NDOF_BUTTON_PLUS') 
        if  len(data.rules) > 0: 
            row.operator("gei.show_hide_rule", text=text, icon=icon) 
        
        if  len(data.rules) > 0:  
            row = layout.row()
            row.label(text='Rules:')
            self.layout.template_list(
                "GI_UL_rules",
                "",
                props,
                "rules",
                props,
                "active_rule_index",
                rows=4
            )
        # show activated rule
        if  props.show_rule and len(data.rules) > 0:            
            row = layout.row() 
            row.separator()
            
            row = layout.row() 
            row.label(text="Active Rule:")
            
            box = layout.box() 
            split=box.split(factor=0.6)
            col_text = split.column()
            col_prop = split.column()
            
            col_text.label(text='Name')
            col_text.label(text='Description')
            col_text.label(text='Checked Componentes')
            col_text.label(text='Componentes in  free area')
            
            col_prop.prop(props, "rule_name", text="")
            col_prop.prop(props, "rule_description", text="")
            col_prop.prop(props, 'source_elements', text='')
            col_prop.prop(props, 'search_elements', text='')

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
            col1.operator("gei.clear_distances", text="clear distances")
            
            col2.separator()
            
            pcoll = previews.preview_collections["main"]
            col2.template_icon(icon_value=pcoll['dimensions'].icon_id, scale=10)

            row = layout.row()
            row.operator("gei.remove_box", text="Remove boxes")
            row.operator("gei.draw_box", text="Draw boxes")
            row = layout.row()
            row.separator()
            row = layout.row()
            row.operator("gei.quit_rule", text="Quit", icon='QUIT')
            row.operator("gei.save_rule", text="Save Rule", icon='DISC').id = props.active_rule_index
        row = layout.row() 
        row.operator("gei.search", text="Search components in free area", icon='VIEWZOOM')
          
class GI_UL_rules(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if item:
            row = layout.row(align=True)
            #row.label(text=f'#{item.id}')
            row.label(text=item.name)
            row.label(text=item.description)
            row.operator("gei.delete_rule", text='', icon='CANCEL').id = item.id
            

#============================================================================================
# Results
#============================================================================================
class Panel_Results(bpy.types.Panel):
    
    bl_label        = "Results"
    bl_idname       = "VIEW3D_PT_results"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "GeoInspector"    
    #bl_options      = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='WORDWRAP_ON')

    def draw(self, context): 
        props = context.scene.gei_props
        layout = self.layout        
        if len(props.components) > 0:
            row = layout.row()
            row.separator()
            row = layout.row()
            row.label(text='Elements found:')

            self.layout.template_list(
                "GI_UL_result_elements",
                "",
                props,
                "result_elements",
                props,
                "active_result_element_index",
                rows=4
            )

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

class GI_UL_result_elements(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if item:
            row = layout.row(align=True)  
            row.label(text=str(item.ifc_id))             
            row.label(text=item.type)
            row.label(text=item.name)          
            # op = row.operator("gei.select_object", text="", icon="RESTRICT_SELECT_OFF")
            # op.ifc_id = item.ifc_id

class GI_UL_components(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        props = context.scene.gei_props
        if item:
            #if props.active_rule_index == item.rule:                    
                row = layout.row(align=True)
                row.label(text=item.side, icon="SELECT_SUBTRACT")
                row.label(text=str(item.rule))
                row.label(text=str(item.side))
                # op = row.operator("gei.select_object", text="", icon="RESTRICT_SELECT_OFF")
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
            op = row.operator("gei.select_object", text="", icon="RESTRICT_SELECT_OFF")
            op.ifc_id = item.ifc_id

#============================================================================================
# Settings
#============================================================================================

class Panel_Settings(bpy.types.Panel):
    
    bl_label        = "Settings"
    bl_idname       = "VIEW3D_PT_settings"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "GeoInspector"
    bl_options      = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='SETTINGS')

    def draw(self, context):
        props = context.scene.gei_props
        layout = self.layout
        row = layout.row()
        row.prop(props, "decorator_color") 
    
#============================================================================================
# Author
#============================================================================================

class Panel_Info(bpy.types.Panel):
    
    bl_label        = "Info"
    bl_idname       = "VIEW3D_PT_info"
    bl_space_type   = 'VIEW_3D'
    bl_region_type  = 'UI'
    bl_context      = "objectmode"
    bl_category     = "GeoInspector"
    bl_options      = {"DEFAULT_CLOSED"}
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(text="", icon='INFO_LARGE')

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="GeoInspector V 0.2.0", icon='MOD_LINEART')
        row = layout.row()
        row.label(text="Carlos dias - Open BIM Academy\u00AE")
        row = layout.row()
        row.operator("gei.open_webpage", text="", icon='URL').uri = 'https://github.com/c4rlosdias/GeoInspector'
        row.label(text="https://github.com/c4rlosdias/GeoInspector")

