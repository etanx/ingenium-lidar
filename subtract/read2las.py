import ctypes
import numpy as np
import laspy
import gc
import sqlite3
import io
import os
import shelve
import csv

#read in file




def organize_data(data,dim):#,db_name):
    data_in = laspy.file.File(data, mode='r')   
    data_tbl = np.zeros((len(data_in.x),dim +1))
    data_tbl[:,0] = data_in.x
    data_tbl[:,1] = data_in.y
    data_tbl[:,2] = data_in.z
    data_tbl[:,3] = data_in.intensity
    print(data_tbl)
    data_tbl = data_tbl[data_tbl[:,1].argsort(),:]
    it = 0
    while data_tbl[it][0]==0 and data_tbl[it][1]==0:
        print(it)
        it+=1
        if it == len(data_tbl[:]):
            break
    print(it)
    data_tbl = data_tbl[it:-1][:]
    data_in.close()
    print(data_tbl)
    return(data_tbl)




def read_out(data,source_name):
    name1 = source_name + "out.las"
    data_in = laspy.file.File(source_name, mode='r')
    outFile1 = laspy.file.File(name1, mode = "w",
                header = data_in.header)
    outFile1.x = data[:,0]
    outFile1.y = data[:,1]
    outFile1.z = data[:,2]
    outFile1.intensity = data[:,3]
    data_in.close()
    outFile1.close()


data_in1 = input('Enter the 1st las file name and path: ')
dim = 3

data_tbl = organize_data(data_in1,3)
read_out(data_tbl,data_in1)