function [p_w_z_n, p_z_d_n, p_z_wd, log_likelihood] = LapPLSA(m_w_d, W, n_z, iter_num)
% Laplacian Probabilistic Latent Semantic Indexing/Alnalysis (LapPLSI) using generalized EM
%
%       m_w_d(w,d) is the number of occurrence of word w in document d
%		n_z        is the number of topics to be discovered
%       W          weight matrix of the affinity graph 
%

differror = 1e-2;
gamma = 0.1;
lambda = 1000;

% pre-allocate space
[n_w, n_d] = size(m_w_d); % max indices of d and w
p_z_d_n = rand(n_z, n_d);   % p(z|d)_n
p_z_d_n2 = rand(n_z, n_d);  % p(z|d)
p_w_z_n = rand(n_w, n_z);   % p(w|z)_n
p_z_wd =  cell(n_z, 1);   %p(z|w,d)

D = spdiags(sum(W,2),0,speye(size(W,1)));
L = D - W;
sum_w_col = full(sum(W,2));

%sum_w_col = sum(W,2);
temp = repmat(sum_w_col', n_z, 1);

%normalize column 
p_z_d_n = p_z_d_n ./ repmat(sum(p_z_d_n,1),n_z,1);
p_w_z_n = p_w_z_n ./ repmat(sum(p_w_z_n,1),n_w,1);

p_w_d = sprand(m_w_d);

for d = 1:n_d
    for w = find(m_w_d(:,d))
        p_w_d(w,d) = p_w_z_n(w,:) * p_z_d_n(:,d);
    end
end

for z = 1:n_z
    p_z_wd{z} = sprand(m_w_d);
end


log_likelihood = []; % log-likelihood

for i = 1:iter_num
    %E-step;
    p_z_wd = mex_Estep_sparse(m_w_d, p_w_z_n, p_z_d_n, p_w_d);
    
    %M-step:
    [p_w_z_n1, p_z_d_n1] = mex_Mstep_sparse(m_w_d, p_z_wd);
    
    p_z_d_n2 = (1 - gamma) * p_z_d_n1 + gamma * p_z_d_n1 * W ./ temp;
    
    obj = Q(m_w_d, L, p_w_z_n1, p_z_d_n1, lambda);
    obj(end + 1) = Q(m_w_d, L, p_w_z_n1, p_z_d_n2, lambda);
    
    while obj(end) > obj(end - 1)
        p_z_d_n1 = p_z_d_n2;
        p_z_d_n2 = (1 - gamma) * p_z_d_n1 + gamma * p_z_d_n1 * W ./ temp;
        obj(end + 1) = Q(m_w_d, L, p_w_z_n1, p_z_d_n2, lambda);
    end
    
    obj_new = Q(m_w_d, L, p_w_z_n, p_z_d_n, lambda);
    
    if abs(obj(end - 1) - obj_new) < differror
        log_likelihood = [log_likelihood; obj_new];
        break;
    end
    
    p_w_z_n = p_w_z_n1;
    p_z_d_n = p_z_d_n1;
    
    for d = 1:n_d
        for w = find(m_w_d(:,d))
            p_w_d(w,d) = p_w_z_n(w,:) * p_z_d_n(:,d);
        end
    end
    
    log_likelihood = [log_likelihood; obj(end - 1)];
    
end

function obj = Q(m_w_d, L, p_w_z, p_z_d, lambda)
% compute object function

p_w_d = mex_pwd(m_w_d, p_w_z, p_z_d);

obj_lap = sum(sum(p_z_d * L .* p_z_d));

%obj = Q2(m_w_d, p_w_z, p_z_d);
obj = mex_likelihood(m_w_d, p_w_d);

obj = obj - lambda * obj_lap;




