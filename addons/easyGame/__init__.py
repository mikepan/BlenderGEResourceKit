import bpy, imp

from easyGame import easyMaterial
from easyGame import easyAsset

imp.reload(easyMaterial)
imp.reload(easyAsset)


bl_info = {
	"name": "Easy Game Collection",
	"author": "Mike Pan",
	"version": (1, 5),
	"blender": (2, 70, 0),
	"location": "View3D > Tool Shelf > Easy Tabs",
	"description": "A collection of tools that make the game-creation process easier.",
	"warning": "",
	"wiki_url": "",
	"category": "Game Engine"
}



def register():
	bpy.utils.register_class(BLEasyAsset)
	bpy.utils.register_class(BLEasyMaterial)
	bpy.utils.register_class(BLEasyMaterialAdv)
	# bpy.utils.register_class(BLSettings)
	bpy.utils.register_class(BLEasyMaterialCreate)
	bpy.utils.register_class(BLEasyAssetCreate)


def unregister():
	bpy.utils.unregister_class(BLEasyAsset)
	bpy.utils.unregister_class(BLEasyMaterial)
	bpy.utils.unregister_class(BLEasyMaterialAdv)
	# bpy.utils.unregister_class(BLSettings)
	bpy.utils.unregister_class(BLEasyMaterialCreate)
	bpy.utils.unregister_class(BLEasyAssetCreate)



###############################################################################


class GamePanel():
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'


class BLEasyAsset(GamePanel, bpy.types.Panel):
	"""Creates The Easy Asset Interface"""
	bl_label = "Create Easy Asset"
	bl_context = "objectmode"
	bl_category = "Easy Asset"

	def draw(self, context):
		layout = self.layout
		obj = context.object

		row = layout.row()
		row.label('Camera:')
		row = layout.row(align=True)
		row.operator("easy.assetcreate", text='FPS Camera', icon='OUTLINER_DATA_CAMERA').arg = 'camera.fps'
		row.operator("easy.assetcreate", text='Orbit Camera', icon='OUTLINER_DATA_CAMERA').arg = 'camera.orbit'

		row = layout.row()
		row.label('Lights:')
		row = layout.row(align=True)
		row.operator("easy.assetcreate", text='Day-Night Cycle', icon='LAMP_SUN').arg = 'light.cycle'
		row.operator("easy.assetcreate", text='Soft Light', icon='LAMP_HEMI').arg = 'light.soft'
		
		row = layout.row()
		row.label('Effects:')
		row = layout.column(align=True)
		row.operator("easy.assetcreate", text='Plane Mirror', icon='MOD_MIRROR').arg = 'fx.mirror'

		row.operator("easy.assetcreate", text='Particles - Smoke', icon='STICKY_UVS_DISABLE').arg = 'fx.emitterSmoke'
		row.operator("easy.assetcreate", text='Particles - Spark', icon='PARTICLES').arg = 'fx.emitterSpark'
		row.operator("easy.assetcreate", text='Particles - Snow', icon='FREEZE').arg = 'fx.emitterSnow'

		row.operator("easy.assetcreate", text='Post-Processing 2D Filters', icon='TEXTURE' ).arg = 'fx.2DFilter'

		row = layout.row()
		row.label('Objects:')
		col = layout.column(align=True)
		col.operator("easy.assetcreate", text='Barrel-Wood').arg = 'barrel.BarrelWood'
		col.operator("easy.assetcreate", text='Barrel-Wood-Faded').arg = 'barrel.BarrelWood2'
		col.operator("easy.assetcreate", text='Barrel-Metal-Blue').arg = 'barrel.BarrelOilBlue'
		col.operator("easy.assetcreate", text='Barrel-Metal-Red').arg = 'barrel.BarrelOilRed'
		col.operator("easy.assetcreate", text='Barrel-Metal-Red-Yellow').arg = 'barrel.BarrelOilRed2'
		col.operator("easy.assetcreate", text='Barrel-Metal-Galvanized').arg = 'barrel.BarrelOilGalvanized'
		
		col = layout.column(align=True)
		col.operator("easy.assetcreate", text='Concrete-Divider').arg = 'concrete.ConcreteDivider'
		col.operator("easy.assetcreate", text='Concrete-Block1').arg = 'concrete.ConcreteBlock1'
		col.operator("easy.assetcreate", text='Concrete-Block2').arg = 'concrete.ConcreteBlock2'
		col.operator("easy.assetcreate", text='Concrete-Block3').arg = 'concrete.ConcreteBlock3'

		col = layout.column(align=True)
		col.operator("easy.assetcreate", text='Wood-Pallet').arg = 'wood.Pallet'
		
		

		row = layout.row()
		
		# row.label('Assets:')
		# template_list now takes two new args.
		# The first one is the identifier of the registered UIList to use (if you want only the default list,
		# with no custom draw code, use "UI_UL_list").
		# layout.template_list("UI_UL_list", "assetid", obj, "material_slots", obj, "active_material_index")


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

		row = layout.row()
		rows = len(obj.material_slots)
		if rows > 1:
			row.template_list("MATERIAL_UL_matslots", "", obj, "material_slots", obj, "active_material_index", rows=rows)

		# material datablock manager
		row = layout.row()
		layout.template_ID_preview(obj, "active_material", new="easy.matcreate")

		# material editor
		row = layout.row()
		mat = obj.material_slots[obj.active_material_index].material

		# bail code
		if not mat:
			return
		if 'uberMaterial' not in mat:
			row.label('Not an UberMaterial', icon='ERROR')
			return

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
		obj = context.object
		layout = self.layout

		# bail on wrong display mode
		if context.scene.game_settings.material_mode != 'GLSL':
			return

		# bail on no mat slot
		if not context.active_object.material_slots:
			return

		# material editor
		row = layout.row()
		mat = obj.material_slots[obj.active_material_index].material

		# bail code
		if not mat:
			return
		
		if 'uberMaterial' not in mat:
			# row.label('Not an UberMaterial', icon='ERROR')
			return
		
		row.prop(mat, 'use_transparency', 'Transparent')
		if mat.use_transparency:
			game = mat.game_settings
			row.prop(game, 'alpha_blend', text='Blending')

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

	arg = bpy.props.StringProperty(options={'HIDDEN'})
	
	def execute(self, context):
		
		objType, option = self.arg.split('.')

		# cleanup before we start
		bpy.ops.object.select_all(action='DESELECT')

		if objType == 'camera':
			obj = easyAsset.createCamera(option)
		elif objType == 'light':
			obj = easyAsset.createLight(option)
		elif objType == 'fx':
			obj = easyAsset.createFX(option)
		elif objType == 'barrel':
			obj = easyAsset.createBarrel(option)
		elif objType == 'concrete':
			obj = easyAsset.createConcrete(option)
		elif objType == 'wood':
			obj = easyAsset.createWood(option)
		else:
			obj = 'Sorry, not implemented yet.'

		if not obj:
			self.report({'ERROR'}, 'Error Importing this model.')
			return {'CANCELLED'}
		else:
			obj.select = True
			bpy.context.scene.objects.active = obj
			return {'FINISHED'}
		

