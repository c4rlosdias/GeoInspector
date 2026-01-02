from bpy.types import PropertyGroup
import bpy
from bpy.props import *
from . import data


class Element(PropertyGroup):
    type                 : StringProperty(name='type')
    name                 : StringProperty(name='name')
    ifc_id               : IntProperty(name='ifc_id') 
    side                 : StringProperty(name='side')

class Component(PropertyGroup):
    side                 : StringProperty(name='side')
    n                    : IntProperty(name='n', default=0)
    elements             : CollectionProperty(name='elements', type=Element)    
    active_element_index : IntProperty(name='element index')

class Rule(PropertyGroup):
    type                 : StringProperty(name='type')
    id                   : IntProperty(name='id')
    name                 : StringProperty(name='name')


class MyProperties(PropertyGroup): 
    rules                : CollectionProperty(name='results', type=Rule)
    active_rule_index    : IntProperty(name='rule index' ) 
    add_rule             : BoolProperty(name='add rule', default=False)  

    # Check free area
    box_is_hide          : BoolProperty(name="hide box", default=False)    
    source_elements      : StringProperty(name='Checked Componentes', default='IfcDoor')
    search_elements      : StringProperty(name='Components in free Area', default='IfcElement')
    front_dist           : FloatProperty(name='Front', default=0)
    back_dist            : FloatProperty(name='Back', default=0)
    right_dist           : FloatProperty(name='Right', default=0)
    left_dist            : FloatProperty(name='Left', default=0)
    top_dist             : FloatProperty(name='Top', default=0)
    bottom_dist          : FloatProperty(name='Bottom', default=0)
    decorator_color      : FloatVectorProperty( name='Box color',
                                           subtype='COLOR',
                                           size=4,
                                           min=0.0,
                                           max=1.0,
                                           default=(0.0, 0.0, 1.0, 1.0) 
                           )
    
    # UL elements
    components             : CollectionProperty(name='elements', type=Component)
    active_component_index : IntProperty(name='component index')

                                   
