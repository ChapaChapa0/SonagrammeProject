clear;
close all;
taille_ecran = get(0,'ScreenSize');
L = taille_ecran(3);
H = taille_ecran(4);

% Lecture d'un extrait musical :
[signal,f_echantillonnage] = audioread('C:\Users\Hatem\Documents\Paul\SonagrammeProject\Scripts_MATLAB\Audio\empreintes_2.wav');
sound(signal,f_echantillonnage);
if size(signal,2)==2
	signal = mean(signal,2);		% Conversion stereo -> mono
end

% Calcul de la transformee de Gabor :
nb_echantillons = length(signal);
duree = floor(nb_echantillons/f_echantillonnage);
duree_mesure = 0.05;				% Duree d'une mesure en secondes
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

% Calcul du sonagramme complexe :
S = TG(1:nb_echantillons_f_S,:);

% Affichage du sonagramme :
figure('Name','Sonagramme','Position',[0,0,0.5*L,0.6*H]);
imagesc(valeurs_t,valeurs_f_S,abs(S));
axis xy;
set(gca,'FontSize',20);
xlabel('Temps ($s$)','Interpreter','Latex','FontSize',30);
ylabel('Frequence ($Hz$)','Interpreter','Latex','FontSize',30);
drawnow;

% Calcul de la partition frequentielle :
nb_bandes = 6;
partition = exp(log(f_min):(log(f_max)-log(f_min))/nb_bandes:log(f_max));
indices_partition = zeros(1,nb_bandes);
for i = 1:nb_bandes
	indices_partition(i) = min(find(valeurs_f_S>partition(i)));
end
indices_partition(end+1) = length(valeurs_f_S);

% Calcul de l'empreinte sonore :
ES = calcul_ES(S,indices_partition,valeurs_t,valeurs_f_S);

% Affichage de l'empreinte sonore :
figure('Name','Empreinte sonore','Position',[0.5*L,0,0.5*L,0.6*H]);
plot(ES(:,1),log(ES(:,2)/f_min),'o','MarkerEdgeColor','b','MarkerFaceColor','b','MarkerSize',5);
set(gca,'FontSize',20);
xlabel('$t$ ($s$)','Interpreter','Latex','FontSize',30);
ylabel('$\log\left(f/f_{\min}\right)$','Interpreter','Latex','FontSize',30);
axis([valeurs_t(1) valeurs_t(end) 0 log(f_max/f_min)]);
hold on;
for i = 2:length(indices_partition)-1
	plot([valeurs_t(1) valeurs_t(end)],[log(partition(i)/partition(1)) log(partition(i)/partition(1))],'-r');
end


%% Modifications sonagramme
% On construit le sonagramme de manière à avoir la partie positive et
% la partie négative en miroir
S2 = permuter_lignes(repmat(S,[2,1]));
S2(S2 > 0) = 0;
S2 = abs(S2);
S3 = S;
S3(S3 < 0) = 0;

k = size(S,1);
S2(k+1:end,:) = S3;

% Lissage du sonagramme (interpolation)
valeurs_f_S = linspace(-f_max,f_max,size(S2,1));
[t_grid, f_S_grid] = meshgrid(valeurs_t, valeurs_f_S);
nb_points = 100;
[xq,yq] = meshgrid(linspace(0,duree,nb_points),linspace(-f_max,f_max,nb_points));
S4 = interp2(t_grid, f_S_grid,S2,xq,yq);

% On modifie le sonagramme S afin d'avoir "un socle" (pour avoir une
% structure fermé)
S0 = zeros(size(S4,1),size(S4,2));
S0(2:end-1,2:end-1) = S4(2:end-1,2:end-1);
epaisseur_socle = max(max(S0))/20; % Définit l'épaisseur du socle
S0 = S0 + epaisseur_socle;

[F, V] = surf2solid(xq,yq,S0,'ELEVATION',0);

figure('Name','Sonagramme imprimable','Position',[0,0,L,0.6*H]);
trisurf(F,V(:,1),V(:,2),V(:,3));
xlabel('Time (s)','FontSize',20);
ylabel('Frequency (Hz)','FontSize',20);
zlabel('Intensity','FontSize',20)

%% Sauvegarde du fichier stl du sonagramme
stlwrite('C:\Users\Hatem\Documents\Paul\SonagrammeProject\Scripts_MATLAB\Gen\test.stl',F,V);

save ecriture_sonagramme
