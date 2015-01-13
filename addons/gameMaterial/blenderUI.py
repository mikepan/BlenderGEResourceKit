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

			# bail code
			if not mat:
				continue
			if mat.specular_shader != 'BLINN':
				row.label('Warning: Not an Ubershader', icon='ERROR')
				layout.active = False

			# edit albedo
			row = layout.row()
			row.prop(mat, 'diffuse_intensity', text='Albedo')
	
			for textureSlot in mat.texture_slots:
				if textureSlot:
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
						...
					if textureSlot.texture_coords == 'UV' and tex.image:
						split.prop_search(textureSlot, "uv_layer", context.active_object.data, "uv_textures", text="")

		# additional material controls
		row = layout.row()
		row.label('Metallic')
		row = layout.row()
		row.prop(mat, 'specular_color')


class BLEasyAsset(GamePanel, bpy.types.Panel):
	"""Creates a Panel in the Object properties window"""
	bl_label = "Easy Asset"
	bl_context = "objectmode"


	def draw(self, context):
		layout = self.layout
		obj = context.object

		row = layout.row()
	


class BLSettings(GamePanel, bpy.types.Panel):
	"""Creates a Panel in the Object properties window"""
	bl_label = "Settings"
	bl_context = "objectmode"


	def draw(self, context):
		layout = self.layout
		obj = context.object

		row = layout.row()

