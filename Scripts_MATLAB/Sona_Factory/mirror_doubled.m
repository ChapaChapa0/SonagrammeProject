function A_d = mirror_doubled(A)

k = size(A,1);
A_d = repmat(permuter_lignes(A,[2,1]));
A_d(k+1:end,:);