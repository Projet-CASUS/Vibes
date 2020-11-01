# Vibes
## Prérequis
Le système est développé testé et oppéré sur python 3.7.7.<br />
Modules python:<br />

 ipython; decimal ; numpy; PyQt5; qwt; scipy; struct; wave

## Description

Cet outil est développé en vue de représenter les forces vécues par la fusée
conçue par le Groupe CASUS de l'université de Sherbrooke dans des actuateurs haptiques.
Des données d'acceleration seront fournies au présent logiciel (actuellement sous format CSV).
Elles seront manipulées à l'aide d'une interface graphique tout le visuel et la flexibilité 
nécessaire à l'expérimentation avec les actuateurs.
Finalement des fichiers en format .wav seront produits par le logiciel afin de
pouvoir être "joués" par les actuateurs.


# Spécifications techniques  

## Commandes fonctionnelles
Toutes ces fonctionnalités ne peuvent être appelées que dans le main pour l'itération présente:
- Importer des fichiers en format csv 
- Exporter le résultat en fichier .wav 
- Afficher l'acceleration en fonction du temps 
- Afficher les séries de fourier de l'acceleration 
- Sélectionner une portion du graphique temporel et en afficher le contenu fréquentiel (Séries de fourier) 
- Intégrales et dérivées du graphique temporel 


## Commandes en développement
- Interface graphique permettant d'ajouter et de modifier les transformations du signal
- Fonctions de filtres FIR & IIR


