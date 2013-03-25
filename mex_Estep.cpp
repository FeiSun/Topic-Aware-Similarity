#include "mex.h"
#include <math.h>
#include "matrix.h"

void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[])
{
    double *m_w_d, *p_w_z, *p_z_d, *p_w_d;
    int i, j, k;
    int n_w, n_d, n_z;
    int      ndim=1, dims[1];
    int      index, nsubs=1, subs[1];
    mxArray  *temp_array;
    double *temp;

    m_w_d = mxGetPr(prhs[0]);
    n_w = mxGetM(prhs[0]);
    n_d = mxGetN(prhs[0]); 
    
    p_w_z = mxGetPr(prhs[1]);
    n_z = mxGetN(prhs[1]);
    
    dims[0] = n_z;
    
    p_z_d = mxGetPr(prhs[2]);
    
    p_w_d = mxGetPr(prhs[3]);
  
    plhs[0] = mxCreateCellArray(ndim, dims);
    //total_num_of_cells = mxGetNumberOfElements(plhs[0]); 
    for(k = 0; k < n_z; k++)
    {
        subs[0] = k;
        index = mxCalcSingleSubscript(plhs[0], nsubs, subs);

        temp_array = mxCreateDoubleMatrix(n_w, n_d, mxREAL);
        temp = mxGetPr(temp_array);

        for(i = 0; i < n_d; i++)
            for(j = 0; j < n_w; j++)
                if(m_w_d[i * n_w + j] > 0)
                {
                    temp[i * n_w + j] = p_w_z[k * n_w + j] * p_z_d[i * n_z + k] / p_w_d[i * n_w + j];
                }
        
        mxSetCell(plhs[0], index, temp_array); 
    }
   return;
}
