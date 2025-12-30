import bpy
import os

preview_collections = {}

def load_previews():
    pcoll = bpy.utils.previews.new()
    path = os.path.join(os.path.dirname(__file__), "resource", "model.png")
    pcoll.load("dimensions", path, 'IMAGE')
    preview_collections["main"] = pcoll

def unload_previews():
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)    
    preview_collections.clear()