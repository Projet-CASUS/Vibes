# Vibes
## Prérequis
Le système est développé testé et oppéré sur python 3.7.7.<br />
Modules python:<br />

 * ipython
 * decimal
 * numpy
 * pandas
 * PyQt5
 * qwt
 * scipy
 * struct
 * wave

## Description
Ce code est un interpréteur/générateur de signaux ayant pour but de produire
les ondes nécéssaire aux fonctionnement d'appareil haptique.

Cet outil est développé en vue de représenter les forces vécues par la fusée
conçue par le Groupe CASUS de l'université de Sherbrooke dans des actuateurs haptiques.
Des données d'acceleration seront fournies au présent logiciel (actuellement sous format CSV).
Elles seront manipulées à l'aide d'une interface graphique tout le visuel et la flexibilité 
nécessaire à l'expérimentation avec les actuateurs.
Finalement des fichiers en format .wav seront produits par le logiciel afin de
pouvoir être "joués" par les actuateurs.


# Spécifications techniques  
##commandes fonctionnelles  
Importer des fichiers csv 
Afficher l'acceleration en fonction du temps
Afficher les séries de fourier de l'acceleration d'une section de vol choisie


### Commandes en développement
- Dérivées / intégrales
- Filtres FIR & IIR
- Extraction .wav
- Interface graphique

