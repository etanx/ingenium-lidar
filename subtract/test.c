
#include "test.h"
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

//helper functions
void free_data(DATA *data){
	free(data);
}
double sq_root2d(double x_sm, double x_lg, double y_sm, double y_lg)
{
	double xdist = pow(x_lg - x_sm,2);
	double ydist = pow(y_lg - y_sm,2);
	double dist = sqrt(xdist+ydist);
	return(dist);
}
//main funcs
void index_sub(DATA *data,int ref_it){
	double diff_pts = .50;
	int it=0;
	int i = 0;
	double distxy, distx, disty, distz;
	int start_it,end_it;
	if(ref_it+2000>data->n1){
		end_it = data->n1;
	}
	else{
		end_it = ref_it+2000;
	}
	if(ref_it-2000<0){
		start_it = 0;
	}
	else{
		start_it = ref_it-2000;
	}
	//printf("%d\n", data->ref_it);
	for(it=start_it;it<end_it;it++){
		//printf("%d %d\n", ref_it, it);

		distxy = sqrt(pow(data->datax1[it] - data->datax2[ref_it],2) + pow(data->datay1[it] - data->datay2[ref_it],2));
		distx = fabs(data->datax1[it] - data->datax2[ref_it]);
		disty = fabs(data->datay1[it] - data->datay2[ref_it]);
		distz = fabs(data->dataz1[it] - data->dataz2[ref_it]);
		if(distx<diff_pts && distz<diff_pts){
			//data->count++;
			//printf("%d\n", data->ref_it);
    		data->datax1[it] = 0;
   			data->datay1[it] = 0;
    		data->dataz1[it] = 0;
    		data->dataintens1[it] = 0;
    		data->datax2[ref_it] = 0;
   			data->datay2[ref_it] = 0;
    		data->dataz2[ref_it] = 0;
    		data->dataintens2[ref_it] = 0;
		}
		if(disty<diff_pts && distz<diff_pts){
			//data->count++;
			//printf("%d\n", data->ref_it);
    		data->datax1[it] = 0;
   			data->datay1[it] = 0;
    		data->dataz1[it] = 0;
    		data->dataintens1[it] = 0;
    		data->datax2[ref_it] = 0;
   			data->datay2[ref_it] = 0;
    		data->dataz2[ref_it] = 0;
    		data->dataintens2[ref_it] = 0;
		}
		if(distz<diff_pts && distz<diff_pts){
			//data->count++;
			//printf("%d\n", data->ref_it);
    		data->datax1[it] = 0;
   			data->datay1[it] = 0;
    		data->dataz1[it] = 0;
    		data->dataintens1[it] = 0;
    		data->datax2[ref_it] = 0;
   			data->datay2[ref_it] = 0;
    		data->dataz2[ref_it] = 0;
    		data->dataintens2[ref_it] = 0;
		}
		if(distxy<diff_pts && distz<diff_pts){
			//data->count++;
			//printf("%d\n", data->ref_it);
    		data->datax1[it] = 0;
   			data->datay1[it] = 0;
    		data->dataz1[it] = 0;
    		data->dataintens1[it] = 0;
    		data->datax2[ref_it] = 0;
   			data->datay2[ref_it] = 0;
    		data->dataz2[ref_it] = 0;
    		data->dataintens2[ref_it] = 0;
		}
	}
}

void index_wrap(DATA *data,int num_pts, PARAM *param){
	int it,it_param,ref_it;

	printf("%d\n", num_pts);
	ref_it = 0;

	
	double* data_refx,data_refy,data_refz;
	
	for(it=0;it<data->n2;it++){
		printf("%d\n", it);
		for(it_param=0;it_param<num_pts;it_param++){
			ref_it = ref_it+param->params[it_param]*it;
		}
		//printf("%d\n", ref_it);
		//printf("%d\n",it);
		ref_it = it; 
		index_sub(data,ref_it);
	}
}