#cython: boundscheck=False, wraparound=False, nonecheck=False
# takes two 3D point clouds and subtracts the dublicate points
# so as to leave what has changed between time of collection
# Author: Rachel Barron
# Affiliation: Wheaton College Ingenium, LiDAR Project
# Date: 7/19/19

#packages
from Cython.Build import cythonize
import pyximport; pyximport	
import ctypes 
import numpy as np
cimport numpy as np
import laspy
import numpy.ctypeslib as npct
import glob
import os
#from libc.stdlib cimport malloc, free
np.import_array()

#load the shared object file
fileshr = glob.glob(os.path.abspath("testc.so"))[0]
testfunc = ctypes.CDLL(fileshr)
#initial conditions
diff_pts = ctypes.c_double(.0001)#input('How far apart can the points be? ')
data_in1 = '97_1.las'#input('Enter the 1st las file name and path: ')
data_in2 = '87_1_geo.las'#input('Enter the 2nd las file name and path: ')
dim = 3#input('Dimension? ')

#read in las file
def organize_data(data,dim,col_sort):#,db_name):
    data_in = laspy.file.File(data, mode='r')	
    data_tbl = np.zeros((len(data_in.x),dim + 2))
    data_tbl[:,0] = np.arange(len(data_in))
    data_tbl[:,1] = data_in.x
    data_tbl[:,2] = data_in.y
    data_tbl[:,3] = data_in.z
    data_tbl[:,4] = data_in.intensity
    data_tbl = data_tbl[data_tbl[:,col_sort].argsort()]
    data_in.close()
    return(data_tbl)



def del_data(index,data):
    count = 0
    for it in range(len(data)):
        if index[count] == data[it]:
            data = np.delete(data[it-count][:])
            count+=1
#organize data: ascend by X val
data_tbl1 = organize_data(data_in1,dim,0)
data_tbl2 = organize_data(data_in2,dim,0)
data_dict1 = {}
data_dict2 = {}
data_tblx = data_tbl1[:,0].astype(np.float64)
int_data = np.zeros(len(data_tbl1[:,0])/2)
int_data = int_data.astype(np.int32)
'''
cdef extern from "py_subtract.h":
    int* div_cloud1(double* data_1,double diff_pts)

def div_cloud1_func(np.ndarray[double, ndim=1,mode="c"] data not None,diff_pts):
    div_cloud1(<double*> np.PyArray_DATA(data),
		diff_pts)
    return div_cloud1(data,diff_pts)
index1,count = div_cloud1_func(data_tblx,diff_pts)
#print(np.array(index1))
'''

# div 2nd cloud
#npct.ndpointer(dtype=np.double, ndim=1, flags='CONTIGUOUS')
#testfunc = npct.load_library("testfunc", ".")

# might use ctypes.cast() later
double_arr = npct.ndpointer(dtype=np.float64)
intarr = np.zeros(100,dtype=np.int32)
testfunc.div_cloud1.argtypes = [double_arr,ctypes.c_double]
testfunc.div_cloud1.restype = intarr
'''
def div_cloud1_func(data,diff_pts):
    return testfunc.div_cloud1(data,diff_pts)
'''
testfunc.div_cloud1(data_tblx,diff_pts,ctypes.c_void_p(intarr.ctypes.data))
print(data_tblx)
#print(ctypes.POINTER(ctypes.c_int))
