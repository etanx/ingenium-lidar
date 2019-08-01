# How to run: enter 'python3 test_struct.py' in a terminal window. 
# enter each file to be compared
# take .csv output from here and run txt2las -parse xyzi filein.txt fileout.las for each
# then move them to txt2las and run read2las.py
#   this will take one las file and remove the zeros
# author: Rachel Barron
# affiliation: Wheaton College Ingenium
# Date: 7/30/19

import ctypes
import numpy as np
import laspy
import gc
import sqlite3
import io
import os
import shelve
import csv
  
print('warning: there are no safety checks yet. Pay close attention to input request.\n This currently only works for 3D')


diff_pts = .0001#input('How far apart can the points be? ')
data_in1 = input('Enter the 1st las file name and path: ')
data_in2 = input('Enter the 2nd las file name and path: ')
dim = 3#input('Dimension? ')

#read in las file
def organize_data(data,dim,col_sort):#,db_name):
    data_in = laspy.file.File(data, mode='r')	
    data_tbl = np.zeros((len(data_in.x),dim +1))
    data_tbl[:,0] = data_in.x
    data_tbl[:,1] = data_in.y
    data_tbl[:,2] = data_in.z
    data_tbl[:,3] = data_in.intensity
    #data_tbl = data_tbl[data_tbl[:,2].argsort(),:]
    #data_tbl = data_tbl[data_tbl[:,1].argsort(),:]
    data_tbl = data_tbl[data_tbl[:,0].argsort(),:]
    data_in.close()
    print(data_tbl)

    return(data_tbl)

print("organizing data")
#def proc_data():
data_tbl1 = organize_data(data_in1,dim,0)
data_tbl2 = organize_data(data_in2,dim,0)
num_pts = 15
def matr_gen(data1,data2):
    print('Initial Matrix: ')
    matr_init = np.zeros(num_pts)
    matr_ref = matr_init
    #set matrices
    print(len(data1[:,0]))
    for i in range(num_pts):
        row = i*len(data1[:,0])/num_pts
        matr_init[i] = row
    print('Reference Matrix')
    
    for i in range(num_pts):
        it_data = 0
        row_ref = int(matr_init[i])
        #row_ref = int(i*len(data2[:,0])/num_pts)
        print(row_ref)
        while data2[it_data][0]<data1[row_ref][0] and data2[it_data][1]<data1[row_ref][1] and data2[it_data][2]<data1[row_ref][2]:
            print()
            it_data+=1
        matr_ref[i] = it_data
    #create line to comp
    param = np.polyfit(matr_ref,matr_init,6) # ref_it comes from data2. Thus data2 -> x
    print(param)
    return(param)
params = np.array(matr_gen(data_tbl1,data_tbl2),dtype=ctypes.c_double)



#div_cloud1
def c_call(data_tbl1,data_tbl2):
    data_tblx = np.array(data_tbl1[:,0])
    data_tblx2 = np.array(data_tbl2[:,0])
    data_tbly = np.array(data_tbl1[:,1])
    data_tbly2 = np.array(data_tbl2[:,1])
    data_tblz = np.array(data_tbl1[:,2])
    data_tblz2 = np.array(data_tbl2[:,2])
    data_tblintens = np.array(data_tbl1[:,3])
    data_tblintens2 = np.array(data_tbl2[:,3])
    testlib = ctypes.cdll.LoadLibrary('/home/shimron/Desktop/georef/test/making_it_easier/test.so')
    class Data(ctypes.Structure):
         _fields_ = [("n", ctypes.c_int),
                    ("n_sub",ctypes.c_int),
                    ("datax",ctypes.POINTER(ctypes.c_double)),
                    ("datay",ctypes.POINTER(ctypes.c_double)),
                    ("dataz",ctypes.POINTER(ctypes.c_double)),
                    ("dataintens",ctypes.POINTER(ctypes.c_double)),
                    ("datax1",ctypes.POINTER(ctypes.c_double)),
                    ("datay1",ctypes.POINTER(ctypes.c_double)),
                    ("dataz1",ctypes.POINTER(ctypes.c_double)),
                    ("dataintens1",ctypes.POINTER(ctypes.c_double)),
                    ("params",ctypes.POINTER(ctypes.c_double))]

    print("past class")
    class Params(ctypes.Structure):
         _fields_ = [("param",ctypes.POINTER(ctypes.c_double))]

    data = Data(len(data_tblx),
            len(data_tblx2),
            np.ctypeslib.as_ctypes(data_tblx),
            np.ctypeslib.as_ctypes(data_tbly),
            np.ctypeslib.as_ctypes(data_tblz),
            np.ctypeslib.as_ctypes(data_tblintens),
            np.ctypeslib.as_ctypes(data_tblx2),
            np.ctypeslib.as_ctypes(data_tbly2),
            np.ctypeslib.as_ctypes(data_tblz2),
            np.ctypeslib.as_ctypes(data_tblintens),
            np.ctypeslib.as_ctypes(params))       
            #np.ctypeslib.as_ctypes(index_main_hold))
    print("past Data")
    testlib.index_wrap.restype = None
    param_pass = Params(np.ctypeslib.as_ctypes(params))
    testlib.index_wrap(ctypes.byref(data),ctypes.c_int(num_pts),ctypes.byref(param_pass))
    data_tbl1[:,0] = data_tblx
    data_tbl2[:,0] = data_tblx2
    data_tbl1[:,1] = data_tbly
    data_tbl2[:,1] = data_tbly2
    data_tbl1[:,2] = data_tblz
    data_tbl2[:,2] = data_tblz2
    data_tbl1[:,3] = data_tblintens
    data_tbl2[:,3] = data_tblintens2
    #testlib.free_data(ctypes.byref(data))
    #data_com(data_tbl1)
    #data_com(data_tbl2)
    return(data_tbl1,data_tbl2)

'''data_tbl1 = np.zeros((len(data_tblx),dim +1))
data_tbl2 = np.zeros((len(data_tblx2),dim +1))
'''
c_call(data_tbl1,data_tbl2)


#conn.commit()
print(data_tbl2)
print(data_tbl1)

#read out
# read out modified data tables

def read_out(source_name,data):
    name1 = source_name + "out.csv"

    with open(name1,'w') as f:
        
        wr = csv.writer(f, delimiter='\t')
        #for i in range(len(data[:,0])):
            #if data[i,0] != 0 and data[i,1] != 0:
        wr.writerows(zip(data[:,0],data[:,1],data[:,2],data[:,3]))
    #np.savetxt(name1,data)

    '''file_out = open(name1,"w")
    for i in range(len(data[:,0])):
        file_out.write(data[i,:])
    data_in = laspy.file.File(source_name, mode='r')
    outFile1 = laspy.file.File(name1, mode = "w",
                header = data_in.header)
    outFile1.x = data[:,0]
    outFile1.y = data[:,1]
    outFile1.z = data[:,2]
    outFile1.intensity = data[:,3]
    data_in.close()
    outFile1.close()
    '''
read_out(data_in1,data_tbl1)
read_out(data_in2,data_tbl2)#[count2:-1,:])
