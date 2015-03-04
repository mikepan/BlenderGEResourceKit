import bpy, imp

from easyGame import easyMaterial
from easyGame import easyAsset

imp.reload(easyMaterial)
imp.reload(easyAsset)


bl_info = {
	"name": "Easy Game Collection",
	"author": "Mike Pan",
	"version": (1, 2),
	"blender": (2, 70, 0),
	"location": "View3D > Tool Shelf > Easy Tabs",
	"description": "Help make the game-creation process simpler.",
	"warning": "",
	"wiki_url": "",
	"category": "Game Engine"
}



def register():
	bpy.utils.register_class(BLEasyMaterial)
	bpy.utils.register_class(BLEasyMaterialAdv)
	bpy.utils.register_class(BLEasyAsset)
	# bpy.utils.register_class(BLSettings)
	bpy.utils.register_class(BLEasyMaterialCreate)
	bpy.utils.register_class(BLEasyAssetCreate)


def unregister():
	bpy.utils.unregister_class(BLEasyMaterial)
	bpy.utils.unregister_class(BLEasyMaterialAdv)
	bpy.utils.unregister_class(BLEasyAsset)
	# bpy.utils.unregister_class(BLSettings)
	bpy.utils.unregister_class(BLEasyMaterialCreate)
	bpy.utils.unregister_class(BLEasyAssetCreate)



###############################################################################


class GamePanel():
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'

	
class BLEasyMaterial(GamePanel, bpy.types.Panel):
	"""Creates the EasyMaterial UI"""
	bl_label = "Easy Material"
	bl_category = "Easy Material"

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

		# bail on no object (We don't want to use poll because that hides the panel)
		if not obj:
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
						continue

					tex = textureSlot.texture
					text = tex.name.split('.')[-1]
					if text.isnumeric():
						text = tex.name.split('.')[-2]

					# move to advanced section
					if text == 'Emit' or text == 'Alpha':
						continue						

					row = layout.row()
					# enable/disable texture channel
					split  = layout.split(percentage=0.20)
					row = split.row()
					row.prop(textureSlot, 'use', text=text)

					# image browse control
					row = split.row()
					row.active = textureSlot.use
					row.template_ID(tex, "image", open="image.open")
					split  = layout.split(percentage=0.20)
					
					# empty
					row = split.row()
					
					split.active = textureSlot.use
					# additional properties
					if text == 'Col':
						split.prop(textureSlot, 'diffuse_color_factor', text='Factor')
						split.prop(mat, 'diffuse_color', text='')
					if text == 'Nor':
						split.prop(textureSlot, 'normal_factor', text='Factor')
					if text == 'Gloss':
						split.prop(textureSlot, 'default_value', text='Factor')

					if textureSlot.texture_coords == 'UV' and tex.image:
						split.prop_search(textureSlot, "uv_layer", context.active_object.data, "uv_textures", text="")


class BLEasyMaterialAdv(GamePanel, bpy.types.Panel):
	"""Creates the EasyMaterial UI"""
	bl_label = "Advanced"
	bl_category = "Easy Material"

	@classmethod
	def poll(self, context):
		return context.active_object

	def draw(self, context):
		layout = self.layout
		obj = context.object

		# bail on no mat slot
		if not context.active_object.material_slots:
			return

		# material editor
		row = layout.row()
		for materialSlot in context.active_object.material_slots:
			mat = materialSlot.material

			# bail code
			if not mat:
				continue
			
			if 'uberMaterial' not in mat:
				# row.label('Not an UberMaterial', icon='ERROR')
				continue
			
			row.prop(mat, 'use_transparency', 'Transparent')
			if mat.use_transparency:
				row.prop(mat, 'transparency_method', expand=True)

			for textureSlot in mat.texture_slots:
				if textureSlot:

					# bail code
					if textureSlot.use_map_color_spec and textureSlot.blend_type == 'COLOR':
						row.prop(textureSlot, 'use', text='Metallic (Use color from Gloss map as Spec Color)')
						continue

					row = layout.row()
					tex = textureSlot.texture
					text = tex.name.split('.')[-1]
					if text.isnumeric():
						text = tex.name.split('.')[-2]
					
					if text != 'Emit' and text!= 'Alpha':
						continue

					# enable/disable texture channel
					split  = layout.split(percentage=0.20)
					split.prop(textureSlot, 'use', text=text)

					# image browse control
					split.template_ID(tex, "image", open="image.open")
					split  = layout.split(percentage=0.20)
					
					# empty
					row = split.row()

					# additional properties
					if text == 'Emit':
						split.prop(textureSlot, 'emit_factor', text='Factor')
					
					if textureSlot.texture_coords == 'UV' and tex.image:
						split.prop_search(textureSlot, "uv_layer", context.active_object.data, "uv_textures", text="")

	
class BLEasyAsset(GamePanel, bpy.types.Panel):
	"""Creates The Easy Asset Interface"""
	bl_label = "Easy Asset"
	bl_context = "objectmode"
	bl_category = "Easy Asset"

	def draw(self, context):
		layout = self.layout
		obj = context.object

		row = layout.row()
		row.label('Create Camera')
		row = layout.row(align=True)
		row.operator("easy.assetcreate", text='FPS Camera').arg = 'camera.fps'
		row.operator("easy.assetcreate", text='Orbit Camera').arg = 'camera.orbit'

		row = layout.row()
		row.label('Create Lights')
		row = layout.row(align=True)
		row.operator("easy.assetcreate", text='Day-Night Cycle').arg = 'light.cycle'
		row.operator("easy.assetcreate", text='Soft Light').arg = 'light.soft'
		
		row = layout.row()
		row.label('Create Objects')
		row = layout.row(align=True)
		row.operator("easy.assetcreate", text='Plane Mirror').arg = 'obj.mirror'
		# row.operator("easy.assetcreate", text='Orbit Camera').arg = 'camera.orbit'


		row = layout.row()
		row.label('Effects')
		row = layout.row(align=True)
		row.operator("easy.assetcreate", text='Post-Processing 2D Filters').arg = 'post.main'

		row = layout.row()
		
		# row.label('Assets:')
		# template_list now takes two new args.
		# The first one is the identifier of the registered UIList to use (if you want only the default list,
		# with no custom draw code, use "UI_UL_list").
		# layout.template_list("UI_UL_list", "assetid", obj, "material_slots", obj, "active_material_index")



class BLEasyMaterialCreate(bpy.types.Operator):
	"""Create an übershader"""
	bl_label = "New UberMaterial"
	bl_idname = 'easy.matcreate'
	bl_options = {'REGISTER', 'UNDO'}

	MatName = bpy.props.StringProperty(name='Material Name', default='uber')

	def execute(self, context):
		error = easyMaterial.sanityCheck(context)
		if not error:
			mat = easyMaterial.createMaterial(context, self.MatName)
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
		
		# cleanup before we start
		bpy.ops.object.select_all(action='DESELECT')

		if objType == 'camera':
			error = easyAsset.createCamera(option)
		elif objType == 'light':
			error = easyAsset.createLight(option)
		elif objType == 'obj':
			error = easyAsset.createObj(option)
		elif objType == 'post':
			error = easyAsset.createPost(option)
		else:
			error = 'Sorry, not implemented yet.'

		if error:
			self.report({'ERROR'}, error)
			return {'CANCELLED'}
		else:
			return {'FINISHED'}
		

