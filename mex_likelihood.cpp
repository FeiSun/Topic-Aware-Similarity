#include "mex.h"
#include <math.h>

void mexFunction(int nlhs,mxArray *plhs[],int nrhs,const mxArray *prhs[])
{
    double   *m_w_d, *p_w_z, *p_z_d, *p_w_d;
    mwIndex  *ir, *jc;
    size_t   d;
    size_t   n_w, n_d;
    size_t   beg_row_id, end_row_id, cur_row_id;
    double   *obj;
    
    if(!mxIsSparse(prhs[0]))
    {
        printf("word-doc matrix should be sparse matrix\n");
        return;
    }
    else if(nrhs != 2 || nlhs != 1)
    {
        printf("usage: obj = likelihood(m_w_d, p_w_d);\n");
        return;
    }
    
    m_w_d = mxGetPr(prhs[0]);
    jc = mxGetJc(prhs[0]);
    ir = mxGetIr(prhs[0]);
    
    n_w = mxGetM(prhs[0]);
    n_d = mxGetN(prhs[0]);
    
    p_w_d = mxGetPr(prhs[1]);
    
    plhs[0] = mxCreateDoubleMatrix(1, 1, mxREAL);
    obj = mxGetPr(plhs[0]); 
    
    for (d = 0; d < n_d; d++)
    {
        beg_row_id = jc[d];
        end_row_id = jc[d + 1];
        for (cur_row_id = beg_row_id; cur_row_id < end_row_id; cur_row_id++)
        {
            obj[0] += m_w_d[cur_row_id] * log(p_w_d[cur_row_id]);
        }
    }

    return;
}