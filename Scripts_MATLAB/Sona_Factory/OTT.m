function S_comp = OTT(S, min_tresh, max_tresh, r, G)
[n,m] = size(S);
S2 = S;
for i = 1:n
    for j = 1:m
        if abs(S(i,j)) < min_tresh
            S2(i,j) = 0;
        else
            if abs(S(i,j)) > max_tresh
                knee = (abs(S(i,j)) - max_tresh)/max_tresh; % Quantity of attenuation
                if knee < 1
                    S2(i,j) = knee * (sign(S(i,j)) * abs(max_tresh^(1-1/r) * S(i,j)^(1/r)));
                else
                    S2(i,j) = (sign(S(i,j)) * abs(max_tresh^(1-1/r) * S(i,j)^(1/r)));
                end
            end
        end
    end
end

S_comp = G * S2;