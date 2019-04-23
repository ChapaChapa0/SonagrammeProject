function ES = calcul_ES(S,indices_partition,valeurs_t,valeurs_f_S)

ES = [];		% Chaque ligne de ES contient un point de l'empreinte sonore
for i = 1:length(indices_partition)-1

	[maxima,indices_maxima] = max(abs(S(indices_partition(i):indices_partition(i+1)-1,:)));
	moyenne_maxima = mean(maxima);
	ecart_type_maxima = std(maxima);

	% Filtrage des maxima locaux de la bande :
	seuil = moyenne_maxima+ecart_type_maxima;
	indices_ES = find(maxima>seuil);

	% Transcription en secondes et en Hertz :
	t_ES = valeurs_t(indices_ES);
	f_ES = valeurs_f_S(indices_partition(i)+indices_maxima(indices_ES)-1);

	ES = [ES ; transpose(t_ES) transpose(f_ES)];

end
