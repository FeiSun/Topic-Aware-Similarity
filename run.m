fid = fopen('./data/authors.txt','rt');
authors = textscan(fid,'%s','Delimiter','\n');
fclose(fid);
authors = authors{1};

wdmatrix_dir = './data/wdmatrix/';
coauthor_dir = './data/coauthor/';
PLSA_purity_dir= './result/PLSA purity/';
purity_dir = './result/purity/';
LapPLSA_topic_dir = './result/LapPLSA topic/';

[n, col]= size(authors);

n_z = 30;
iter_num = 200;

h_sim = zeros(100,3);
h_sim_doc = zeros(100,3);

for i = 1:n
    author = authors(i);
    author = author(1);
    
    
    wdmatrix_file_name = strcat(wdmatrix_dir,author,{'_wdmatrix.txt'});
    
    coauthor_file_name = strcat(coauthor_dir,author,{'_coauthor.txt'});
    
    m_w_d = sparse(dlmread(char(wdmatrix_file_name),'\t'));
    W = sparse(dlmread(char(coauthor_file_name),'\t'));
    
    % Train the pLSA model
    %[p_w_z, p_z_d, Lt] = pLSA(m_w_d, n_z, 200);
    
    tic
    [p_w_z, p_z_d, p_z_wd, log_likelihood] = LapPLSA(m_w_d, W, n_z, iter_num);
    toc
    [topic_value, topic_index] = max(p_z_d);

    %maxtopic_file_name = strcat(PLSA_purity_dir,author,{'_maxtopic.txt'});
    maxtopic_file_name = strcat(purity_dir,author,{'_maxtopic.txt'});
    dlmwrite(char(maxtopic_file_name), topic_index, 'delimiter', '\t');
    
    LapPLSA_dz_name = strcat(LapPLSA_topic_dir,author,{'_dz.txt'});
    LapPLSA_zw_name = strcat(LapPLSA_topic_dir,author,{'_zw.txt'});
    LapPLSA_mat_name = strcat(LapPLSA_topic_dir,author,{'.mat'});
    
    dlmwrite(char(LapPLSA_dz_name), p_z_d', 'delimiter', '\t', 'precision', '%.6f');
    dlmwrite(char(LapPLSA_zw_name), p_w_z', 'delimiter', '\t', 'precision', '%.6f');
    
    save(char(LapPLSA_mat_name), 'm_w_d', 'p_z_d', 'p_w_z', 'p_z_wd');

    %LapPLSA_mat_name = strcat(LapPLSA_topic_dir,author,{'.mat'});
    %load(char(LapPLSA_mat_name));

    sim_intent = intentSim(m_w_d, p_z_wd, p_z_d, p_w_z);
    
    intra_sim = IntraSim(p_z_d, sim_intent);
    
    inter_sim = InterSim(p_z_d, sim_intent);
    
    h_sim(i,1) = intra_sim;
    h_sim(i,2) = inter_sim;
    
    if intra_sim > 0
        h_sim(i,3) = inter_sim / intra_sim;
    end
    
    doc_sim = DocSim(m_w_d);
    
    doc_sim_intent = cell(n_z, 1);
    
    for z = 1:n_z
        doc_sim_intent{z} = doc_sim;
    end
    
    doc_intra_sim = IntraSim(p_z_d, doc_sim_intent);
    
    doc_inter_sim = InterSim(p_z_d, doc_sim_intent);
    
    h_sim_doc(i,1) = doc_intra_sim;
    h_sim_doc(i,2) = doc_inter_sim;
    
    if doc_intra_sim > 0
        h_sim_doc(i,3) = doc_inter_sim / doc_intra_sim;
    end
    toc
    
end

dlmwrite('./result/intent_sim.txt', h_sim, 'delimiter', '\t');
dlmwrite('./result/doc_sim.txt', h_sim_doc, 'delimiter', '\t');

fprintf('%f,%f \n', mean(h_sim(:,3)), mean(h_sim_doc(:,3)));


%n_kw = 10; % Find 10 keywords
%for z = 1:n_z
%    fprintf('Key words for topic %d:\n', z);
%    [S, I] = sort(p_w_z(:,z), 'descend');
%    for w = I(1:n_kw)'
%        fprintf('%d %s\t(%f)\n', w, vocabs{w}, p_w_z(w,z))
%    end
%    fprintf('\n')
%end
%fprintf('\n')

%n_d_show = 10; % Pick 10 documents
%for d = 1:size(m_w_d,2)
%    fprintf('Topic weights for document %d:\n', d);
%    for z = 1:n_z
%        fprintf('%f\t', p_z_d(z,d))
%    end
%    fprintf('\n')
%end
