# MeteoReddit

# Nicolas Jeffrey Théo

# Contexte du projet
Vous faites partie d’une équipe de data scientists au sein d’une entreprise de vente de composants informatiques aux particuliers (B2C). Votre communication passe principalement par la publication de contenu sur les réseaux sociaux, en particulier Reddit.

Cependant, les responsables communication ont fait remonter leurs interrogations quant à la date de parution de certains contenus, qui semble avoir un impact sur le nombre de vues et de commentaires postés. On soupçonnerait presque les amateurs de matériel informatique de sortir dehors les jours de beau temps.

Votre responsable vous a donc demandé de réaliser une étude sur l’impact de la météo sur le nombre de retours sur les publications de l’entreprise. Il est important de pouvoir réitérer cette analyse au cours de l’année, on attend donc un script qui pourra être facilement exécuté tout au long de l’année.

Cheminement: La première étape consiste en la récupération des données météorologiques des journées concernées. D’après l’équipe de communication, les températures, risques de pluie, force du vent et autres informations peuvent être récupérées sur de nombreux sites web, comme par exemple weather.com.

Ensuite, on pourra s’attaquer à la récupération du niveau de suivi des publications sur Reddit. On pourra s’intéresser par exemple au nombre de votes, au nombre de commentaires, à la durée de présence sur la première page, etc.

Ces données correctement récupérées, traitées et nettoyées devront ensuite être mises en relation, afin de mettre en évidence la présence d’une éventuelle corrélation.

# How to use

python3 reddit.py
python3 meteo.py
python3 analyse.py
