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
import sys
import datetime

from Halo import Halo
from mpl_toolkits.mplot3d import Axes3D

# Settings ------------------------------------------------------------------------
# Number of timesteps deep to connect descendant halos to parent
# i.e. depth 0 will only track the ~58 halos that appear in the first file
# i.e. depth 1 will only track the halos that first appear in the first two files
maxDepth = 0

# File index number of the starting file and ending file to read
startFileIndex = 0
endFileIndex = 100 # there are 88 files total

plotRK4 = True # Process velocities using RK4 instead of using the provided position data
euler = False # Process velocities using euler instead of RK4 (Requires plotRK4 to be enabled)

# Render as an animation over time instead of showing all timesteps as a streamline
showOverTime = True

# If showOverTime == true, also show previous timesteps instead of drawing only the current position
showPrevTimeTrails = False

spinPlot = False

# Start/end time of the animation 
startTime = 0
endTime = 100 # there are 88 files total

# Write halo positions
writeToFile = False

generateFigures = False

nPartitions = 1

# Globals --------------------------------------------------------------------------
haloList = {}
haloClusters = {}
fig = plt.figure()
p = fig.gca(projection='3d')

# Load the data -------------------------------------------------------------------
# Loads in the files and tracks halo descendant IDs of the host halo and allows the host
# halo to track the position of all decendant halos over time 
def loadData(nodeID, maxDepth, startFileIndex, endFileIndex, divisions):
	global haloList
	global haloClusters
	global spinPlot
	global p
	
	initialHalos = {}
	
	PATH = "C:/Workspace/cs594/Project/data/rockstar/hlists/"
	#filenames = os.listdir(PATH) # returns list
	
	#PATH = "http://darksky.slac.stanford.edu/scivis2015/data/ds14_scivis_0128/rockstar/hlists/"
	print "Loading data from PATH: " + PATH
	print "Max Depth: " + str(maxDepth)
	filenames = []
	for i in range(12, 99):
		filenames.append("hlist_0."+str(i)+"000.list")
		#print PATH+"hlist_0."+str(i)+"000.list"
	#filenames.append("hlist_1.00000.list")

	initialDepthCount = 0
	currentFileIndex = 0
	for file in filenames:
		if(startFileIndex > currentFileIndex or currentFileIndex > endFileIndex):
			currentFileIndex = currentFileIndex + 1
			continue

		if( generateFigures ):
			fig = plt.figure()
			p = fig.gca(projection='3d')
			#p.set_xlim(10, 50)
			#p.set_ylim(10, 50)
			#p.set_zlim(10, 50)
			p.set_xlabel( "X" )
			p.set_ylabel( "Y" )
			p.set_zlabel( "Z" )
			mpl.rcParams['legend.fontsize'] = 10
	
		print "["+str(datetime.datetime.now())+"] Loading file: "+str(currentFileIndex)+" '"+ file + "'"
		data = tk.loadtxt(PATH+file)
		
		rk4pos = []
		dataLength = len(data)
		
		dataSegmentSize = dataLength / divisions
		remainder = dataLength % divisions
		print "Node: " + str(nodeID)
		print "   Data length: " + str(dataLength)
		print "   Data divisions: " + str(divisions)
		print "   Data segment size: " + str(dataSegmentSize)
		print "   remainder: " + str(remainder)
		
		startIndex = dataSegmentSize * nodeID
		
		if( nodeID == divisions - 1 ):
			endIndex = (dataSegmentSize * (nodeID+1)) + remainder
		else:
			endIndex = (dataSegmentSize * (nodeID+1)) - 1
			
		print "   index: " + str(startIndex) + " to " + str(endIndex)
		
		for halo in data[startIndex:endIndex+1]:
			# Add halo to dictionary
			curHalo = Halo(halo)
			if( curHalo.id in haloList ):
				print "Existing halo " + str(curHalo.id) + " found" # This dosen't happen
			else:
				haloList[curHalo.id] = curHalo
			
			# If halo has a host ID, append it to the host halos's client list
			if( curHalo.pid in haloList ):
				haloList[curHalo.pid].clients[curHalo.id] = curHalo
				
				haloClusters[curHalo.pid] = haloList[curHalo.pid]

			#if( curHalo.desc_id != -1 ):
			for initHaloID in initialHalos:
				if( initialHalos[initHaloID].nextDesc_id == curHalo.id ):
					initialHalos[initHaloID].trackedPosX.append( curHalo.position[0] )
					initialHalos[initHaloID].trackedPosY.append( curHalo.position[1] )
					initialHalos[initHaloID].trackedPosZ.append( curHalo.position[2] )
							
					initialHalos[initHaloID].trackedVelX.append( curHalo.velocity[0] )
					initialHalos[initHaloID].trackedVelY.append( curHalo.velocity[1] )
					initialHalos[initHaloID].trackedVelZ.append( curHalo.velocity[2] )
					
					initialHalos[initHaloID].nextDesc_id = curHalo.desc_id
					
					initPos = [initialHalos[initHaloID].trackedPosX[0],initialHalos[initHaloID].trackedPosY[0], initialHalos[initHaloID].trackedPosZ[0]];
					rk4pos = RK4( initPos, 1, 1000, initialHalos[initHaloID].trackedVelX, initialHalos[initHaloID].trackedVelY, initialHalos[initHaloID].trackedVelZ );
					
					# Format for plot
					rk4x = []
					rk4y = []
					rk4z = []
					for index in range(0,len(rk4pos)):
						rk4x.append(rk4pos[index][0])
						rk4y.append(rk4pos[index][1])
						rk4z.append(rk4pos[index][2])
					if( generateFigures ):
						#p.plot(rk4x[0:currentFileIndex], rk4y[0:currentFileIndex], rk4z[0:currentFileIndex])
						p.plot([rk4x[currentFileIndex-1]], [rk4y[currentFileIndex-1]], [rk4z[currentFileIndex-1]])
			if( initialDepthCount <= maxDepth ):
				initialHalos[curHalo.id] = curHalo
				initialHalos[curHalo.id].nextDesc_id = curHalo.desc_id
	
		if( generateFigures ):
			if( spinPlot ):
				p.view_init(elev=10., azim= currentFileIndex / 88.0 * 360)
			else:
				p.view_init(elev=10., azim=33)
		
			# Save figure
			print "["+str(datetime.datetime.now())+"] Generating figure: " + str(currentFileIndex)
			plt.savefig("figure_"+str(currentFileIndex)+".png", transparent=True)
			
			# Clear plot for next time stamp
			plt.clf() # Clears plots
		
		initialDepthCount = initialDepthCount + 1
		currentFileIndex = currentFileIndex + 1
	return initialHalos
	
# Topic 8: Assignment 1 -----------------------------------------------------------
def RK4(seed, step_size, num_steps, u, v, w):
	global euler
	#print "\nRK4 start:"
		
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
if len(sys.argv) == 2:
	nPartitions = int(sys.argv[1])
	
	print 'nPartitions:', nPartitions
if( len(sys.argv) == 5 ):
	maxDepth = int(sys.argv[1])
	startFileIndex = int(sys.argv[2])
	endFileIndex = int(sys.argv[3])
	nPartitions = int(sys.argv[4])
else:
	print "Expecting 2 arguments: program, nPartitions"
	print "or 5 arguments: program, maxDepth, startFileIndex, endFileIndex, nPartitions"
	print "Received " + str(len(sys.argv))
	sys.exit("Ending application")

haloPartitions = {}

for partitionID in range(0, nPartitions):
	print "Process: " + str(partitionID)
	haloPartitions[partitionID] = loadData( partitionID, maxDepth, startFileIndex, endFileIndex, nPartitions)

print "Loaded " + str(len(haloList)) + " halos"
print "Counted " + str(len(haloClusters)) + " with children"

#( writeToFile ):

mergedHaloList = {}

print "Merging halo lists"
for partitionID in haloPartitions:
	currentHaloList = haloPartitions[partitionID]
	for haloID in currentHaloList:
		curhalo = currentHaloList[haloID]
		
		if( haloID in mergedHaloList):
			print "Existing halo " + str(curhalo.id) + " found" # This dosen't happen
		else:
			mergedHaloList[haloID] = curhalo
			
print "Merged " + str(len(mergedHaloList)) + " halos"
for haloID in mergedHaloList:
	curhalo = mergedHaloList[haloID]
	
	f = open('./position_results/positions_halo_'+str(haloID), 'w')
	for i in range(0, len(curhalo.trackedPosX)):
		x = curhalo.trackedPosX[int(i)]
		y = curhalo.trackedPosY[int(i)]
		z = curhalo.trackedPosZ[int(i)]
		f.write(str(x) + " " + str(y) + " " + str(z)+" "+str(curhalo.id) + " " + str(curhalo.nextDesc_id)+"\n")
	f.close()

sys.exit()

for t in range(startTime, endTime):
	fig = plt.figure()
	
	p = fig.gca(projection='3d')
	p.set_xlim(45, 60)
	p.set_ylim(10, 60)
	p.set_zlim(40, 60)
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
			
			if( rk4pos[index][0] > 50 and rk4pos[index][2] > 40 ):
				if( showOverTime ):
					if( showPrevTimeTrails ):
						p.plot(rk4x[0:t], rk4y[0:t], rk4z[0:t], label=title)
					else:
						p.plot([rk4x[t]], [rk4y[t]], [rk4z[t]], label=title)
				else:
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
	
	# use this to spin the plot
	if( spinPlot ):
		p.view_init(elev=10., azim= t / 100.0 * 360)
	else:
		p.view_init(elev=10., azim=33)
		
	# Save figure
	print "Generating figure: " + str(t)
	plt.savefig("figure_"+str(t)+".png", transparent=True)
	
	# Clear plot for next time stamp
	plt.clf() # Clears plots
if( spinPlot ):
	for t in range(0, 360):
		p.view_init(elev=10., azim= 33+t)
		print "["+str(datetime.datetime.now())+"] Generating figure: " + str(87+t)
		plt.savefig("figure_"+str(87+t)+".png", transparent=True)
		
#p.legend()
#plt.show()