# Vibes
## Prérequis
Le système a été développé testé et oppéré sur python 3.7<br />
Modules python:<br />

 ipython; numpy; PyQt5; PythonQwt; scipy ; pyqtgraph    (; wave)

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
Toutes ces fonctionnalités ne peuvent être appelées ***uniquement que dans le main*** (main.py) pour l'itération présente:

> ### Importer des fichiers en format csv
>
> - En démarant l'application, l'utilisateur se fera proposer d'ouvrir un fichier à travers un explorateur de fichiers
> - Le format des données doit suivre ce pattern: 
>    - EN DEVELOPPEMENT..........................................................................
>    - EN DEVELOPPEMENT..........................................................................

> ### Exporter le résultat en fichier .wav
>
> - L'utilisateur se fera présenter un explorateur de fichier pour sauvegarder son fichier .wav
> - La dernière transformation de signaux sera choisie pour l'exportation
> - Fonction à appeler dans le main: ***control.model.data.export_wav(control.model.data)***

> ### Afficher l'amplitude en fonction du temps 
>
> - Dans le cas de notre utilisation, l'amplitude correspond à l'accélération (de la fusée)
> - Elle peu toutefois correspondre à n'importe quelle valeur
> - Cette fonction est appelées automatiquement au début du programme et ne nécessite pas d'appel dans le main

> ### Afficher les séries de fourier
>
> - Affiche le contenu fréquentiel de toute la portion du graphique temporel affichée
> - Cette fonction est appelées automatiquement au début du programme et ne nécessite pas d'appel dans le main

> ### Sélectionner une portion du graphique temporel
>
> - Cette fonction permet de d'observer le contenu temporel et fréquentiel de la section du graphique choisie
> - Un nouveau graphique temporel et fréquentiel est généré suite à l'appel de cette fonction
> - Fonctions à appeler dans le main: ***control.time_range_selections(0, 300)***
>    - Les valeurs à entrer sont en millisecondes

> ### "Pipeline Browser"
>
> - Cette fonction est contenue dans une fenêtre de l'interface graphique
> - Elle permet de revisiter la séquence des transformations appliquées sur les données
> - Il est représenté à l'aide d'un bouton glissant vertical

> ### Intégrales et dérivées du graphique temporel 
>
> - Fonctions à appeler dans le dashboard:
>    - ***control.differential(control.model.data.transformations[1])***
>    - ***control.integral(control.model.data.transformations[1])***
>       - L'index passé en argument correspond à la position dans le pipeline
>    - L'intégral est encore en développement

> ### Merging
>
> - Fonctions à appeler dans le dashboard:
>    - ***control.Merging(self, data, index=-1)***
>       - L'index passé en argument correspond à la position dans le pipeline
>    

> ### Filter
>
> - Fonctions à appeler dans le dashboard:
>    - ***control.filter(self, data, cut_off, cut_off2, attenuation, fourier, type, index=-1)***
>       - L'index passé en argument correspond à la position dans le pipeline

> ### Filter_Fir
>
> - Fonctions à appeler dans le dashboard:
>    - ***control.filter_fir(self, data, sample_rate, cut_off, cut_off2, type, index=-1)***
>       - L'index passé en argument correspond à la position dans le pipeline

## Commandes en développement
- integrale
- interpolation
- position des fenêtres
- manipulation des num-taps
- plusieurs y dans les csv (pas toute les transformation le supporte)

## Problèmes connus
- ### EN DÉVELOPPEMENT

