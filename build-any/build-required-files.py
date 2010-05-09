#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import platform
import shutil
import getopt

OSNAME=os.name
if OSNAME=='posix' and sys.platform=='darwin':
	OSNAME='mac'
required_files=[]
os.chdir(os.path.dirname(sys.argv[0]) + os.sep + '..')
opts, args = getopt.getopt(sys.argv[1:], 'o:d:')
outputFile = 'required-files.txt'
destFolder = None
for option, argument in opts:
	if option == '-o':
		outputFile = argument
	elif option == '-d':
		destFolder = argument
		if destFolder[-1] != os.sep:
			destFolder += os.sep
if os.path.exists(outputFile):
	os.remove(outputFile)
if os.path.exists('COPYING'):
	os.remove('COPYING')
shutil.copyfile('build-any/COPYING','./COPYING')
ext='py'
if OSNAME=='nt':
	ext='exe'
required_files.extend(['DamnVid.'+ext,'version.damnvid','COPYING'])
del ext
if OSNAME=='nt':
	shutil.copyfile('build-exe/DamnVid.exe.manifest','DamnVid.exe.manifest')
	required_files.append('DamnVid.exe.manifest')
required_dirs=['img','conf','locale']
def addDir(d):
	global required_files
	for f in os.listdir(d):
		if f.find('.svn')==-1 and f.find('.psd')==-1 and f.find('.noinclude')==-1 and f.find('.module.damnvid')==-1 and f.find('.bmp')==-1 and f.find('.ai')==-1 and f.find('.exe')==-1 and f.find('.zip')==-1 and f.find('fireworks.png')==-1:
			if os.path.isdir(d+os.sep+f):
				addDir(d+os.sep+f)
			else:
				required_files.append(d+os.sep+f)
for d in required_dirs:
	addDir(d)
for f in os.listdir('./'):
	if f[-15:]=='.module.damnvid':
		os.remove(f)
for f in os.listdir('./modules/'):
	if f[-15:]=='.module.damnvid':
		os.remove('./modules/'+f)
for f in os.listdir('./modules/'):
	if os.path.isdir('./modules/'+f) and f.find('.svn')==-1:
		p=os.popen('python build-any/module-package.py modules/'+f)
		for l in p.readlines():
			print l.strip()
		try:
			p.close()
		except:
			pass
for f in os.listdir('.'):
	if f[-15:]=='.module.damnvid':
		if os.path.lexists('modules/'+f):
			os.remove('modules/'+f)
		os.rename(f,'modules/'+f)
		required_files.append('modules'+os.sep+f)
if OSNAME=='nt':
	required_files.extend(['bin'+os.sep+'ffmpeg.exe','bin'+os.sep+'taskkill.exe','bin'+os.sep+'SDL.dll'])
elif OSNAME=='mac':
	required_files.append('bin'+os.sep+'ffmpegosx')
else:
	print 'ffmpeg binary ommitted on Linux'
	#if platform.architecture()[0]=='64bit':
		#required_files.append('bin'+os.sep+'ffmpeg64')
	#else:
		#required_files.append('bin'+os.sep+'ffmpeg')
required_file=open(outputFile,'w')
for f in required_files:
	required_file.write(f)
	if destFolder is not None:
		required_file.write(' ' + destFolder + os.path.dirname(f))
	required_file.write('\n')
required_file.close()
