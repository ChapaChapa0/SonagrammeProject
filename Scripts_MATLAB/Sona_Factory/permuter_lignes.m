function S2 = permuter_lignes(S)
n = size(S,1);

for i = 1:n
    S2(i,:) = S(n+1-i,:);
end