clear;
close all;
taille_ecran = get(0,'ScreenSize');
L = taille_ecran(3);
H = taille_ecran(4);

% Lecture d'un extrait musical :
[signal,f_echantillonnage] = audioread('C:\Users\Hatem\Documents\Paul\SonagrammeProject\Scripts_MATLAB\Audio\empreintes_2.wav');
% sound(signal,f_echantillonnage);
if size(signal,2)==2
	signal = mean(signal,2);		% Conversion stereo -> mono
end

% Calcul de la transformee de Gabor :
nb_echantillons = length(signal);
duree = floor(nb_echantillons/f_echantillonnage);
duree_mesure = 0.1;				% Duree d'une mesure en secondes
nb_mesures = floor(duree/duree_mesure);
valeurs_t = 0:duree/(nb_mesures-1):duree;
nb_echantillons_par_mesure = floor(nb_echantillons/nb_mesures);
TG = gabor(signal,nb_echantillons_par_mesure);

% Bande de frequences audibles :
f_min = 20;
f_max = 2000;
pas_f = f_echantillonnage/nb_echantillons_par_mesure;
valeurs_f_S = 0:pas_f:f_max;
nb_echantillons_f_S = length(valeurs_f_S);

% Calcul du sonagramme :
S = TG(1:nb_echantillons_f_S,:);

% Affichage du sonagramme :
figure('Name','Sonagramme','Position',[0,0,0.5*L,0.6*H]);
imagesc(valeurs_t,valeurs_f_S,abs(S));
axis xy;
set(gca,'FontSize',20);
xlabel('Temps ($s$)','Interpreter','Latex','FontSize',30);
ylabel('Frequence ($Hz$)','Interpreter','Latex','FontSize',30);
drawnow;

% Parameters for multiband dynamic compression
min_tresh = max(abs(S(:))) * 1/100;
max_tresh = max(abs(S(:))) * 50/100;
ratio = 5;
gain = 3;

% Compressing the signal with a function which simulate a multiband compressor
S_comp = OTT(S, min_tresh, max_tresh, ratio, gain);
S_comp = S;

% Affichage du sonagramme compressé :
figure('Name','Sonagramme (compressed)','Position',[0,0,0.5*L,0.6*H]);
imagesc(valeurs_t,valeurs_f_S,abs(S_comp));
axis xy;
set(gca,'FontSize',20);
xlabel('Temps ($s$)','Interpreter','Latex','FontSize',30);
ylabel('Frequence ($Hz$)','Interpreter','Latex','FontSize',30);
drawnow;

%% Modifications sonagramme

% On construit le sonagramme de manière à avoir la partie positive et
% la partie négative en miroir
S_comp = S_comp(200:end,:);
S_neg = S_comp;
S_neg(S_neg > 0) = 0;
S_neg = abs(S_neg);
S_pos = S_comp;
S_pos(S_pos < 0) = 0;
S_pos = abs(S_pos);

% On effectue une 'compression multibande' sur le sonagramme pour rendre
% chaque bande de fréquence plus égale en amplitude

% Calcul de la partition frequentielle :
nb_bandes = 6;
partition = exp(log(f_min):(log(f_max)-log(f_min))/nb_bandes:log(f_max));
indices_partition = zeros(1,nb_bandes);
for i = 1:nb_bandes
	indices_partition(i) = min(find(valeurs_f_S>partition(i)));
end
indices_partition(end+1) = length(valeurs_f_S);

% Calcul de l'empreinte sonore :
S2 = permuter_lignes(repmat(S_pos,[2,1]));
k = size(S_comp,1);
S2(k+1:end,:) = S_neg;

% Lissage du sonagramme (interpolation)
valeurs_f_S_2 = linspace(-f_max,f_max,size(S2,1));
[t_grid, f_S_grid] = meshgrid(valeurs_t, valeurs_f_S_2);

nb_points = 100; % Definit la 'quantite' d'interpolation du sonagramme
[xq,yq] = meshgrid(linspace(0,duree,nb_points),linspace(-f_max,f_max,nb_points));
S3 = interp2(t_grid, f_S_grid,S2,xq,yq);

% On modifie le sonagramme S afin d'avoir "un socle" (pour avoir une
% structure fermé)
S0 = zeros(size(S3,1),size(S3,2));
S0(2:end-1,2:end-1) = S3(2:end-1,2:end-1);

ratio_socle_maxpic = 5/100; % Definit l'épaisseur du socle
epaisseur_socle = max(max(S0)) * ratio_socle_maxpic;
S0 = S0 + epaisseur_socle;

[F, V] = surf2solid(xq,yq,S0,'ELEVATION',0);

figure('Name','Sonagramme imprimable','Position',[0,0,L,0.6*H]);
trisurf(F,V(:,1),V(:,2),V(:,3));

%% Sauvegarde du fichier stl du sonagramme
stlwrite('C:\Users\Hatem\Documents\Paul\Scripts_MATLAB\Gen\test.stl',F,V);

save ecriture_sonagramme
