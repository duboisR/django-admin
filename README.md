# django-admin

Un mini projet pour apprendre les bases en Django Admin.

Plugins:
- [django](https://www.djangoproject.com/)


## Développement Pipenv

Pour lancer le projet localement sur votre machine de développement:

```sh
$ pipenv shell
$ ./manage.py runserver
```

Vérifier que le projet se lance bien sur [http://localhost:8000/](http://localhost:8000/)


### Environnement avec pipenv

Pour installer pipenv, il vous suffit de suivre la [documentation](https://pypi.org/project/pipenv/). Ou bien simplement de lancer la commande suivantes
```sh
pip install --user pipenv
```

Il faut ensuite se mettre dans le dossier qui contient le fichier `Pipfile` (dans notre cas le dossier `app`)

Installer l'environnement :
```sh
$ pipenv install
```

Installer les packages utiles au debug :
```sh
$ pipenv install --dev
```

Lorsqu'on veut installer un nouveau paquet, ne pas utiliser `pip install` mais `pipenv install`, cela l'ajoutera automatiquement au fichier `Pipfile`.

Utiliser l'environnement :

```sh
$ pipenv shell
```

Maintenant on peut lancer toutes les commandes `migrate.py`


### Première utilisation

Lors de la première utilisation, ne pas oublier de lancer la première migration.

```sh
$ ./manage.py migrate
```


### Création d'un compte super utilisateur

Pour créer un compte super utilisateur:

```sh
$ ./manage.py createsuperuser
```

Il vous suffit ensuite de vous connecter à la [page d'administration Django](http://localhost:8000/rmas-admin/) avec les identifiants que vous avez renseigné.



## Développement Docker

Pour lancer le projet localement sur votre machine de développement:

```sh
$ docker-compose up -d --build
```

Vérifier que le projet se lance bien sur [http://localhost:8000/](http://localhost:8000/)


### Environnement avec docker

Pour installer docker, il vous suffit de suivre la [documentation](https://docs.docker.com/engine/install/ubuntu/).
Pour installer docker-compose, il vous suffit de suivre la [documentation](https://docs.docker.com/compose/install/).


### Première utilisation

Lors de la première utilisation, ne pas oublier de lancer la première migration.

```sh
$ docker-compose exec web ./manage.py migrate
```


### Création d'un compte super utilisateur

Pour créer un compte super utilisateur:

```sh
$ docker-compose exec web ./manage.py createsuperuser
```

Il vous suffit ensuite de vous connecter à la [page d'administration Django](http://localhost:8000/rmas-admin/) avec les identifiants que vous avez renseigné.



## Modification du thème/ReactJs

Nous utilisons Webpack pour concaténer/minifier/bunble nos fichiers JS + SCSS.

Version NVM / NPM
```
$ nvm list
    [...]
->      v15.3.0
default -> node (-> v15.3.0)
node -> stable (-> v15.3.0) (default)
stable -> 15.3 (-> v15.3.0) (default)
[...]

$ npm --version
7.0.14
```

Pour lancer le watcher de webpack
```sh
$ cd app/assets
$ npm install
$ npm run watch
```

Pour faire un build pour la mise en prod
```sh
$ cd app/assets
$ npm run build
```


## Projet

Ce mini projet a été mis en place pour vous permettre de découvrir/apprendre/perfectionner les bases en Django Admin.
Une première App Django (invoice1) sera créée et utilisera la mise en page de Django Admin basique.
La seconde App Django (invoice2) utilisera quant à elle une mise en page de Django Admin customisée.

Un, deux, trois... c'est partie.

STEP 1: Ajout des verboses names.
STEP 2: Ajout des Meta classes.
STEP 3: Ajout des methodes __str__ + utilisation dans le Tableau de Django Admin.
STEP 4: Ajout des methodes + utilisation dans le Tableau de Django Admin.
STEP 5: Renomer l'App dans la page d'accueil de Django Admin
STEP 6: Dynamiser la page Facture