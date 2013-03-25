#include "mex.h"
#include <string.h>

void mexFunction(int nlhs,mxArray *plhs[],int nrhs,const mxArray *prhs[])
{
    double   *m_w_d, *p_w_z, *p_z_d, *p_w_d;
    mwIndex  *ir, *jc;
    size_t   d, k;
    size_t   n_w, n_d, n_z;
    mwSize   ndim = 1, dims[1];
    mwSize   nsubs = 1;
    mxArray  *temp_array;
    double   *temp;
    size_t   beg_row_id, end_row_id, cur_row_id;
    mwIndex  index, subs[1];
    mwIndex  *beg_of_ir, *beg_of_jc;
    mwSize   nzmax;
    size_t total = 0;
    
    
    if(!mxIsSparse(prhs[0]))
    {
        printf("word-doc matrix should be sparse matrix\n");
        return;
    }
    else if(nrhs != 4 || nlhs != 1)
    {
        printf("usage: p_z_wd = mex_Estep_sparse(m_w_d, p_w_z_n, p_z_d_n, p_w_d)\n");
        return;
    }
    
    m_w_d = mxGetPr(prhs[0]);
    jc = mxGetJc(prhs[0]);
    ir = mxGetIr(prhs[0]);
    nzmax = mxGetNzmax(prhs[0]);
    
    n_w = mxGetM(prhs[0]);
    n_d = mxGetN(prhs[0]);

    p_w_z = mxGetPr(prhs[1]);
    n_z = mxGetN(prhs[1]);
    
    
    
    p_z_d = mxGetPr(prhs[2]);
    
    p_w_d = mxGetPr(prhs[3]);
    
    dims[0] = n_z;
    plhs[0] = mxCreateCellArray(ndim, dims);
    //total_num_of_cells = mxGetNumberOfElements(plhs[0]);
    
    for(k = 0; k < n_z; k++)
    {
        total = 0;
        subs[0] = k;
        index = mxCalcSingleSubscript(plhs[0], nsubs, subs);
        
        temp_array = mxCreateSparse(n_w, n_d, nzmax, mxREAL);
        temp = mxGetPr(temp_array);
        mxSetNzmax(temp_array, nzmax);
        
        //Place ir data into the newly created sparse array.
        beg_of_ir = mxGetIr(temp_array);
        memcpy(beg_of_ir, ir, nzmax * sizeof(mwIndex));
        
        //Place jc data into the newly created sparse array.
        beg_of_jc = mxGetJc(temp_array);
        memcpy(beg_of_jc, jc, (n_d + 1) * sizeof(mwIndex));
        
        for (d = 0; d < n_d; d++)
        {
            beg_row_id = jc[d];
            end_row_id = jc[d + 1];
            
            if (beg_row_id == end_row_id)
                continue;
            else
            {
                for (cur_row_id = beg_row_id; cur_row_id < end_row_id; cur_row_id++)
                {
                    temp[total] = p_w_z[k * n_w + ir[cur_row_id]] * p_z_d[d * n_z + k] / p_w_d[total];
                    total++;
                }
            }
        }
        
        mxSetCell(plhs[0], index, temp_array);
    }
    return;
}