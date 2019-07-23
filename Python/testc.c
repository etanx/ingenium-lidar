//testing for loop with C
//sample C file to add 2 numbers - int and floats

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include "py_subtract.h"

//helper functions

double sq_root2d(double x_sm, double x_lg, double y_sm, double y_lg)
{
	double xdist = pow(x_lg - x_sm,2);
	double ydist = pow(y_lg - y_sm,2);
	double dist = sqrt(xdist+ydist);
	return(dist);
}

//main calculating functions
int* div_cloud1(double* data_1,double diff_pts)
{
	printf("Dividing first cloud");
	int it=0; //the random counter 
    int count=0; //random counter for knowing where to put a value
	//pointer for calloc
    int* index_end; 
    int lendata=sizeof(data_1)/sizeof(double);

    double absdata[lendata];

    for(it=0;it<lendata;it++){
    	absdata[it] = fabs(data_1[it]);
    }
    index_end=(int*) calloc(lendata/2,sizeof(double));
    if (index_end == NULL) { 
        printf("Memory not allocated.\n"); 
        exit(0); 
    } 
	while(it<lendata){
		int keyadd=it;
		while(absdata[keyadd]-absdata[it]<diff_pts){
			it++;
		}
		index_end[count] = keyadd;
		count++;
		it++;
		index_end[count] = lendata;
	}	
	int* index_out=malloc(count*sizeof(int));
	for(it=0;it<=count;it++){
		index_out[it] = index_end[it];
	}
		index_out[count] = lendata-1;
		free(index_end);
	return index_end;
}


int* div_cloud2(double* data,double* data_ref,int* index_ref,double diff_pts)
{
	int it=0;
	int count=0;

	int* index_end;
	int lendata=sizeof(data)/sizeof(double);
    int lendata_ref=sizeof(data_ref)/sizeof(double);


	double absdata[lendata];
	double absdata_ref[lendata_ref];

	for(it=0;it<lendata;it++){
		absdata[it]=fabs(data[it]);
	}
	for(it=0;it<lendata_ref;it++){
		absdata_ref[it]=fabs(data_ref[it]);
	}
	index_end=(int*) calloc(lendata/2,sizeof(double));
    if (index_end == NULL) { 
        printf("Memory not allocated.\n"); 
        exit(0); 
    } 
    while(it<index_end[count]){
    	//int keyadd2 = it;
    	while(absdata[index_ref[count]]-absdata_ref[it]<diff_pts){
    		it++;
    	}
    	index_end[count] = it;

    	it++;
    	count++;

	}
	int* index_out=malloc(count*sizeof(int));
	for(it=0;it<=count;it++){
		index_out[it] = index_end[it];
	}
	index_out[count] = lendata-1;
	free(index_end);
	return index_out;
}

int* div_cloudy1(int dim,double temp_data[][dim],int* index,int lendata){
	int keyadd, it=0,count = 0;

    //int lendata=sizeof(temp_data)/sizeof(double);
	int* index_add = malloc(lendata*sizeof(int)/2);
	
	while(it<lendata){
		keyadd = it;
		double x_sm = temp_data[keyadd][0];
		double y_sm	= temp_data[keyadd][1];
		while((temp_data[it][1]-temp_data[keyadd][1]<1) && sq_root2d(x_sm,temp_data[it][0],y_sm,temp_data[it][1])<1 && it<lendata){
			it++;
		}
		index[count] = keyadd;
		count++;
		it++;
	}

	return(index_add); 
}

int* div_cloudy2(int dim, double data[][dim], double data_ref[][dim], int* index_ref,int lendata, int lendata_ref){
	int keyadd, it=0, count=0;
	//int lendata=sizeof(data1)/sizeof(double);
    //int lendata_ref=sizeof(data2)/sizeof(double);
	int* index_add = malloc(lendata*sizeof(int)/2);
	while(it<lendata){
		keyadd = it;
		while(data_ref[index_ref[count]][1] - data[it][1]>1){
			it++;
		}
		index_add[count] = keyadd;
		count++;
		it++;
	}
	return(index_add);
}
