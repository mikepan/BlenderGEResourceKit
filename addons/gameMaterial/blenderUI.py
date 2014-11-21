# This module sets up the user interface in Blender that
# is used to manage the easyMaterial

import bpy


class GamePanel():
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "Game Resources"

	
class BLEasyMaterial(GamePanel, bpy.types.Panel):
	"""Creates a Panel in the Object properties window"""
	bl_label = "Easy Material"
	bl_context = "objectmode"

	@classmethod
	def poll(self, context):
		return context.active_object

	def draw(self, context):
		layout = self.layout
		obj = context.object

		if context.scene.game_settings.material_mode != 'GLSL':
			row = layout.row()
			row.label('Warning: GLSL Shading is not enabled', icon='ERROR')
			row = layout.row()
			row.prop(context.scene.game_settings, 'material_mode', text='')

		# material datablock manager
		row = layout.row()
		layout.template_ID_preview(obj, "active_material", new="gr.matcreate")

		# material editor
		row = layout.row()
		for materialSlot in context.active_object.material_slots:
			mat = materialSlot.material
			if not mat:
				continue
			if mat.specular_shader != 'WARDISO':
				row.label('Not an Ubershader, cannot edit.')
				continue

			row = layout.row()
			row.prop(mat, 'diffuse_intensity', text='Albedo')
			row = layout.row()
			row.prop(mat, 'specular_slope', text = 'Gloss')
	
			row = layout.row()
			for textureSlot in mat.texture_slots:
				if textureSlot:
					row = layout.row()
					tex = textureSlot.texture
					text = tex.name.split('.')[-1]
					if text.isnumeric():
						text = tex.name.split('.')[-2]
					split  = layout.split(percentage=0.1)
		
					split.label(text)
					split.template_ID(tex, "image", open="image.open")
					
					split  = layout.split(percentage=0.1)
					row = split.row()
					
			
					if text == 'Col':
						split.prop(textureSlot, 'diffuse_color_factor', text='Factor')
					# if text == 'Nor':
					# 	split.prop(textureSlot, 'normal_factor', text='Factor')
					# if text == 'Gloss':
					# 	split.prop(mat, 'specular_intensity', text='Glossy')

						
					if textureSlot.texture_coords == 'UV' and tex.image:
						split.prop_search(textureSlot, "uv_layer", context.active_object.data, "uv_textures", text="")


class BLEasyAsset(GamePanel, bpy.types.Panel):
	"""Creates a Panel in the Object properties window"""
	bl_label = "Easy Asset"
	bl_context = "objectmode"


	def draw(self, context):
		layout = self.layout
		obj = context.object

		### Tracking ###
		row = layout.row()
	


class BLSettings(GamePanel, bpy.types.Panel):
	"""Creates a Panel in the Object properties window"""
	bl_label = "Settings"
	bl_context = "objectmode"


	def draw(self, context):
		layout = self.layout
		obj = context.object

		### Tracking ###
		row = layout.row()
		
		

		

def register():
	bpy.utils.register_class(BLEasyMaterial)
	bpy.utils.register_class(BLEasyAsset)
	bpy.utils.register_class(BLSettings)


def unregister():
	bpy.utils.unregister_class(BLEasyMaterial)
	bpy.utils.unregister_class(BLEasyAsset)
	bpy.utils.unregister_class(BLSettings)


def refresh():
	try:
		register()
	except ValueError:
		print('Re-registering')
		unregister()
		register()
	