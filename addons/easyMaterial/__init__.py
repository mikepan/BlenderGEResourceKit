import bpy, imp

from easyGame import easyMaterial
from easyGame import easyAsset
imp.reload(easyMaterial)
imp.reload(easyAsset)


bl_info = {
	"name": "Easy Games for Game Engine",
	"author": "Mike Pan",
	"version": (1, 0),
	"blender": (2, 70, 0),
	"location": "View3D > Tool Shelf > Easy Games Tab",
	"description": "Help make the game creation process less painful",
	"warning": "",
	"wiki_url": "",
	"category": "Game Engine"
}



def register():
	bpy.utils.register_class(BLEasyMaterial)
	bpy.utils.register_class(BLEasyAsset)
	bpy.utils.register_class(BLSettings)
	bpy.utils.register_class(BLEasyMaterialCreate)
	bpy.utils.register_class(BLEasyAssetCreate)

def unregister():
	bpy.utils.unregister_class(BLEasyMaterial)
	bpy.utils.unregister_class(BLEasyAsset)
	bpy.utils.unregister_class(BLSettings)
	bpy.utils.unregister_class(BLEasyMaterialCreate)
	bpy.utils.unregister_class(BLEasyAssetCreate)


###############################################################################


class GamePanel():
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "Easy Games"

	
class BLEasyMaterial(GamePanel, bpy.types.Panel):
	"""Creates the EasyMaterial UI"""
	bl_label = "Easy Material"
	# bl_context = "objectmode"

	@classmethod
	def poll(self, context):
		return context.active_object

	def draw(self, context):
		layout = self.layout
		obj = context.object

		# bail on wrong display mode
		if context.scene.game_settings.material_mode != 'GLSL':
			row = layout.row()
			row.label('EasyMaterial requires GLSL mode', icon='ERROR')
			row = layout.row()
			row.prop(context.scene.game_settings, 'material_mode', text='')
			return

		# material datablock manager
		row = layout.row()
		layout.template_ID_preview(obj, "active_material", new="easy.matcreate")

		# material editor
		row = layout.row()
		for materialSlot in context.active_object.material_slots:
			mat = materialSlot.material

			# bail code
			if not mat:
				continue
			if 'uberMaterial' not in mat:
				row.label('Not an UberMaterial', icon='ERROR')
				continue

			# edit albedo
			row = layout.row()
			row.prop(mat, 'diffuse_intensity', text='Albedo')
	


			metallicTextureSlot = None
			for textureSlot in mat.texture_slots:
				if textureSlot:
					# bail code
					if textureSlot.use_map_color_spec and textureSlot.blend_type == 'COLOR':
						metallicTextureSlot = textureSlot
						continue


					row = layout.row()
					tex = textureSlot.texture
					text = tex.name.split('.')[-1]
					if text.isnumeric():
						text = tex.name.split('.')[-2]
					# enable/disable texture channel
					split  = layout.split(percentage=0.20)
					split.prop(textureSlot, 'use', text=text)

					# image browse control
					split.template_ID(tex, "image", open="image.open")
					split  = layout.split(percentage=0.20)
					
					# empty
					row = split.row()

					# additional properties
					if text == 'Col':
						split.prop(textureSlot, 'diffuse_color_factor', text='Factor')
						split.prop(mat, 'diffuse_color', text='')
					if text == 'Nor':
						split.prop(textureSlot, 'normal_factor', text='Factor')
					if text == 'Gloss':
						split.prop(textureSlot, 'default_value', text='Factor')
						if metallicTextureSlot:
							split.prop(metallicTextureSlot, 'use', text='Metallic')


					if textureSlot.texture_coords == 'UV' and tex.image:
						split.prop_search(textureSlot, "uv_layer", context.active_object.data, "uv_textures", text="")


class BLEasyAsset(GamePanel, bpy.types.Panel):
	"""Creates The Easy Asset Interface"""
	bl_label = "Easy Asset"
	bl_context = "objectmode"

	# @classmethod
	# def poll(self, context):
	# 	return context.active_object


	def draw(self, context):
		layout = self.layout
		obj = context.object

		row = layout.row()
		row.label('Camera')
		row = layout.row(align=True)
		row.operator("easy.assetcreate", text='Create FPS Camera').arg = 'camera.fps'
		row.operator("easy.assetcreate", text='Create Orbit Camera').arg = 'camera.orbit'

		row = layout.row()
		row.label('Light')
		row = layout.row(align=True)
		row.operator("easy.assetcreate", text='Create Light Cycle').arg = 'light.cycle'
		row.operator("easy.assetcreate", text='Create Orbit Camera').arg = 'light.orbit'
	


class BLSettings(GamePanel, bpy.types.Panel):
	"""Creates a Panel in the Object properties window"""
	bl_label = "Settings"
	bl_context = "objectmode"


	def draw(self, context):
		layout = self.layout
		obj = context.object
		row = layout.row()



class BLEasyMaterialCreate(bpy.types.Operator):
	"""Create an übershader"""
	bl_label = "New UberMaterial"
	bl_idname = 'easy.matcreate'

	def execute(self, context):
		error = easyMaterial.sanityCheck(context)
		if not error:
			mat = easyMaterial.createMaterial(context, 'uber')
			easyMaterial.assignMaterial(context, mat)
			return {'FINISHED'}
		else:
			self.report({'ERROR'}, error)
			return {'CANCELLED'}


class BLEasyAssetCreate(bpy.types.Operator):
	"""Create an asset"""
	bl_label = "New Asset"
	bl_idname = 'easy.assetcreate'
	bl_options = {'REGISTER', 'UNDO'}

	arg = bpy.props.StringProperty()
	
	def execute(self, context):
		objType, option = self.arg.split('.')
		if objType == 'camera':
			easyAsset.createCamera(context, option)
		else:
			print('Unsupported Asset')


		return {'FINISHED'}
		self.report({'ERROR'}, error)
		return {'CANCELLED'}
