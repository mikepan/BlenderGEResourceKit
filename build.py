# Run with Python3

import argparse
import sys
import os
import shutil
import time

ignored = shutil.ignore_patterns('__pycache__', '.git', '*.blend1', '*.blend2')


def copyFiles(useZip):
	startTime = time.time()
	pwd = os.path.dirname(os.path.realpath(__file__))
	print('Working directory: %s' % pwd)

	print('Creating release folder', end='...')
	sys.stdout.flush()
	try:
		os.makedirs('BGERsourceKit')
		print('Done')
	except Exception as E:
		print('Error', E)
		return

	print('Copying Files to release', end='...')
	sys.stdout.flush()
	shutil.copytree('Library', 'BGERsourceKit/Library', ignore=ignored)
	shutil.copytree('StarterTemplate', 'BGERsourceKit/GEStarterTemplate', ignore=ignored)


	name = time.strftime('%Y%m%d')

	if useZip:
		print('Zipping', end='...')
		sys.stdout.flush()
		shutil.make_archive(name, 'zip', 'BGERsourceKit')
	
	elapsedTime = time.time() - startTime
	print('Completed in %d seconds' % elapsedTime)


# -------------------------------------------------------------------------------

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Help build BGE Resource Kit from source')
	parser.add_argument('--zip', '-z', default=False, help='Compress release into one archive')
	args = parser.parse_args()

	useZip = args.zip

	copyFiles(useZip)
	