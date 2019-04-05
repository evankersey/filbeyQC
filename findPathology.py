#!/usr/bin/python3 env

# 2/18/19
# Evan Kersey
# code pulled from Venetian_Axial.py by Ryan Hammonds
# 
# to do:
#	efficiency, only parse mri once, store differences in multidiminsional array and check standard deviation from that
# 	figure out optimal sensitivity
#		find greatest difference / sd for images with no pathology and with pathology
#	do voxels have to be contigous to determine if a slice is bad? could there be a threshold for a certain number of non-contigues voxels that could determine a slice to be bad?
#	build recursive function to find contigous voxels below threshold

import os
import sys
import numpy as np
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=FutureWarning)
import nibabel as nib


## the number of standard deviations from the mean for a voxel to be bad
sensitivity = 2
## the number of consecutive voxels required for a slice to be bad
threshold = 10


## gets nifti as input
input_img=sys.argv[1]

#load nifti to object
img = nib.load(input_img)
img_data = img.get_data()
data_obj = img.dataobj

## get dimensions
x_len = data_obj.shape[0]
y_len = data_obj.shape[1]
z_len = data_obj.shape[2]

##calculate standard deviation and mean in each slice
sliceVals = []
stdPerSlice = []
meanPerSlice = []
for z in range(0, z_len):
	sliceVals.clear() #clears list
	for y in range(0, y_len): #creates a list of all values in slice that exist (not 0)
		for x in range(0, x_len):
			if img_data[x,y,z]:
				sliceVals.append(img_data[x,y,z])
	if len(sliceVals): #excludes slices that are outside of the brain while maintaining correlation with slices position
		stdPerSlice.append(np.std(sliceVals))
		meanPerSlice.append(np.mean(sliceVals))
	else:
		stdPerSlice.append(0)
		meanPerSlice.append(0)


def checkBadSpot(x,y,z, threshold):
	badCount = 0
	while img_data[x+i,y,z] < threshold && img_data[x+i,y,z]:
		badCount++
	return badCount

## find voxels outside of std range
badSlices = [0] * z_len # list of all slices, initialized to all slices normal
for z in range(0, z_len):
	if stdPerSlice[z]: #makes sure slice is inside of brain
	thresholdVal = meanPerSlice[z] - (stdPerSlice[z] * sensitivity) #lowest normal value
		for y in range(0, y_len):
			if badSlices[z]:
				break #skips the rest of a slice if it is already determined to be bad
			for x in range(0, x_len):
				badCount = checkBadSpot(x,y,z,threshold) ##FIXME find a way to add badcount to x while staying within range
			if badCount > threshold:
				badSlices[z] = True
count = 0
for i in badSlices:
	if badSlices[i] == True:
		count++
print("number of bad slices: ", count)
