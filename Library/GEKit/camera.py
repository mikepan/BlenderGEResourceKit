#Blender Game Engine Resource Kit 2.7x
#Created by Mike Pan: mikepan.com

# Use mouse to look around
# W,A,S,D key to walk around
# E and C key to ascend and descend

from bge import logic
from bge import events
from bge import render

from . import utils

def look(cont):
	'''Called every logic tick'''

	owner = cont.owner
	currentScene = logic.getCurrentScene()

	# only apply to active camera
	if currentScene.active_camera is not owner\
		and currentScene.active_camera not in owner.children:
		return

	mouse = logic.mouse
	keyboard = logic.keyboard.events

	walkSpeed = owner['walkSpeed']
	lookSensitivity = owner['lookSpeed']
	RClickToLook = owner['RClickToLook']
	LClickToLook = owner['LClickToLook']
	lookSmoothing = utils.clamp(owner['lookSmoothing'], 0.0, 0.99)

	# Init code
	if "oldX" not in owner:
			# center mouse on first frame, create temp variables
			print('Using BGE Resource Kit - Mouselook Camera:', owner)
			mouse.position = (0.5,0.5)
			owner["oldX"] = 0.0
			owner["oldY"] = 0.0

	# loop code
	else:
		# round() is a hack to work around the drifting mouse bug
		x = round(0.5 - mouse.position[0], 2)
		y = round(0.5 - mouse.position[1], 2)

		# workaround for re-engaged mouse
		if logic.mouse.visible:
			x = 0
			y = 0
	
		# Smooth movement
		x = (owner['oldX']*lookSmoothing + x*(1.0-lookSmoothing))
		y = (owner['oldY']*lookSmoothing + y*(1.0-lookSmoothing))
	
		# use mouse clutching options
		if (RClickToLook and logic.mouse.events[events.RIGHTMOUSE] == logic.KX_INPUT_ACTIVE)\
			or \
			(LClickToLook and logic.mouse.events[events.LEFTMOUSE] == logic.KX_INPUT_ACTIVE)\
			or not (RClickToLook or LClickToLook):
			
			# apply the camera view transforms
			owner.applyRotation([0, 0, x * lookSensitivity], False)
			owner.applyRotation([y * lookSensitivity, 0, 0], True)
			
			# Center mouse in game window
			mouse.position = (0.5,0.5)
			logic.mouse.visible = False
		else:
			# release mouse
			logic.mouse.visible = True

		# save old value for smoothing use
		owner['oldX'] = x
		owner['oldY'] = y

		
		# keyboard control
		if keyboard[events.WKEY]:
			owner.applyMovement([0,0,-walkSpeed], True)
		if keyboard[events.SKEY]:
			owner.applyMovement([0,0, walkSpeed], True)
		if keyboard[events.AKEY]:
			owner.applyMovement([-walkSpeed,0,0], True)
		if keyboard[events.DKEY]:
			owner.applyMovement([walkSpeed,0,0], True)
		if keyboard[events.EKEY]:
			owner.applyMovement([0,walkSpeed/2,0], True)
		if keyboard[events.CKEY]:
			owner.applyMovement([0,-walkSpeed/2,0], True)