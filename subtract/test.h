struct DATA;

typedef struct DATA{
    int n1;
    int n2;
    double *datax1;
    double *datay1;
    double *dataz1;
    double *dataintens1;
    double *datax2;
    double *datay2;
    double *dataz2;
    double *dataintens2;
    double *params;
} DATA;

struct PARAM;

typedef struct PARAM{
    double *params;
} PARAM;