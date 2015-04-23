# ./examples/load_data_yt.py
# Required libraries:
# pip install yt 

#import yt
import thingking as tk  # loadtxt
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

from Halo import Halo
from mpl_toolkits.mplot3d import Axes3D


#prefix = "http://darksky.slac.stanford.edu/scivis2015/data/ds14_scivis_0128/"
#prefix = "../data/"
#ds = yt.load(prefix+"ds14_scivis_0128_e4_dt04_1.0000")
#print ds.all_data()
#ad = ds.all_data()
#p = yt.ProjectionPlot(ds, 'z', ('deposit','all_cic'))
#p.save()

PATH = "C:/Workspace/cs594/Project/data/rockstar/hlists/"

filenames = os.listdir(PATH) # returns list
haloList = {}

haloClusters = {}

trackedHaloID = 257;
trackedPosX = []; 
trackedPosY = []; 
trackedPosZ = []; 

initialHalos = {}
initialFile = True
for file in filenames:
	print "Loading file: '"+ file + "'"
	data = tk.loadtxt(PATH+file)

	for halo in data:
		# Add halo to dictionary
		testHalo = Halo(halo)
		if( testHalo.id in haloList ):
			print "Existing halo " + str(testHalo.id) + " found"
		else:
			haloList[testHalo.id] = testHalo
		
		# If halo has a host ID, append it to the host halos's client list
		if( testHalo.pid in haloList ):
			haloList[testHalo.pid].clients[testHalo.id] = testHalo
			
			haloClusters[testHalo.pid] = haloList[testHalo.pid]
			
		if( testHalo.id == trackedHaloID ):
			if( testHalo.desc_id != -1 ):
				trackedHaloID = testHalo.desc_id
				print "Halo " + str(testHalo.id) + " now following " + str(trackedHaloID)
				
				trackedPosX.append( testHalo.position[0] );
				trackedPosY.append( testHalo.position[1] );
				trackedPosZ.append( testHalo.position[2] );
				
		if( initialFile == True ):
			initialHalos[testHalo.id] = testHalo
		
	initialFile = False

print "Loaded " + str(len(haloList)) + " halos"

print "Counted " + str(len(haloClusters)) + " with children"

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

for i in haloClusters:
	childCount = len(haloClusters[i].clients)
	if( childCount > 15 ):
		print "Halo id: "+str(i) + " " + str(childCount)
		
# Topic 8 assignment 1 plotting code
fig = plt.figure()
	
p = fig.gca(projection='3d')
#p.set_xlim(0, 48)
#p.set_ylim(0, 48)
#p.set_zlim(0, 48)
p.set_xlabel( "X" )
p.set_ylabel( "Y" )
p.set_zlabel( "Z" )
	
#mpl.rcParams['legend.fontsize'] = 10
#title = "RK4 - Seed: " + str(seed) + " StepSize: " + str(step_size) + " nSteps: "+str(len(result))
#p.plot(x, y, z, label=title)
p.plot(trackedPosX, trackedPosY, trackedPosZ)
p.legend()
plt.show()