function doc_sim = DocSim(m_w_d)
% using doc-word vector to computer cos simility

[n_w, n_d] = size(m_w_d); % max indices of d and w

norm_d = diag(sqrt(m_w_d' * m_w_d));

doc_sim = m_w_d' * m_w_d ./ (norm_d * norm_d');