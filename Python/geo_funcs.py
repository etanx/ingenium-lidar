# takes 3 (or eventually 6) reference points, creates a transformation matrix,
# takes a file and uses the transformation matrix to map all incoming points to 
# their transformed points
# How to run: enter 'python' in a terminal window to start the python shell. Use 
# 'import geo_funcs' to start the script.

# author: Rachel Barron
# affiliation: Wheaton College Ingenium
# Date: 7/10/19

import numpy as np 
from liblas import file
import laspy


  
print('warning: there are no safety checks yet. Pay close attention to input request.\n This currently only works for 3D')

# create matrices
dim = int(input('Dimension? '))
ref_pts = int(input('Number of reference points? '))
matr_init = np.zeros((ref_pts,dim))
matr_fin = matr_init
repeat = True

while repeat == True:
	print('Initial Matrix: ')
	for i in range(ref_pts):
		for it in range(dim):
			matr_init[i,it] = float(input('Enter element ' + str(i) + ',' + str(it) + ': '))
	print('Reference Matrix')
	for i in range(ref_pts):
		for it in range(dim):
			matr_fin[i,it] = float(input('Enter element ' + str(i) + ',' + str(it) + ': '))

	repeat = bool(raw_input('Initial matrix is: \n ' + str(matr_init) + '\n' + 'Final is: \n' + str(matr_fin) + '\nIf correct, enter. Else press another key: '))

matr_trans = matr_fin*np.linalg.inv(matr_init)

# read input file
data_in = input('Enter the las file name and path: ')
data = laspy.file.File(data_in, mode='r')
data_list = np.zeros((dim+1,len(data.x)))
new_data = np.zeros((dim+1,len(data.x)))
for obj in range(len(data.x)):
	data_list[0,obj] = data.x[obj]
	data_list[1,obj] = data.y[obj]
	data_list[2,obj] = data.z[obj]
	data_list[3,obj] = data.intensity[obj]
	print(obj)

# multiply each point by transformation matrix
for i in range(len(data.x)):
	new_data[:-1,i] = np.matmul(data_list[:-1,i],matr_trans)

# read out new points
outFile1 = laspy.file.File("returnData.las", mode = "w",
                header = data.header)
outFile1.x = new_data[0,:]
outFile1.y = new_data[1,:]
outFile1.z = new_data[2,:]
outFile1.intensity = new_data[3,:]



data.close()
outFile1.close()