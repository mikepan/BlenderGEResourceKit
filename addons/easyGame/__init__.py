import bpy, imp

from easyGame import easyMaterial
from easyGame import easyAsset

imp.reload(easyMaterial)
imp.reload(easyAsset)


bl_info = {
	"name": "Easy Games Collection",
	"author": "Mike Pan",
	"version": (1, 0),
	"blender": (2, 70, 0),
	"location": "View3D > Tool Shelf > Easy Games Tab",
	"description": "Help make the game-creation process simpler.",
	"warning": "",
	"wiki_url": "",
	"category": "Game Engine"
}



def register():
	bpy.utils.register_class(BLEasyMaterial)
	bpy.utils.register_class(BLEasyAsset)
	# bpy.utils.register_class(BLSettings)
	bpy.utils.register_class(BLEasyMaterialCreate)
	bpy.utils.register_class(BLEasyAssetCreate)
	bpy.utils.register_class(BLAssetList)

def unregister():
	bpy.utils.unregister_class(BLEasyMaterial)
	bpy.utils.unregister_class(BLEasyAsset)
	# bpy.utils.unregister_class(BLSettings)
	bpy.utils.unregister_class(BLEasyMaterialCreate)
	bpy.utils.unregister_class(BLEasyAssetCreate)
	bpy.utils.unregister_class(BLAssetList)



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
	bl_category = "Easy Asset"

	def draw(self, context):
		layout = self.layout
		obj = context.object

		row = layout.row()
		row.label('Camera')
		row = layout.row(align=True)
		row.operator("easy.assetcreate", text='FPS Camera').arg = 'camera.fps'
		row.operator("easy.assetcreate", text='Orbit Camera').arg = 'camera.orbit'

		row = layout.row()
		row.label('Light')
		row = layout.row(align=True)
		row.operator("easy.assetcreate", text='Day-Night Cycle').arg = 'light.cycle'
		row.operator("easy.assetcreate", text='Soft Light').arg = 'light.soft'
		
		row = layout.row()
		row.label('Objects')
		row = layout.row(align=True)
		row.operator("easy.assetcreate", text='Plane Mirror').arg = 'obj.mirror'
		# row.operator("easy.assetcreate", text='Orbit Camera').arg = 'camera.orbit'


		row = layout.row()
		row.label('Effects')
		row = layout.row(align=True)
		row.operator("easy.assetcreate", text='Post-Processing 2D Filters').arg = 'post.main'

		# template_list now takes two new args.
		# The first one is the identifier of the registered UIList to use (if you want only the default list,
		# with no custom draw code, use "UI_UL_list").
		# layout.template_list("BLAssetList", "", obj, "material_slots", obj, "active_material_index")



# class BLSettings(GamePanel, bpy.types.Panel):
# 	"""Creates a Panel in the Object properties window"""
# 	bl_label = "Settings"
# 	bl_context = "objectmode"
#	bl_category = "Easy Settings"

# 	def draw(self, context):
# 		layout = self.layout
# 		obj = context.object
# 		row = layout.row()



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
		

class BLAssetList(bpy.types.UIList):
	# The draw_item function is called for each item of the collection that is visible in the list.
	#   data is the RNA object containing the collection,
	#   item is the current drawn item of the collection,
	#   icon is the "computed" icon for the item (as an integer, because some objects like materials or textures
	#   have custom icons ID, which are not available as enum items).
	#   active_data is the RNA object containing the active property for the collection (i.e. integer pointing to the
	#   active item of the collection).
	#   active_propname is the name of the active property (use 'getattr(active_data, active_propname)').
	#   index is index of the current item in the collection.
	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		ob = data
		slot = item
		ma = slot.material
		# draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
		if self.layout_type in {'DEFAULT', 'COMPACT'}:
			# You should always start your row layout by a label (icon + text), this will also make the row easily
			# selectable in the list!
			# We use icon_value of label, as our given icon is an integer value, not an enum ID.
			layout.label(ma.name if ma else "", icon_value=icon)
			# And now we can add other UI stuff...
			# Here, we add nodes info if this material uses (old!) shading nodes.
			if ma and not context.scene.render.use_shading_nodes:
				manode = ma.active_node_material
				if manode:
					# The static method UILayout.icon returns the integer value of the icon ID "computed" for the given
					# RNA object.
					layout.label("Node %s" % manode.name, icon_value=layout.icon(manode))
				elif ma.use_nodes:
					layout.label("Node <none>")
				else:
					layout.label("")
		# 'GRID' layout type should be as compact as possible (typically a single icon!).
		elif self.layout_type in {'GRID'}:
			layout.alignment = 'CENTER'
			layout.label("", icon_value=icon)

