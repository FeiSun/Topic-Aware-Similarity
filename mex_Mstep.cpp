#include "mex.h"
#include <math.h>
#include "matrix.h"

void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[])
{
    double *m_w_d;
    double *p_w_z, *p_z_d;
    double *p_w_z_temp, *p_z_d_temp;
    int i, j, k;
    int n_w, n_d, n_z;
    int      ndim=1, dims[1];
    int      index, nsubs=1, subs[1];
    const mxArray  *p_z_wd, *cell_element_ptr;
    double *temp;

    m_w_d = mxGetPr(prhs[0]);
    n_w = mxGetM(prhs[0]);
    n_d = mxGetN(prhs[0]); 
    
    p_z_wd = prhs[1];
    n_z = mxGetNumberOfElements(prhs[1]); 
    
    plhs[0] = mxCreateDoubleMatrix(n_w, n_z, mxREAL); //p_w_z
    p_w_z = mxGetPr(plhs[0]);
    plhs[1] = mxCreateDoubleMatrix(n_z, n_d, mxREAL); //p_z_d
    p_z_d = mxGetPr(plhs[1]);
    p_w_z_temp = (double *) mxCalloc(n_z, sizeof(double));
    p_z_d_temp = (double *) mxCalloc(n_d, sizeof(double));
    //mexPrintf("%f %f ", p_w_z_temp[0], p_z_d_temp[0]);
    
    //update p(w|z)
    
    for(i = 0; i < n_z; i++)
    {
        subs[0] = i;
        index = mxCalcSingleSubscript(p_z_wd, nsubs, subs); //k= index?
        
        cell_element_ptr = mxGetCell(p_z_wd, index);
        temp = mxGetPr(cell_element_ptr);
        
        for(j = 0; j < n_w; j++)
        {
            p_w_z[i * n_w + j] = 0;
            
            for(k = 0; k < n_d; k++)
            {
                p_w_z[i * n_w + j] += m_w_d[k * n_w + j] * temp[k * n_w + j];
            }
            p_w_z_temp[i] += p_w_z[i * n_w + j];
        }
        for(j = 0; j < n_w; j++)
        {
            p_w_z[i * n_w + j] /= p_w_z_temp[i];
        }
    }
    mxFree(p_w_z_temp);
    
    //update p(z|d)
    for(i = 0; i < n_z; i++)
    {
        subs[0] = i;
        index = mxCalcSingleSubscript(p_z_wd, nsubs, subs);
        
        cell_element_ptr = mxGetCell(p_z_wd, index);
        temp = mxGetPr(cell_element_ptr);
        
        for(j = 0; j < n_d; j++)
        {
            p_z_d[j * n_z + i] = 0;
            
            for(k = 0; k < n_w; k++)
            {
                p_z_d[j * n_z + i] += m_w_d[j * n_w + k] * temp[j * n_w + k];
            }
            p_z_d_temp[j] += p_z_d[j * n_z + i];
        }
    }
    
     for(i = 0; i < n_d; i++)
    {
        for(j = 0; j < n_z; j++)
        {
            p_z_d[i * n_z + j] /= p_z_d_temp[i];
        }
    }
    
    mxFree(p_z_d_temp);
    
   return;
}
