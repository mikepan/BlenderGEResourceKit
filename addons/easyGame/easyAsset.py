import bpy

from math import *
import os


def createCamera(option):
	ops = bpy.ops

	if option == 'fps':
		ops.object.camera_add(rotation=(pi/2, 0, 0))
	if option == 'orbit':
		ops.object.empty_add(type='SPHERE')

	obj = bpy.context.active_object

	# mouse look
	sensors, actuators = makeLogicBrick(obj, 'ALWAYS', 'LOGIC_AND', 'MOUSE')
	actuators[0].mode = 'LOOK'

	if option == 'fps':
		# walk
		sensors, actuators = makeLogicBrick(obj, ('KEYBOARD', 'KEYBOARD'), 'LOGIC_OR', 'MOTION')
		sensors[0].key = 'UP_ARROW'
		sensors[1].key = 'W'
		actuators[0].name = 'Forward'
		actuators[0].offset_location[2] = -0.2

		sensors, actuators = makeLogicBrick(obj, ('KEYBOARD', 'KEYBOARD'), 'LOGIC_OR', 'MOTION')
		sensors[0].key = 'DOWN_ARROW'
		sensors[1].key = 'S'
		actuators[0].name = 'Back'
		actuators[0].offset_location[2] = 0.2

		sensors, actuators = makeLogicBrick(obj, ('KEYBOARD', 'KEYBOARD'), 'LOGIC_OR', 'MOTION')
		sensors[0].key = 'LEFT_ARROW'
		sensors[1].key = 'A'
		actuators[0].name = 'Left'
		actuators[0].offset_location[0] = -0.2

		sensors, actuators = makeLogicBrick(obj, ('KEYBOARD', 'KEYBOARD'), 'LOGIC_OR', 'MOTION')
		sensors[0].key = 'RIGHT_ARROW'
		sensors[1].key = 'D'
		actuators[0].name = 'Right'
		actuators[0].offset_location[0] = 0.2

		obj.name = 'GECamera.FPS'

		return obj

	if option == 'orbit':
		# add camera and parent
		parentObj = obj
		ops.object.camera_add(rotation=(pi/2, 0,0), location=(0,0,0))
		ops.transform.translate(value=(0,-10,0))
		childObj = bpy.context.active_object
		childObj.parent = parentObj
		childObj.select = True
		parentObj.select = True
		childObj.name = 'GECamera.Orbit'
		parentObj.name = 'GECamera.Pivot'

		return parentObj



def createLight(option):

	if option == 'cycle':
		obj = checkExists('GECycle.Target')
		if obj: return obj
		obj = checkExists('GECycle.Sun')
		if obj: return obj
		obj = checkExists('GECycle.Fill')
		if obj: return obj

		obj = loadAsset('fx.blend', ('GECycle.Target', 'GECycle.Sun', 'GECycle.Fill'))
	
	if option == 'soft':
		obj = checkExists('GESoftLight')
		if obj: return obj

		obj = loadAsset('fx.blend', ('GESoftLight.0', 'GESoftLight.1', 'GESoftLight.2', 'GESoftLight.3', 'GESoftLight.4'))
	
	return obj


def createFX(option):
	if option == '2DFilter':
		obj = checkExists('2DFilter')
		if obj: return obj

	if option.startswith('emitter'):
		obj = loadAsset('fx.blend', (option))
		option = option.replace('emitter', 'particle')
		objParticle = loadAsset('fx.blend', (option))


		layers = 20*[False]
		layers[19] = True
		objParticle.layers = layers
		return obj

	obj = loadAsset('fx.blend', (option))
	return obj


def createBarrel(option):
	obj = loadAsset('barrels.blend', (option))
	return obj


def createConcrete(option):
	obj = loadAsset('concrete.blend', (option))
	return obj


def checkExists(name):
	for obj in bpy.context.scene.objects:
		if name in obj.name:
			return obj
	return False


def loadAsset(filename, objList):

	scriptPath = os.path.realpath(__file__)
	assetPath = os.path.join(os.path.dirname(scriptPath), 'asset', filename)
	
	try:
		with bpy.data.libraries.load(assetPath)	as (data_from, data_to):
			data_to.objects = [name for name in data_from.objects if name in objList]

	except:
		return 'Asset file not found'

	for obj in data_to.objects:
		bpy.context.scene.objects.link(obj)

	return obj


def makeLogicBrick(obj, s, c, a, pulse=True):
	logic = bpy.ops.logic
	sensorsList = []
	actuatorsList = []

	# create controller first
	logic.controller_add(type=c)
	controller = obj.game.controllers[-1]

	# add sensors
	if type(s) is str: s = [s]
	for i in s:
		logic.sensor_add(type=i)
		sensor = obj.game.sensors[-1]
		sensor.use_pulse_true_level = pulse
		sensor.link(controller)
		sensorsList.append(sensor)	
	
	# add actuators
	if type(a) is str: a = [a]
	for i in a:
		logic.actuator_add(type=i)
		actuator = obj.game.actuators[-1]
		actuator.link(controller)
		actuatorsList.append(actuator)	

	return sensorsList, actuatorsList
