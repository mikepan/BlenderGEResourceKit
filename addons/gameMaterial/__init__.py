from gameMaterial.blenderUI import *
from gameMaterial.easyMaterial import *

import bpy


bl_info = {
	"name": "EasyMaterial",
	"author": "Mike Pan",
	"version": (1, 0),
	"blender": (2, 70, 0),
	"location": "View3D > Tool Shelf > Easy Material Tab",
	"description": "Easily creates realistic material",
	"warning": "",
	"wiki_url": "",
	"category": "Game Engine"
}



def register():
	bpy.utils.register_class(BLEasyMaterial)
	bpy.utils.register_class(BLEasyAsset)
	bpy.utils.register_class(BLSettings)
	
	bpy.utils.register_class(BLEasyMaterialCreate)



def unregister():
	bpy.utils.unregister_class(BLEasyMaterial)
	bpy.utils.unregister_class(BLEasyAsset)
	bpy.utils.unregister_class(BLSettings)

	bpy.utils.unregister_class(BLEasyMaterialCreate)
