# README

## Projet de tournoi d'échecs

Ce projet est une application de gestion de tournois d'échecs. Il permet de créer des tournois, d'ajouter des joueurs, de gérer les matchs et les tours, et de générer des rapports.

### Structure du projet

Le projet est structuré en quatre fichiers principaux : `views.py`, `models.py`, `controller.py` et `main.py`.

#### `views.py`

Ce fichier contient la logique de l'interface utilisateur. Il comprend une classe `View` qui contient des méthodes pour afficher des menus, créer des tournois, afficher des tournois, ajouter des joueurs, afficher la liste des joueurs, démarrer des tours, définir des scores, afficher des scores, afficher la fin d'un tournoi, afficher des rapports, et plus encore.

#### `models.py`

Ce fichier contient les modèles de données pour les joueurs, les matchs, les tours et les tournois. Chaque modèle a des méthodes pour sérialiser et désérialiser ses instances en JSON.

#### `controller.py`

Ce fichier contient la logique de contrôle de l'application. Il comprend une classe `Controller` qui contient des méthodes pour créer des tournois, ajouter des joueurs, créer des matchs, définir des scores, jouer des tours, et démarrer des tournois.

#### `main.py`

Ce fichier est le point d'entrée de l'application. Il importe la classe `Controller` du fichier `controller.py` et appelle la méthode `start_tournament()` pour démarrer un tournoi.

### Comment utiliser

Pour utiliser cette application, vous devez d'abord créer un tournoi. Ensuite, vous pouvez ajouter des joueurs au tournoi. Une fois que vous avez ajouté tous les joueurs, vous pouvez commencer le tournoi. Chaque tour du tournoi consiste en une série de matchs. Après chaque match, vous devez définir le score. À la fin du tournoi, vous pouvez afficher un rapport.

### Dépendances

Ce projet dépend des bibliothèques Python suivantes :

- `json` pour sérialiser et désérialiser les données en JSON.
