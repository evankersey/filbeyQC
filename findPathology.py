#!/usr/bin/env python
#
# creates mask of bad voxels
#
# 4/15/2019
# Evan Kersey

import sys
import numpy as np
import nibabel as nib
import time

## gets nifti as input
input_img=sys.argv[1]
voxel_std = float(sys.argv[2])
clust_size = int(sys.argv[3])

#load nifti to object
img = nib.load(input_img)
img_data = img.get_data()
data_obj = img.dataobj

## get dimensions
x_len = data_obj.shape[0]
y_len = data_obj.shape[1]
z_len = data_obj.shape[2]

#creates a list of all nonzero intensities, used to calculate std/mean
voxelValsList = []
for z in range(0, z_len):
	for y in range(0, y_len):
		for x in range(0, x_len):
			if img_data[x,y,z]:
				voxelValsList.append(img_data[x,y,z])

meanIntensity = np.mean(voxelValsList)
stdIntensity = np.std(voxelValsList)

threshold = meanIntensity - (voxel_std * stdIntensity)

#list of all coordinates below threshold
flagList = []
for z in range(0, z_len):
	for y in range(0, y_len):
		for x in range(0, x_len):
			if img_data[x,y,z]:
				if img_data[x,y,z] < threshold:
					flagList.append([x,y,z])
#recursive function, finds clusters in 3D 
def checkContig(pt, flagList, clustList):
	x = pt[0]
	y = pt[1]
	z = pt[2]
	points = [[x,y,z-1], [x+1,y,z-1], [x+1,y+1,z-1], [x+1,y-1,z-1], [x-1,y,z-1], [x-1,y+1,z-1], [x-1,y-1,z-1], [x,y+1,z-1], [x,y-1,z-1], [x,y,z+1], [x+1,y,z+1], [x+1,y+1,z+1], [x+1,y-1,z+1], [x-1,y,z+1], [x-1,y+1,z+1], [x-1,y-1,z+1], [x,y+1,z+1], [x,y-1,z+1], [x,y-1,z], [x+1,y-1,z], [x+1,y-1,z+1], [x+1,y-1,z-1], [x-1,y-1,z], [x-1,y-1,z+1], [x-1,y-1,z-1], [x,y-1,z+1], [x,y-1,z-1], [x,y+1,z], [x+1,y+1,z], [x+1,y+1,z+1], [x+1,y+1,z-1], [x-1,y+1,z], [x-1,y+1,z+1], [x-1,y+1,z-1], [x,y+1,z+1], [x,y+1,z-1], [x-1,y,z], [x-1,y+1,z], [x-1,x+1,z+1], [x-1,y+1,z-1], [x-1,y-1,z], [x-1,y-1,z+1], [x-1,y-1,z-1], [x-1,y,z+1], [x-1,y,z-1], [x+1,y,z], [x+1,y+1,z], [x+1,y+1,z+1], [x+1,y+1,z-1], [x+1,y-1,z], [x+1,y-1,z+1], [x+1,y-1,z-1], [x+1,y,z+1], [x+1,y,z-1]]
	for coord in points:
		if coord in flagList and coord not in clustList:
			clustList.append(coord)	
			flagList.remove(coord)
			checkContig(coord, flagList, clustList)

clustList2 = []
for xyz in flagList:
	clustList = []	
	checkContig(xyz, flagList, clustList)
	clustList2.append(clustList)
	

#print(clustList2)

for cluster in clustList2:
	if len(cluster) > clust_size:
		print(len(cluster))
		print(cluster)
		#print(img_data[cluster[0]])
		print()

maskImage = nib.Nifti1Image(new_data, img.affine, img.header)
type(maskImage)
