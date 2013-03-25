function [inter_sim] = InterSim(p_z_d, sim_intent)
% similarity between topics

[n_z, n_d] = size(p_z_d);

[topic_value, topic_index] = max(p_z_d);
topic = unique(topic_index,'sorted');

sim = zeros(n_z);

K = 0;
N = 0;


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


for z = topic
    id = find(topic_index == z);
    
    for z1 = topic
       if z ~= z1
           N = 0;
           id1 = find(topic_index == z1);
           
           for i = id
               for j = id1
                   sim(z, z1) =  sim(z, z1) + sim_intent{z}(i, j);
                   N = N + 1;
               end
           end
           if N > 0
               sim(z, z1) = sim(z, z1) / N;
               K = K+ 1;
           end
       end
    end
end


if K > 0
    inter_sim = sum(sum(sim)) / K;
else
    inter_sim = 0;
end


