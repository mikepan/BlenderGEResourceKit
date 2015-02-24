import bpy

def createMaterial(context, name):
	mat = bpy.data.materials.new(name)

	# Diffuse with fresnel simulation
	mat.use_diffuse_ramp = True
	mat.diffuse_ramp_input = 'NORMAL'
	mat.diffuse_ramp_blend = 'MULTIPLY'
	mat.diffuse_ramp_factor = 0.4
	mat.diffuse_ramp.elements[0].color = [1,1,1,1]
	mat.diffuse_ramp.elements[1].color = [0,0,0,1]
	mat.diffuse_ramp.elements[0].position = 0.0
	mat.diffuse_ramp.elements[1].position = 1.0

	# alternative diffuse
	# mat.diffuse_shader = 'MINNAERT'
	# mat.darkness = 1.5

	# specular
	mat.specular_shader = 'BLINN'
	mat.specular_intensity = 0.0
	mat.specular_hardness = 1
	mat.specular_ior = 10.0

	# color map
	tex = bpy.data.textures.new(name+'.Col', type = 'IMAGE')
	tex.use_alpha = False
	mtex = mat.texture_slots.add()
	mtex.texture = tex
	mtex.texture_coords = 'UV'
	mtex.uv_layer = 'UVMap'
	mtex.use_map_color_diffuse = True 

	# normal map
	tex = bpy.data.textures.new(name+'.Nor', type = 'IMAGE')
	tex.use_alpha = False
	tex.use_normal_map = True
	mtex = mat.texture_slots.add()
	mtex.texture = tex
	mtex.texture_coords = 'UV'
	mtex.uv_layer = 'UVMap'
	mtex.use_map_normal = True
	mtex.use_map_color_diffuse = False

	# light map
	tex = bpy.data.textures.new(name+'.AO', type = 'IMAGE')
	tex.use_alpha = False
	mtex = mat.texture_slots.add()
	mtex.texture = tex
	mtex.texture_coords = 'UV'
	mtex.uv_layer = 'Lightmap'
	mtex.blend_type = 'MULTIPLY'
	mtex.use_map_color_spec = True

	# spec map (gloss map with color)
	specTexture = bpy.data.textures.new(name+'.Gloss', type = 'IMAGE')
	specTexture.use_alpha = False
	mtex = mat.texture_slots.add()
	mtex.texture = specTexture
	mtex.texture_coords = 'UV'
	mtex.uv_layer = 'UVMap'
	mtex.use_map_color_diffuse = False
	mtex.use_map_color_spec = True
	mtex.blend_type = 'COLOR'

	# gloss map (gloss map grayscale)
	mtex = mat.texture_slots.add()
	mtex.texture = specTexture
	mtex.texture_coords = 'UV'
	mtex.uv_layer = 'UVMap'
	mtex.use_map_color_diffuse = False
	mtex.use_map_specular = True
	mtex.specular_factor = 2.0
	mtex.use_map_hardness = True 
	mtex.hardness_factor = 2.0
	mtex.use_rgb_to_intensity = True
	mtex.use_stencil = True
	mtex.default_value = 1.0
	mtex.color = [1,1,1]

	# reflection map
	tex = bpy.data.textures.new(name+'.Env', type = 'IMAGE')
	tex.use_alpha = False
	mtex = mat.texture_slots.add()
	mtex.texture = tex
	mtex.texture_coords = 'REFLECTION'
	mtex.diffuse_color_factor = 0.75
	mtex.blend_type = 'MULTIPLY'

	return mat


def assignMaterial(context, mat):
	''' assign material to all selected objects, overriding all mat slots'''
	for obj in context.selected_objects:
		obj.data.materials.clear()
		obj.data.materials.append(mat)


def sanityCheck(context):
	''' returns error if selected objects has usable materials'''
	for obj in context.selected_objects:
		if obj.type != 'MESH':
			return 'Object is not a mesh, Aborted'
		for mat in obj.data.materials:
			if mat:
				return 'Object already has materials, Aborted.'
	return False

