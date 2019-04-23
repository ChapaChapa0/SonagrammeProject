function post_depth = post_processing_depth(l_depth)
 
% l_s_depth = [];
% 
% for k = 1:size(l_depth,2)
%     depth = l_depth{k};
%     ind_depth = find(depth > 0);
%     s_depth = size(ind_depth,1);
%     l_s_depth = [l_s_depth, s_depth];
% end
% 
% [~, k_best_depth] = max(l_s_depth);
% post_depth = l_depth{k_best_depth};

epsilon = 0.0001;

post_depth = l_depth{1};
ind_values = find(post_depth < epsilon);
l_ind_depth = {};
for k = 1:size(l_depth,2)
    depth = l_depth{k};
    ind_depth = find(depth > 0);
    l_ind_depth{end + 1} = ind_depth;
end

for i = 1:size(ind_values,1)
    i_hole = ind_values(i);
    l_values = [];
    for k = 1:size(l_depth,2)
        ind_depth = l_ind_depth{k};
        if i_hole < size(ind_depth,1) && length(find(ind_depth == i_hole))
            depth = l_depth{k};
            l_values = [l_values, depth(i_hole)];
        end
    end
    if l_values
        post_depth(i_hole) = mean(l_values);
    end
end

