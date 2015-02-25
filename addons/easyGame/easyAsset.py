import bpy

from math import *
import os


def makeLogicBrick(obj, s, controller, a, pulse=True):
	logic = bpy.ops.logic
	sensorsList = []
	actuatorsList = []

	# create controller first
	logic.controller_add(type=controller)
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

	if option == 'orbit':
		# add camera and parent
		parentObj = obj
		ops.object.camera_add(rotation=(pi/2, 0,0), location=(0,0,0))
		ops.transform.translate(value=(0,-10,0))
		childObj = bpy.context.active_object
		childObj.parent = parentObj
		bpy.ops.object.select_all(action='DESELECT')
		childObj.select = True
		parentObj.select = True
		childObj.name = 'GECamera.Orbit'
		parentObj.name = 'GECamera.Pivot'
		bpy.context.scene.objects.active = parentObj



def createLight(option):
	error = None

	if option == 'cycle':
		error = checkExists('GECycle.Target')
		if error: return error
		error = checkExists('GECycle.Sun')
		if error: return error
		error = checkExists('GECycle.Fill')
		if error: return error

		error = loadAsset('asset.blend', ('GECycle.Target', 'GECycle.Sun', 'GECycle.Fill'))

	return error


def createPost(option):
	error = checkExists('GEKit2DFilter')
	if error: return error

	error = loadAsset('2dfilters.blend', ('GEKit2DFilter'))
	return error


def checkExists(name):
	for obj in bpy.context.scene.objects:
		if name in obj.name:
			bpy.ops.object.select_all(action='DESELECT')
			obj.select = True
			bpy.context.scene.objects.active = obj
			return obj.name + ' already exists. Aborted.'
	return False


def loadAsset(filename, objList):

	scriptPath = os.path.realpath(__file__)
	assetPath = os.path.join(os.path.dirname(scriptPath), 'asset', filename)
	
	try:
		with bpy.data.libraries.load(assetPath)	as (data_from, data_to):
			# data_to.objects = data_from.objects
			data_to.objects = [name for name in data_from.objects if name in objList]

	except:
		return 'Asset file not found'

	for obj in data_to.objects:
		if obj.name in objList:
			bpy.context.scene.objects.link(obj)

	return False