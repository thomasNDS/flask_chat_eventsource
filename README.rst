Installer les dépendances
=========================

Tout d'abord installer les outils python

::

    sudo apt-get install redis-server python-virtualenv


Puis les dependances du projets dans un nouveau virtualenv
(le Makefile permet de faciliter cette tâche)

::

    make virtualenv


Lancer le serveur
=================

::

    source ./env/bin/activate
    ./server.py
    Server running on http://127.0.0.1:5001. Ctrl+C to quit
