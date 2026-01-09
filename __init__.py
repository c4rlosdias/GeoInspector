# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


bl_info = {
    "name"        : "GeoInspector",
    "author"      : "Carlos Dias",
    "description" : "",
    "blender"     : (5, 0, 0),
    "version"     : (0, 0, 1),
    "location"    : "View3D > Panel > GeoInspector",
    "warning"     : "",
    "category"    : "User"
}


import sys
import os
from bpy.props import PointerProperty
from bpy.types import Scene
from bpy.utils import register_class, unregister_class
from .operators import *
from .panels import *
from .properties import *
from .decorators import BoxDecorator
from . import previews


#if sys.modules.get("bpy", None):
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), "libs", "site", "packages"))


classes = [
    Element,
    Component,
    Rule,
    GEI_Properties, 
    Operator_Load_Rules,  
    Operator_Save_Rules,
    Operator_Clear_Rules, 
    Operator_Add_Rule,
    Operator_Show_Hide_Rule,
    Operator_Quit_Rule,
    Operator_Save_Rule,
    Operator_Delete_Rule,
    Operator_Draw_Box,
    Operator_Remove_Box,
    Operator_Clear_Distances,
    Operator_Search,
    Operator_select_object,
    ErrorMessage,
    OpenWebpage,
    GI_UL_result_elements,
    GI_UL_elements,
    GI_UL_components,
    Panel_Free_Area,
    GI_UL_rules,
    Panel_Results,
    Panel_Settings,
    Panel_Info
    
]

def register():
    data.clear_rules()
    previews.load_previews()
    for c in classes:
        register_class(c)
    Scene.gei_props = PointerProperty(type=GEI_Properties)


def unregister():
    data.clear_rules()
    del Scene.gei_props
    for c in classes:
        unregister_class(c)
    previews.unload_previews()

if __name__ == "__main__":
    register()