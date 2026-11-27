# Sunflower — animation générative en Python

Un tournesol dessiné par du code, animé étape par étape et accompagné d'un
message personnalisable. Ce petit projet pédagogique explore le dessin 2D, la
géométrie, les GIF animés, la gestion d'un cache et une interface de bureau.

![Animation du tournesol](Sunflower_animation.gif)

## Fonctionnalités

- Dessine une tige, des feuilles, 34 pétales, un cœur et des graines.
- Répartit les graines selon un motif inspiré de la phyllotaxie et de l'angle
  d'or.
- Révèle progressivement les étapes du dessin dans un GIF en boucle.
- Affiche l'animation dans une fenêtre de bureau Tkinter.
- Permet de personnaliser le texte affiché au centre du tournesol.
- Réutilise la sauvegarde existante au lancement suivant.
- Permet de régénérer le GIF avec l'option `--regenerate`.

Le GIF présent dans le dépôt est une prévisualisation et la sauvegarde utilisée
par le programme. Il mesure 900 × 900 pixels et contient 90 images.

## Prérequis

- Python 3.10 ou plus récent.
- Pillow, installée dans le même environnement Python que celui qui lance le
  programme.
- Tkinter, généralement fourni avec Python. Certaines distributions Linux
  peuvent nécessiter l'installation séparée de Tkinter.

## Installation et lancement

Dans PowerShell, ouvre le dossier du projet puis exécute :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python .\Sunflower2.py
```

Par défaut, le tournesol affiche « Hello world ». Le premier lancement crée
`Sunflower_animation.gif` à côté du script s'il n'existe pas déjà. Les
lancements suivants réutilisent cette sauvegarde.

Pour choisir un autre texte, passe-le avec `--message` :

```powershell
python .\Sunflower2.py --message "Hello, GitHub!"
```

Le texte est automatiquement ajusté et réparti sur plusieurs lignes pour tenir
dans le cœur. Garde un message assez court pour qu'il reste lisible. Chaque
texte personnalisé possède son propre GIF en cache ; ainsi, le programme ne
réutilise pas par erreur une animation contenant un autre message. Ces GIF
personnalisés sont ignorés par Git afin de ne pas publier accidentellement des
messages personnels.

Pour recréer l'animation du texte demandé et remplacer sa sauvegarde :

```powershell
python .\Sunflower2.py --message "Hello, GitHub!" --regenerate
```

`--regenerate` fonctionne aussi sans `--message` pour recréer l'animation
générique « Hello world ».

Le chemin Python et le chemin du fichier sont chacun entourés de guillemets si
on les écrit directement et que le chemin contient des espaces. Exemple :

```powershell
& "C:\chemin avec espaces\python.exe" ".\Sunflower2.py"
```

## Vérification

Les tests utilisent `unittest`, inclus dans Python :

```powershell
python -m unittest discover -s tests -v
```

## Notions et domaines d'application

| Notion | Dans ce projet | Applications possibles |
|---|---|---|
| Repères et coordonnées | Conversion entre origine centrée et pixels | Interfaces, jeux 2D, cartographie, visualisation |
| Trigonométrie | Placement des points, pétales et feuilles | Animation, robotique, trajectoires, modélisation |
| Angle d'or et phyllotaxie | Répartition des graines en spirale | Art génératif, motifs, particules, simulation de croissance |
| Géométrie des polygones | Construction des pétales, feuilles et cœur | Icônes, logos, jeux, formes vectorielles |
| Dessin raster avec Pillow | Création de la toile et tracé des formes | Vignettes, graphiques, traitement d'images, exports |
| Animation par images | Capture des étapes successives du dessin | GIF, aperçus, tutoriels visuels, visualisations |
| Interface événementielle | Lecture image par image avec Tkinter | Outils de bureau et interfaces interactives |
| Fichiers et chemins portables | Sauvegarde à côté du programme avec `pathlib` | Configuration, exports et outils multiplateformes |
| Cache et régénération explicite | Réutilisation du GIF avec une option de mise à jour | Calculs coûteux, téléchargements, génération de rapports |
| Tests et diagnostic | Vérification du dessin et du cache sans fenêtre | Fiabilité des scripts, automatisation et intégration continue |
| Dépendances Python | Installation cohérente de Pillow dans l'environnement actif | Projets Python reproductibles et travail en équipe |

Une fiche plus détaillée est disponible dans
[Fiche-notions-Sunflower.md](Fiche-notions-Sunflower.md).

## Structure du projet

```text
.
├── .gitignore
├── Fiche-notions-Sunflower.md
├── README.md
├── requirements.txt
├── Sunflower2.py
├── Sunflower_animation.gif
└── tests/
    └── test_sunflower.py
```
