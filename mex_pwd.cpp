#include "mex.h"
#include <string.h>

void mexFunction(int nlhs,mxArray *plhs[],int nrhs,const mxArray *prhs[])
{
    double   *m_w_d, *p_w_z, *p_z_d, *p_w_d;
    mwIndex  *ir, *jc;
    size_t   d, k;
    size_t   n_w, n_d, n_z;
    size_t   beg_row_id, end_row_id, cur_row_id;
    mwIndex  *beg_of_ir, *beg_of_jc;
    mwSize   nzmax;
    size_t   word_index;
    
    if(!mxIsSparse(prhs[0]))
    {
        printf("word-doc matrix should be sparse matrix\n");
        return;
    }
    else if(nrhs != 3 || nlhs != 1)
    {
        printf("usage: p_w_d = pwd(m_w_d, p_w_z, p_z_d)\n");
        return;
    }
    
    // prhs[0] m_w_d sparse matrix
    m_w_d = mxGetPr(prhs[0]);
    jc = mxGetJc(prhs[0]);
    ir = mxGetIr(prhs[0]);
    nzmax = mxGetNzmax(prhs[0]);
    
    n_w = mxGetM(prhs[0]);
    n_d = mxGetN(prhs[0]);
    
    p_w_z = mxGetPr(prhs[1]);
    n_z = mxGetN(prhs[1]);
    
    p_z_d = mxGetPr(prhs[2]);
    
    plhs[0] = mxCreateSparse(n_w, n_d, nzmax, mxREAL);
    p_w_d = mxGetPr(plhs[0]);
    
    //Place ir data into the newly created sparse array.
    beg_of_ir = mxGetIr(plhs[0]);
    memcpy(beg_of_ir, ir, nzmax * sizeof(mwIndex));   //mwIndex for 64 bit system (cross platform)

    //Place jc data into the newly created sparse array.
    beg_of_jc = mxGetJc(plhs[0]);
    memcpy(beg_of_jc, jc, (n_d + 1) * sizeof(mwIndex));
    
    for (d = 0; d < n_d; d++)
    {
        beg_row_id = jc[d];
        end_row_id = jc[d + 1];
        
        for (cur_row_id = beg_row_id; cur_row_id < end_row_id; cur_row_id++)
        {
            word_index = ir[cur_row_id];
            for(k = 0; k < n_z; k++)
            {
                p_w_d[cur_row_id] += p_w_z[k * n_w + word_index] * p_z_d[d * n_z + k];
            }
        }
    }
    
    return;
}