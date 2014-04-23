from bge import logic
from bge import events
from bge import render

def init():
	'''Called at start of game'''

	scene = logic.getCurrentScene()
	scene.post_draw = [postDraw]
	scene.pre_draw = [preDraw]


def loop():
	'''Called every logic tick'''

	# Drop to debug console
	keyboard = logic.keyboard.events
	if keyboard[events.ACCENTGRAVEKEY] == logic.KX_SENSOR_JUST_DEACTIVATED:
		from pprint import pprint
		import code
		namespace = globals().copy()
		namespace.update(locals())
		code.interact(local=namespace)


def preDraw():
	'''called just before drawing screen'''
	pass


def postDraw():
	'''called just after drawing screen'''
	pass