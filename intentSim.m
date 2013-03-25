function sim_intent = intentSim(m_w_d, p_z_wd, p_z_d, p_w_z)
% Laplacian Probabilistic Latent Semantic Indexing/Alnalysis (LapPLSI) using generalized EM
%
%       m_w_d(w,d) is the number of occurrence of word w in document d
%		n_z        is the number of topics to be discovered
%       W          weight matrix of the affinity graph 
%
[n_z, n] = size(p_z_wd);
[n_w, n_d] = size(m_w_d);      % max indices of d and w
d_z_wd =  p_z_wd;              %p(z|w,d)
norm_d = rand(n_d, n_z);
sim_intent =  cell(n_z, 1);    %p(z|w,d)
p_w_d = sprand(m_w_d);         % p(w|d)

% if just use 0.1 as threshold, some doc maybe all 0
for d = 1:n_d
    temp = p_z_d(:,d);
    threshold = unique(temp,'sorted');
    [x, y] = size(threshold);
    if x > 1
        if threshold(end-1) > 0.1
            temp(temp < 0.1) = 0;
        else
            temp(temp < 1.0 / n_z) = 0;
        end
    end
    p_z_d(:,d) = temp;
end

for d = 1:n_d
    for w = find(m_w_d(:,d))
        p_w_d(w,d) = p_w_z(w,:) * p_z_d(:,d);
    end
end

for d = 1:n_d
    for w = find(m_w_d(:,d))'
        for z = 1:n_z
            p_z_wd{z}(w,d) = p_w_z(w,z) * p_z_d(z,d) / p_w_d(w,d);
        end
    end
end

for z = 1:n_z
    d_z_wd{z} = p_z_wd{z} .* m_w_d;
    for d = 1:n_d
        norm_d(d,z) = norm(d_z_wd{z}(:,d));
        if norm_d(d,z) == 0
            for w = find(m_w_d(:,d))'
                d_z_wd{z}(w,d) = 0;
            end
        else
            for w = find(m_w_d(:,d))'
                d_z_wd{z}(w,d) = d_z_wd{z}(w,d) / norm_d(d,z);
            end
        end
    end
end

for z = 1:n_z
    sim_intent{z} = d_z_wd{z}' * d_z_wd{z};
end




