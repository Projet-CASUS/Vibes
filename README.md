# Vibes
## Prérequis
Le système a été développé testé et oppéré sur python 3.7<br />
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
Toutes ces fonctionnalités ne peuvent être appelées ***uniquement que dans le main*** (main.py) pour l'itération présente:

> ### Importer des fichiers en format csv
>
> - En démarant l'application, l'utilisateur se fera proposer d'ouvrir un fichier à travers un explorateur de fichiers
> - Le format des données doit suivre ce pattern: 
>    - blabla..........................................................................
>    - blabla..........................................................................

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
> - Fonctions à appeler dans le main:
>    - ***control.differential(control.model.data.transformations[1])***
>    - ***control.integral(control.model.data.transformations[1])***
>       - L'index passé en argument correspond à ........................................................

## Structure de données
- ### EN DÉVELOPPEMENT

## Commandes en développement
- Interface graphique permettant d'ajouter et de modifier les transformations du signal
- Fonctions de filtres FIR & IIR

## Problèmes connus
- ### EN DÉVELOPPEMENT

