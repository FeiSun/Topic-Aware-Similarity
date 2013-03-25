#include "mex.h"
#include <math.h>
#include "matrix.h"

void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[])
{
    double   *m_w_d;
    double   *p_w_z, *p_z_d;
    double   *p_w_z_temp, *p_z_d_temp;
    size_t   n_w, n_d, n_z;
    size_t   i, j, k;
    mwIndex  *ir, *jc;
    mwIndex  index, subs[1];
    mwSize   nsubs = 1;
    const mxArray  *p_z_wd, *cell_element_ptr;
    double   *temp;
    mwSize   nzmax;
    size_t   beg_row_id, end_row_id, cur_row_id;

    
    if(!mxIsSparse(prhs[0]))
    {
        printf("word-doc matrix should be sparse matrix\n");
        return;
    }
    else if(!mxIsCell(prhs[1]))
    {
        printf("p(z|w,d) shoulde be cell\n");
        return;
    }
    else if(nrhs != 2 || nlhs != 2)
    {
        printf("usage: [p_w_z_n1, p_z_d_n1] = mex_Mstep_sparse(m_w_d, p_z_wd)\n");
        return;
    }
    
    m_w_d = mxGetPr(prhs[0]);
    n_w = mxGetM(prhs[0]);
    n_d = mxGetN(prhs[0]); 
    
    jc = mxGetJc(prhs[0]);
    ir = mxGetIr(prhs[0]);
    nzmax = mxGetNzmax(prhs[0]);
    
    p_z_wd = prhs[1];
    n_z = mxGetNumberOfElements(prhs[1]); 
    
    //output p(w|z) p(z|d)
    plhs[0] = mxCreateDoubleMatrix(n_w, n_z, mxREAL);
    p_w_z = mxGetPr(plhs[0]);
    plhs[1] = mxCreateDoubleMatrix(n_z, n_d, mxREAL);
    p_z_d = mxGetPr(plhs[1]);
    p_w_z_temp = (double *) mxCalloc(n_z, sizeof(double));
    p_z_d_temp = (double *) mxCalloc(n_d, sizeof(double));
    
    //update p(w|z)    
    for(i = 0; i < n_z; i++)
    {
        subs[0] = i;
        index = mxCalcSingleSubscript(p_z_wd, nsubs, subs);
        
        cell_element_ptr = mxGetCell(p_z_wd, index);
        temp = mxGetPr(cell_element_ptr);
            
        for(k = 0; k < n_d; k++)
        {
            //get sparse matrix value by subscript (j, k)
            beg_row_id = jc[k];
            end_row_id = jc[k + 1];
            
            for (cur_row_id = beg_row_id; cur_row_id < end_row_id; cur_row_id++)
            {
                //p_w_z (ir[cur_row_id], i)
                p_w_z[i * n_w + ir[cur_row_id]] += m_w_d[cur_row_id] * temp[cur_row_id];
            }
        }
    }
    
    for(i = 0; i < n_z; i++)
    {
        for(j = 0; j < n_w; j++)
        {
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
            
            //get sparse matrix value by subscript (j, k)
            beg_row_id = jc[j];
            end_row_id = jc[j + 1];
            
            for (cur_row_id = beg_row_id; cur_row_id < end_row_id; cur_row_id++)
            {
                //p_w_z (ir[cur_row_id], i)
                p_z_d[j * n_z + i] += m_w_d[cur_row_id] * temp[cur_row_id];
            }
            
            //p_z_d_temp[j] += p_z_d[j * n_z + i];
        }
    }
    
     for(i = 0; i < n_d; i++)
    {
        for(j = 0; j < n_z; j++)
        {
            p_z_d_temp[i] += p_z_d[i * n_z + j];
        }
        for(j = 0; j < n_z; j++)
        {
            p_z_d[i * n_z + j] /= p_z_d_temp[i];
        }
    }
    
    mxFree(p_z_d_temp);
    
   return;
}
