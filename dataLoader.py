# ./examples/load_data_yt.py
# Required libraries:
# pip install yt 

#import yt
import thingking as tk  # loadtxt
import os
from Halo import Halo

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

for file in filenames:
	print "Loading file: '"+ file + "'"
	data = tk.loadtxt(PATH+file)

	for halo in data:
		testHalo = Halo(halo)
		if( testHalo.id in haloList ):
			print "Existing halo " + str(testHalo.id) + " found"
		else:
			haloList[testHalo.id] = testHalo

		if( testHalo.pid in haloList ):
			haloList[testHalo.pid].clients[testHalo.id] = testHalo
			
			haloClusters[testHalo.pid] = haloList[testHalo.pid]
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