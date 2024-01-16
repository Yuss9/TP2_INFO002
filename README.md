### TP2 INFO 002 CRYPTOLOGIE 

Sujet : https://pierre-hyvernat.apps.math.cnrs.fr/data/Enseignement/2324/info002/tp2.html#toc_1

GITHUB : https://github.com/Yuss9/TP2_INFO002

### STATUS 

Equipe : YURTSEVEN Hüseyin, CHAVANCE Rémi, DURAND-NOËL Amaury


### SET UP LE PROJET : 

```bash
python3 -m venv .myenv
```

```bash
source .myenv/bin/actti
```

```bash
pip install -r requirements.txt
```

### COMMANDES : 

Pour générer un diplome : 

```bash
python main.py --generate ./diplome.png ./diplome_output.png 095462187AP CHAVANCE Remi 15.5 1548A9G8ER
```

Pour vérifier une signature : 

```bash
python main.py --verify ./diplome_output.png 
```

### Pour aller plus loins :

- QR Code afin de faciliter l'accès aux données, les étudiants pourraient avoir besoins de vérifier la validité de leur diplôme.
- Site web permettant de visualiser les infos liées au diplôme accessible grâce a un code (ou QRCode) présent sur le diplôme.
- Signature affichée sur le diplome mais aussi dans la composante bleue de l'image, ceci afin que d'autres entité (écoles, entreprises) puissent