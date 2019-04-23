function LS = calcul_LS(depth, pas, sigma, seuil)

LS = depth(1:pas:end,1:pas:end);
LS = imgaussfilt(LS, sigma);

% moyenne_sona = mean(mean(LS));
% std_sona = std(mean(LS));

condition1 = ~(LS > 0);
% condition2 = LS > moyenne_sona + std_sona;
condition2 = LS > seuil;

LS(condition1) = 0;
LS(condition2) = 0;