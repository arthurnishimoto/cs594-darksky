# haloViewer.py
# Description: loads the halo list, renders as streamlines or points over time
#
# Class: CS 594 - Spring 2015
# System: Windows 8.1, Python 2.7.8 (Anaconda 2.1.0 - x64), VTK 6.1.0 (x64)
# Author: Arthur Nishimoto (anishi2)

import thingking as tk  # loadtxt
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

from Halo import Halo
from mpl_toolkits.mplot3d import Axes3D

# Settings ------------------------------------------------------------------------
# Number of timesteps deep to connect descendant halos to parent
# i.e. depth 0 will only track the ~58 halos that appear in the first file
# i.e. depth 1 will only track the halos that first appear in the first two files
maxDepth = 0

# File index number of the starting file and ending file to read
startFile = 0
endFileIndex = 100 # there are 88 files total

plotRK4 = False # Process velocities using RK4 instead of using the provided position data
euler = False # Process velocities using euler instead of RK4 (Requires plotRK4 to be enabled)

# Render as an animation over time instead of showing all timesteps as a streamline
showOverTime = False

# If showOverTime == true, also show previous timesteps instead of drawing only the current position
showPrevTimeTrails = False

# Start/end time of the animation 
startTime = 0
endTime = 100 # there are 88 files total

# Write halo positions
writeToFile = False

# Globals --------------------------------------------------------------------------
haloList = {}
haloClusters = {}
initialHalos = {}
initialFile = True

# Load the data -------------------------------------------------------------------
# Loads in the files and tracks halo descendant IDs of the host halo and allows the host
# halo to track the position of all decendant halos over time 
def loadData(maxDepth, startFileIndex, endFileIndex):
	global haloList
	global haloClusters
	global initialHalos
	global initialFile
	
	PATH = "C:/Workspace/cs594/Project/data/rockstar/hlists/"
	filenames = os.listdir(PATH) # returns list
	
	initialDepthCount = 0
	currentFileIndex = 0
	for file in filenames:
		if( startFileIndex > currentFileIndex or currentFileIndex > endFileIndex ):
			currentFileIndex = currentFileIndex + 1
			continue
		print "Loading file: "+str(currentFileIndex)+" '"+ file + "'"
		currentFileIndex = currentFileIndex + 1
		
		data = tk.loadtxt(PATH+file)

		for halo in data:
			# Add halo to dictionary
			testHalo = Halo(halo)
			if( testHalo.id in haloList ):
				print "Existing halo " + str(testHalo.id) + " found" # This dosen't happen
			else:
				haloList[testHalo.id] = testHalo
			
			# If halo has a host ID, append it to the host halos's client list
			if( testHalo.pid in haloList ):
				haloList[testHalo.pid].clients[testHalo.id] = testHalo
				
				haloClusters[testHalo.pid] = haloList[testHalo.pid]

			if( testHalo.desc_id != -1 ):
				for initHaloID in initialHalos:
					if( initialHalos[initHaloID].nextDesc_id == testHalo.id ):
						initialHalos[initHaloID].trackedPosX.append( testHalo.position[0] )
						initialHalos[initHaloID].trackedPosY.append( testHalo.position[1] )
						initialHalos[initHaloID].trackedPosZ.append( testHalo.position[2] )
						
						initialHalos[initHaloID].trackedVelX.append( testHalo.velocity[0] )
						initialHalos[initHaloID].trackedVelY.append( testHalo.velocity[1] )
						initialHalos[initHaloID].trackedVelZ.append( testHalo.velocity[2] )
						
						initialHalos[initHaloID].nextDesc_id = testHalo.desc_id
			#else:
			if( initialDepthCount <= maxDepth ):
				initialHalos[testHalo.id] = testHalo
				initialHalos[testHalo.id].nextDesc_id = testHalo.desc_id
		initialDepthCount = initialDepthCount + 1
		initialFile = False

# Topic 8: Assignment 1 -----------------------------------------------------------
def RK4(seed, step_size, num_steps, u, v, w):
	global euler
	print "\nRK4 start:"
		
	# Do stuff
	curPos = seed;
	flowPos = []

	for step in range(0, num_steps):
		if( step >= len(u) ):
			break
			
		scale = 0.0001
		
		velAtCurPos = [scale * u[step], scale * v[step], scale * w[step]]
		
		ex = curPos[0] + velAtCurPos[0] * step_size
		ey = curPos[1] + velAtCurPos[1] * step_size
		ez = curPos[2] + velAtCurPos[2] * step_size
		ePos = [ex,ey,ez] # Euler
		
		# a = v(p0) * 2 dt
		a = velAtCurPos * step_size * 2
		
		# b = v(p0+a/2) * 2 dt
		bu = (velAtCurPos[0] + a[0]/2) * step_size * 2
		bv = (velAtCurPos[1] + a[1]/2) * step_size * 2
		bw = (velAtCurPos[2] + a[2]/2) * step_size * 2
		b = [bu, bv, bw]
		
		# c = v(p0+b/2) * 2 dt
		cu = (velAtCurPos[0] + b[0]/2) * step_size * 2
		cv = (velAtCurPos[1] + b[1]/2) * step_size * 2
		cw = (velAtCurPos[2] + b[2]/2) * step_size * 2
		c = [cu, cv, cw]
		
		# d = v(p0+c/2) * 2 dt
		du = (velAtCurPos[0] + c[0]/2) * step_size * 2
		dv = (velAtCurPos[1] + c[1]/2) * step_size * 2
		dw = (velAtCurPos[2] + c[2]/2) * step_size * 2
		d = [du, dv, dw]
		
		
		x2 = curPos[0] + (a[0] + 2 * b[0] + 2 * c[0] + d[0]) / 6
		y2 = curPos[1] + (a[1] + 2 * b[1] + 2 * c[1] + d[1]) / 6
		z2 = curPos[2] + (a[2] + 2 * b[2] + 2 * c[2] + d[2]) / 6
		
		if( euler ):
			nexPos = ePos
		else:
			nexPos = [x2,y2,z2]
		
		flowPos.append(nexPos)
		
		curPos = [nexPos[0], nexPos[1], nexPos[2]]
	# Return a list of 3D points
	return flowPos
	
# Program Specific ----- -----------------------------------------------------------
loadData(maxDepth, startFile, endFileIndex)

print "Loaded " + str(len(haloList)) + " halos"
print "Counted " + str(len(haloClusters)) + " with children"

# Calculate min/max/avg child count
maxChildren = 0
minChildren = 9999999999999999999999
avgChildren = 0
for i in haloClusters:
	childCount = len(haloClusters[i].clients)
	if( childCount > maxChildren ):
		maxChildren = childCount
	if( childCount < minChildren ):
		minChildren = childCount	
	avgChildren += childCount

avgChildren = avgChildren / len(haloClusters)

print "Max " + str(maxChildren)
print "Min " + str(minChildren)
print "Avg " + str(avgChildren)

#for i in haloClusters:
#	childCount = len(haloClusters[i].clients)
#	if( childCount > 15 ):
#		print "Halo id: "+str(i) + " " + str(childCount)

if( writeToFile ):
	resultsPath = "./results/"
	for initHaloID in initialHalos:
		curhalo = initialHalos[initHaloID]
		f = open('positions_halo_'+str(initHaloID), 'w')
		for i in curhalo.trackedPosX:
			x = curhalo.trackedPosX[int(i)]
			y = curhalo.trackedPosY[int(i)]
			z = curhalo.trackedPosZ[int(i)]
			f.write(str(x) + " " + str(y) + " " + str(z)+"\n")
		f.close()



print "Tracked " + str(len(initialHalos))
count = 0

# Not showing over time, don't bother to render more frames
if( showOverTime == False ):
	startTime = 0
	endTime = 1
	
for t in range(startTime, endTime):
	fig = plt.figure()
	
	p = fig.gca(projection='3d')
	#p.set_xlim(0, 48)
	#p.set_ylim(0, 48)
	#p.set_zlim(0, 48)
	p.set_xlabel( "X" )
	p.set_ylabel( "Y" )
	p.set_zlabel( "Z" )
	mpl.rcParams['legend.fontsize'] = 10

	for initHaloID in initialHalos:
		curHalo = initialHalos[initHaloID]
		
		# RK4
		if( plotRK4 ):
			initPos = [curHalo.trackedPosX[0],curHalo.trackedPosY[0], curHalo.trackedPosZ[0]];
			rk4pos = RK4( initPos, 1, 1000, curHalo.trackedVelX, curHalo.trackedVelY, curHalo.trackedVelZ );
			
			# Format for plot
			rk4x = []
			rk4y = []
			rk4z = []
			for index in range(0,len(rk4pos)):
				rk4x.append(rk4pos[index][0])
				rk4y.append(rk4pos[index][1])
				rk4z.append(rk4pos[index][2])
				
			title = str(curHalo.id) + " (RK4)"
			p.plot(rk4x, rk4y, rk4z, label=title)
		else:
			title = str(curHalo.id) + ""
			
			# Plot time from 0 to time t
			if( showOverTime ):
				if( showPrevTimeTrails ):
					p.plot(curHalo.trackedPosX[0:t], curHalo.trackedPosY[0:t], curHalo.trackedPosZ[0:t], label=title)
				else:
					p.plot(curHalo.trackedPosX[t], curHalo.trackedPosY[t], curHalo.trackedPosZ[t], label=title)
			else:
				p.plot(curHalo.trackedPosX, curHalo.trackedPosY, curHalo.trackedPosZ, label=title)
		count = count + 1
		#if(count > 100):
		#	break
	
	# use this to spin the plot
	#p.view_init(elev=10., azim=t)
	
	# Save figure
	print "Generating figure: " + str(t)
	plt.savefig("figure_"+str(t)+".png", transparent=True)
	
	# Clear plot for next time stamp
	plt.clf() # Clears plots
	
# Potentially used for rendering multiple images
#for ii in xrange(0,360,1):
#	p.view_init(elev=10., azim=ii)
#	plt.savefig("movie"+str(ii)+".png", transparent=True)
#p.legend()
#plt.show()