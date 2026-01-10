from bpy.types import PropertyGroup
import bpy
from bpy.props import *
from . import data
import bonsai.tool as tool

def update_active_rule(self, context):
    model = tool.Ifc.get()
    self.components.clear()
    if len(data.rules) > self.active_rule_index:
        self.rule_name = data.rules[self.active_rule_index]['name']
        self.rule_description = data.rules[self.active_rule_index]['description']
        self.source_elements = data.rules[self.active_rule_index]['check']
        self.search_elements = data.rules[self.active_rule_index]['search']
        self.top_dist = data.rules[self.active_rule_index]['distances']['top']
        self.bottom_dist = data.rules[self.active_rule_index]['distances']['bottom']
        self.front_dist = data.rules[self.active_rule_index]['distances']['front']
        self.back_dist = data.rules[self.active_rule_index]['distances']['back']
        self.right_dist = data.rules[self.active_rule_index]['distances']['right']
        self.left_dist = data.rules[self.active_rule_index]['distances']['left']
    
    if len(data.results) > 0:
        self.result_elements.clear()
        search_elements = data.results[self.active_rule_index]
        print(search_elements)
        for ifc_id, sides in search_elements.items(): 
            # elementos encontrados na busca                     
            search_element = model.by_id(ifc_id)
            new_search_element = self.result_elements.add()
            new_search_element.rule = self.active_rule_index
            new_search_element.type = search_element.is_a()
            new_search_element.name = search_element.Name
            new_search_element.ifc_id = ifc_id     
              

def update_active_result_element(self, context):     
            if len(data.results) > 0:
                 key = list(data.results[self.active_rule_index].keys())[self.active_result_element_index]
                 components = data.results[self.active_rule_index][key]
            self.components.clear()
            for side, elements in components.items():
                new_component = self.components.add()   
                new_component.side = side
                new_component.rule = self.active_rule_index  
                for element in elements:                                           
                    new_item = new_component.elements.add()
                    new_item.type = element.is_a()
                    new_item.name = element.Name
                    new_item.ifc_id = element.id()
                    new_item.side = side
                    new_item.rule = self.active_rule_index

class Element(PropertyGroup):
    rule                 : IntProperty(name='rule') 
    type                 : StringProperty(name='type')
    name                 : StringProperty(name='name')
    ifc_id               : IntProperty(name='ifc_id') 
    side                 : StringProperty(name='side')

class Component(PropertyGroup):
    side                 : StringProperty(name='side')
    rule                 : IntProperty(name='rule')
    n                    : IntProperty(name='n', default=0)
    elements             : CollectionProperty(name='elements', type=Element)    
    active_element_index : IntProperty(name='element index')

class Rule(PropertyGroup):
    type                 : StringProperty(name='type')
    id                   : IntProperty(name='id')
    name                 : StringProperty(name='name')
    description          : StringProperty(name='description')




class GEI_Properties(PropertyGroup): 
    #============================================================================================
    # Check Free Area
    #============================================================================================
    rules                : CollectionProperty(name='results', type=Rule)
    active_rule_index    : IntProperty(name='rule index', update=update_active_rule) 
    show_rule            : BoolProperty(name='show rule', default=False)
    box_is_hide          : BoolProperty(name="hide box", default=False)

    rule_name            : StringProperty(name='rule name')
    rule_description     : StringProperty(name='rule description')

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
    components                  : CollectionProperty(name='elements', type=Component)
    active_component_index      : IntProperty(name='component index')

    result_elements             : CollectionProperty(name='elements', type=Element)
    active_result_element_index : IntProperty(name='component index', update=update_active_result_element)

                                   
