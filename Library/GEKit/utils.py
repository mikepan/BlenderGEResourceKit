from bge import logic
from bgl import *

import os, subprocess, math, cProfile

def profile(cmd, g, l):
	cProfile.runctx(cmd, g, l, sort=1)

def clamp(var, minLimit = 0.0, maxLimit = 1.0):
	assert minLimit < maxLimit
	return max(min(var, maxLimit), minLimit)

def smoothstep(x):
	'''returns a smoothed float given an input between 0 and 1'''
	return x * x * (3-2*(x))

def computeFlatS(period, b, time, offset=1):
	"""compute the position of the object based on time using this curve:
	http://www.wolframalpha.com/input/?i=y%3D%281%2F%281%2Be%5E%28-10-x%29%29+%2B+1%2F%281%2Be%5E%2810-x%29%29%29"""
	time = (time%period)+offset
	time = (time-period/2)*(20/period)
	x = 1/(1+math.e**(-b-time))+1/(1+math.e**(b-time))
	x /= 2.0
	x += offset/10
	return x

def mix(a,b,factor):
	'''mix two number together using a factor'''
	if type(a) is list or type(a) is tuple:
		if len(a)==len(b)==2:
			return [a[0]*factor + b[0]*(1.0-factor), a[1]*factor + b[1]*(1.0-factor)]
		elif len(a)==len(b)==3:
			return [a[0]*factor + b[0]*(1.0-factor), a[1]*factor + b[1]*(1.0-factor), a[2]*factor + b[2]*(1.0-factor)]
		elif len(a)==len(b)==4:
			return [a[0]*factor + b[0]*(1.0-factor), a[1]*factor + b[1]*(1.0-factor), a[2]*factor + b[2]*(1.0-factor), a[3]*factor + b[3]*(1.0-factor)]
		else:
			raise Exception(ArithmeticError)
	else:
		return (a*factor + b*(1.0-factor))


