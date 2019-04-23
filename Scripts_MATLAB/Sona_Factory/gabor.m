function TG = gabor(signal,nb_echantillons_par_mesure)

nb_echantillons = length(signal);
TG = [];
debut_fenetre = 1;
fin_fenetre = nb_echantillons_par_mesure;
while fin_fenetre<=nb_echantillons
	signal_fenetre = signal(debut_fenetre:fin_fenetre);	% signal est un vecteur colonne !
	TG = [TG dct(signal_fenetre)];
	debut_fenetre = debut_fenetre+nb_echantillons_par_mesure;
	fin_fenetre = fin_fenetre+nb_echantillons_par_mesure;
end
