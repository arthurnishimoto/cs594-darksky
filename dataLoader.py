import thingking as tk  # loadtxt
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

from Halo import Halo
from mpl_toolkits.mplot3d import Axes3D


haloList = {}
haloClusters = {}
initialHalos = {}
initialFile = True

# Load the data -------------------------------------------------------------------
def loadData():
	global haloList
	global haloClusters
	global initialHalos
	global initialFile
	
	PATH = "C:/Workspace/cs594/Project/data/rockstar/hlists/"
	filenames = os.listdir(PATH) # returns list

	for file in filenames:
		print "Loading file: '"+ file + "'"
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
					
			if( initialFile == True ):
				initialHalos[testHalo.id] = testHalo
				initialHalos[testHalo.id].nextDesc_id = testHalo.desc_id
		initialFile = False

# Topic 8: Assignment 1 -----------------------------------------------------------
def RK4(self, seed, step_size, num_steps, u, v, w):
	print "\nRK4 start:"
	
	# Check if seed is within volume boundary
	validSeed = True
	if( seed[0] < 0 or seed[0] >= u.shape[0] ):
		print "Seed X value "+str(seed[0])+" out of bounds"
		validSeed = False
	if( seed[1] < 0 or seed[1] >= v.shape[1] ):
		print "Seed Y value "+str(seed[1])+" out of bounds"
		validSeed = False
	if( seed[2] < 0 or seed[2] >= w.shape[2] ):
		print "Seed Z value "+str(seed[2])+" out of bounds"
		validSeed = False
		
	if( validSeed == False ):
		print "Valid Volume Boundaries: 0 - " + str(w.shape[2]-1)
		return
		
	# Do stuff
	curPos = seed;
	flowPos = []
	
	for step in range(0, num_steps):
		velAtCurPos = [u[int(curPos[0])][int(curPos[1])][int(curPos[2])], v[int(curPos[0])][int(curPos[1])][int(curPos[2])], w[int(curPos[0])][int(curPos[1])][int(curPos[2])]]
		
		ex = curPos[0] + velAtCurPos[0] * step_size
		ey = curPos[1] + velAtCurPos[1] * step_size
		ez = curPos[2] + velAtCurPos[2] * step_size
		ePos = [ex,ey,ez] # Euler
		
		# a = v(p0) * 2 dt
		a = velAtCurPos * step_size * 2
		
		# b = v(p0+a/2) * 2 dt
		bu = (velAtCurPos[0] + u[int(a[0])][int(a[1])][int(a[2])]/2) * step_size * 2
		bv = (velAtCurPos[1] + v[int(a[0])][int(a[1])][int(a[2])]/2) * step_size * 2
		bw = (velAtCurPos[2] + w[int(a[0])][int(a[1])][int(a[2])]/2) * step_size * 2
		b = [bu, bv, bw]
		
		# c = v(p0+b/2) * 2 dt
		cu = (velAtCurPos[0] + u[int(b[0])][int(b[1])][int(b[2])]/2) * step_size * 2
		cv = (velAtCurPos[1] + v[int(b[0])][int(b[1])][int(b[2])]/2) * step_size * 2
		cw = (velAtCurPos[2] + w[int(b[0])][int(b[1])][int(b[2])]/2) * step_size * 2
		c = [cu, cv, cw]
		
		# d = v(p0+c/2) * 2 dt
		du = (velAtCurPos[0] + u[int(c[0])][int(c[1])][int(c[2])]/2) * step_size * 2
		dv = (velAtCurPos[1] + v[int(c[0])][int(c[1])][int(c[2])]/2) * step_size * 2
		dw = (velAtCurPos[2] + w[int(c[0])][int(c[1])][int(c[2])]/2) * step_size * 2
		d = [du, dv, dw]
		
		x2 = curPos[0] + (a[0] + 2 * b[0] + 2 * c[0] + d[0]) / 6
		y2 = curPos[1] + (a[1] + 2 * b[1] + 2 * c[1] + d[1]) / 6
		z2 = curPos[2] + (a[2] + 2 * b[2] + 2 * c[2] + d[2]) / 6
		
		nexPos = [x2,y2,z2]
			
		# Check that next position is in volume
		if( nexPos[0] < 0 or nexPos[0] >= u.shape[0] ):
			print "Position out of bounds on step " + str(step) + " of max: " + str(num_steps)
			break
		if( nexPos[1] < 0 or nexPos[1] >= v.shape[1] ):
			print "Position out of bounds on step " + str(step) + " of max: " + str(num_steps)
			break
		if( nexPos[2] < 0 or nexPos[2] >= w.shape[2] ):
			print "Position out of bounds on step " + str(step) + " of max: " + str(num_steps)
			break
		
		flowPos.append(nexPos)
		
		curPos = [nexPos[0], nexPos[1], nexPos[2]]
	# Return a list of 3D points
	return flowPos
	
# Program Specific ----- -----------------------------------------------------------
loadData()

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

# Write halo positions
writeToFile = False

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

# Topic 8 assignment 1 plotting code
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
	title = str(curHalo.id)
	p.plot(curHalo.trackedPosX, curHalo.trackedPosY, curHalo.trackedPosZ, label=title)

# Potentially used for rendering multiple images
#for ii in xrange(0,360,1):
#        ax.view_init(elev=10., azim=ii)
 #       savefig("movie"%ii+".png")
p.legend()
plt.show()