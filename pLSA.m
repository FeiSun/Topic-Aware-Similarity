function [p_w_z, p_z_d, log_likelihood] = pLSA(m_w_d, n_z, iter_num)
% PLSA	Fit a pLSA model on given data
%       in which m_w_d(w,d) is the number of occurrence of word w in document d
%		n_z is the number of topics to be discovered
%

differror = 1e-2;

% pre-allocate space
[n_w, n_d] = size(m_w_d); % max indices of d and w
p_z_d = rand(n_z, n_d);   % p(z|d)
p_w_z = rand(n_w, n_z);   % p(w|z)
p_z_wd = cell(n_z, 1);   %p(z|w,d)

p_z_d = p_z_d ./ repmat(sum(p_z_d,1),n_z,1);

p_w_z = p_w_z ./ repmat(sum(p_w_z,1),n_w,1);

p_w_d = sprand(m_w_d);

for d = 1:n_d
    for w = find(m_w_d(:,d))
        p_w_d(w,d) = p_w_z(w,:) * p_z_d(:,d);
    end
end

for z = 1:n_z
    p_z_wd{z} = sprand(m_w_d);
end

log_likelihood = []; % log-likelihood

for i = 1:iter_num
    %E-step;
    p_z_wd = mex_Estep_sparse(m_w_d, p_w_z, p_z_d, p_w_d);
    
    %M-step:
    [p_w_z, p_z_d] = mex_Mstep_sparse(m_w_d, p_z_wd);
    
    % update p(w|d) and calculate likelihood
    L = 0;
    for d = 1:n_d
        for w = find(m_w_d(:,d))'
            p_w_d(w,d) = p_w_z(w,:) * p_z_d(:,d);
            L = L + m_w_d(w,d) * log(p_w_d(w,d));
        end
    end
    
    %fprintf('%d\n',L);
    log_likelihood = [log_likelihood; L];
    length = size(log_likelihood,1);
    if length > 1
        %fprintf('%d\n',log_likelihood(end) - log_likelihood(end-1));
        if log_likelihood(end) - log_likelihood(end-1) < differror
            break;
        end
    end
end
