function [intra_sim] = IntraSim(p_z_d, sim_intent)
% similarity inside

[n_z, n_d] = size(p_z_d);

[topic_value, topic_index] = max(p_z_d);
topic = unique(topic_index,'sorted');

sim = zeros(n_z,1);

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


K = 0;

for z = topic
    id = find(topic_index == z);
    [x1, d_n] = size(id);
    
    if d_n > 1
        for d1 = id
            for d2 = id
                if d1 ~= d2
                    sim(z) = sim(z) + sim_intent{z}(d1, d2);
                end
            end
        end
        
        sim(z) = sim(z) / (d_n * (d_n - 1));
        K = K + 1;
    end
end


if K > 0
    intra_sim = sum(sim) / K ;
else
    intra_sim = 0;
end

