### TP2 INFO 002 CRYPTOLOGIE 

Sujet : https://pierre-hyvernat.apps.math.cnrs.fr/data/Enseignement/2324/info002/tp2.html#toc_1

GITHUB : https://github.com/Yuss9/TP2_INFO002

#### IMPORTANT 
Toutes les commandes fonctionnent correctement.

### STATUS 

Equipe : YURTSEVEN Hüseyin, CHAVANCE Rémi, DURAND-NOËL Amaury
Etat : on a fait toutes les questions, sauf la partie bonus.

### SET UP LE PROJET : 

#### Si vous avez déjà installer venv sur votre python : 
```bash
python3 -m venv .myenv
```

```bash
source .myenv/bin/activate
```

```bash
pip install -r requirements.txt
```

#### Sinon vous pouvez directement faire cette commande : 

```bash
pip install -r requirements.txt
```

##### Ou : 

```bash
pip3 install -r requirements.txt
```

### COMMANDES : 

Pour générer un diplome : 

```bash
python main.py --generate ./diplome.png ./diplome_output.png 095462187AP CHAVANCE Remi 2.5 1548A9G8ER
```

Pour vérifier une signature : 

```bash
python main.py --verify ./diplome_output.png 
```

### Pour aller plus loins :

### à rédiger pour le rapport :

- QR Code afin de faciliter l'accès aux données, les étudiants pourraient avoir besoins de vérifier la validité de leur diplôme.
- Site web permettant de visualiser les infos liées au diplôme accessible grâce a un code (ou QRCode) présent sur le diplôme.
- La signature est affichée sur le diplome mais aussi dans la composante bleue de l'image, ceci afin que d'autres entités (écoles, entreprises, ...) puissent valider le diplôme.
