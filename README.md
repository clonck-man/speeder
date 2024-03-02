# Speeeeeeeeeder 

Speeder est un projet de conduite automatique d'une voiture dans un jeu vidéo via intelligence artificielle.

Pour le moment il se découpe en plusieurs composants distincts :
- un module de jeu pour humain, permettant de prendre l'environnement en main
- un module d'entrainement des ia. Pour le moment le choix s'est porté sur l'algorithme neat. J'envisage de tenter d'implémenter ma propre version de l'algorithme et/ou d'implémenter d'autres algorithmes à l'avenir.
- un générateur basique de terrain procédural
- un outil basique de création de terrain à la main

Ce projet est le premier d'une série plus large de petits projets que je mène pour améliorer mes compétences dans le domaine de l'IA. Je n'ai suivi aucun tutoriel ou cours en ligne.

## Versions
Pour le moment le projet est en 1.0

## Fabriqué avec
* [neat-python](https://github.com/CodeReclaimers/neat-python) - une implémentation de l'algorithme neat en python
* [pygame](https://www.pygame.org/news) - une librairie de création de jeu
* [pygame-car-tutorial](https://github.com/maximryzhov/pygame-car-tutorial) - la physique de la voiture est très inspiré de ce tutoriel (mais pas identique, j'ai en bonne partie remanié ce code)

## License
Ce projet est sous licence ``Apache 2.0`` - voir le fichier [LICENSE.txt](LICENSE.txt) pour plus d'informations
