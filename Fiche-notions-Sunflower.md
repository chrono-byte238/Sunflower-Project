# Fiche de notions — projet Sunflower

Cette fiche récapitule les notions de Python, de géométrie, de graphisme et de
débogage mobilisées pour créer le tournesol animé, enregistrer son animation en
GIF et rejouer la sauvegarde aux lancements suivants.

Le programme étudié est [Sunflower2.py](./Sunflower2.py). Il utilise Pillow
pour dessiner et produire le GIF, ainsi que Tkinter pour afficher l’animation.

## 1. Structure d’un programme Python

### Imports et bibliothèques

Au début du fichier, les instructions `import` rendent disponibles des outils :

- `math` fournit `sin`, `cos`, `sqrt`, `pi` et les conversions degrés/radians ;
- `pathlib.Path` construit et manipule des chemins de fichiers ;
- `argparse` lit les options entrées dans le terminal ;
- `tkinter` crée la fenêtre d’affichage ;
- Pillow (`PIL`) dessine les images, choisit les polices et les affiche dans
  Tkinter.

`math`, `pathlib`, `argparse` et Tkinter font partie de la bibliothèque standard
de Python, même si Tkinter peut manquer dans certaines distributions. Pillow est
une dépendance externe : elle doit être installée dans le même environnement
Python que celui utilisé pour exécuter le script.

```powershell
python -m pip install Pillow
```

**Applications dans d’autres projets :** les imports permettent de séparer les
outils généraux de la logique propre au programme. On peut ainsi ajouter une
bibliothèque pour lire des fichiers CSV, traiter des images, communiquer avec
une API ou accéder à une base de données.

### Constantes et fonctions

Les valeurs comme `WIDTH`, `HEIGHT`, `FLOWER_X` et `FLOWER_Y` sont définies une
fois au début, puis réutilisées dans le programme. Les fonctions
`draw_animation`, `save_animation` et `play_animation` regroupent des tâches
distinctes.

**Applications :** définir des constantes facilite l’ajustement d’une interface
ou d’un dessin. Séparer un programme en fonctions rend les tests, les
modifications et la réutilisation plus simples.

### Point d’entrée

La condition suivante lance `main()` seulement quand le fichier est exécuté
directement :

```python
if __name__ == "__main__":
    main()
```

Si un autre fichier importe `Sunflower2.py`, le dessin ne démarre donc pas
automatiquement.

**Applications :** cette convention permet de réutiliser des fonctions d’un
script dans un autre programme sans déclencher immédiatement son interface ou
ses traitements.

## 2. Repères, coordonnées et géométrie

### Transformer les coordonnées du dessin

Le dessin est décrit avec une origine au centre de la fenêtre : l’axe `x`
augmente vers la droite et l’axe `y` vers le haut. Les images Pillow, elles,
utilisent une origine en haut à gauche et un axe vertical qui augmente vers le
bas. `image_point()` convertit les coordonnées d’un système à l’autre :

```python
x_image = WIDTH / 2 + x
y_image = HEIGHT / 2 - y
```

Le signe moins devant `y` inverse la direction verticale.

**Applications :** la conversion entre repères est courante en dessin 2D,
interfaces graphiques, cartographie, jeux et visualisation de données.

### Trigonométrie et radians

Les fonctions `math.sin` et `math.cos` positionnent les points d’une courbe, les
feuilles et les pétales. Elles attendent un angle exprimé en radians. Pour
convertir un angle `a` en degrés :

```python
angle_radians = math.radians(a)
```

Pour un cercle de rayon `r`, les coordonnées autour du centre sont :

```python
x = centre_x + r * math.cos(angle)
y = centre_y + r * math.sin(angle)
```

**Applications :** la trigonométrie sert à placer des objets circulaires,
orienter des sprites, construire des trajectoires et dessiner des courbes.

### Pétales et feuilles comme polygones

Le script calcule une série de points, puis demande à Pillow de relier ces
points pour remplir un polygone. Pour former un pétale ou une feuille, il
calcule aussi un axe perpendiculaire à sa direction. Une largeur variable,
réduite aux extrémités, donne une forme effilée.

La boucle sur `side` construit les deux côtés du contour. Les points du second
côté sont parcourus en sens inverse afin de fermer le polygone sans croiser son
contour.

**Applications :** les polygones conviennent aux icônes, logos, cartes simples,
personnages de jeux et formes décoratives.

### Angle d’or et répartition des graines

Le script définit :

```python
GOLDEN_ANGLE = math.pi * (3 - math.sqrt(5))
```

Cet angle vaut environ 2,4 radians, soit 137,5°. À chaque graine, le programme
augmente l’angle par cette valeur et augmente la distance au centre selon
`3.9 * sqrt(index)`. Le résultat est une disposition en spirale qui remplit
approximativement le disque du cœur.

**Applications :** la phyllotaxie et les angles d’or servent à créer des motifs
qui répartissent des points, des feuilles, des particules ou des objets dans
une zone circulaire.

### Courbe paramétrique du cœur

Le contour du cœur est calculé par une formule utilisant `sin` et `cos`. Le
programme évalue cette formule pour 121 angles, collecte les coordonnées, puis
remplit le polygone obtenu.

**Applications :** les courbes paramétriques permettent de représenter des
cœurs, étoiles, rosaces, trajectoires et formes mathématiques personnalisées.

## 3. Dessiner une image avec Pillow

### Toile, outils et primitives

`Image.new()` crée une image de 900 × 900 pixels. `ImageDraw.Draw()` fournit les
outils pour dessiner dessus. Le script utilise notamment :

- `line()` pour la tige et les nervures ;
- `polygon()` pour les pétales, les feuilles et le cœur ;
- `ellipse()` pour le disque central et les graines ;
- `multiline_text()` pour le message personnalisable ;
- `ImageFont` pour charger une police.

Les couleurs sont définies avec des codes hexadécimaux, par exemple `#101b22`
pour le fond.

**Applications :** Pillow sert à produire des vignettes, cartes, graphiques,
images générées automatiquement, aperçus et outils de traitement par lots.

### Police de secours et gestion ciblée d’erreur

Le code tente de charger `arialbd.ttf`. Si cette police n’est pas trouvée, il
intercepte l’exception `OSError` et utilise la police par défaut de Pillow.
Cela évite qu’une police absente empêche de créer l’image.

Le texte par défaut est « Hello world ». L’option `--message` accepte un texte
différent et le programme ajuste sa taille pour l’insérer dans le cœur :

```powershell
python .\Sunflower2.py --message "Bonjour tout le monde"
```

Le texte est réparti en lignes et la taille de police est réduite si nécessaire.
Un message trop long pour rester lisible est refusé avec une erreur explicite.

**Applications :** prévoir une solution de repli est utile pour les ressources
facultatives, comme une police, un thème ou une image décorative. Il vaut mieux
intercepter l’erreur attendue précisément plutôt que de masquer toute erreur
avec un `except` général.

## 4. Animation et format GIF

### Une animation est une suite d’images

`draw_animation()` maintient une image de travail (`canvas`) et une liste
`frames`. Le programme ajoute une copie quantifiée de la toile à différents
moments du dessin. Les étapes enregistrées montrent donc la tige qui pousse,
puis les feuilles, les pétales, les graines et enfin le message.

`add_frame()` réduit chaque image à un maximum de 256 couleurs, limite du GIF,
et ajoute l’image à la liste. Une durée associée à chaque image contrôle le
temps d’affichage correspondant.

**Applications :** le principe « suite d’états + durée » sert aux GIF, aux
animations d’interface, aux aperçus de progression et à la visualisation de
simulations.

### Enregistrer un GIF animé

`save_animation()` utilise la première image comme image initiale et ajoute
les autres avec `append_images`. Les options utilisées ont ces rôles :

- `save_all=True` demande d’enregistrer plusieurs images ;
- `duration` indique le temps d’affichage des images ;
- `loop=0` demande une lecture répétée en boucle ;
- `disposal=2` aide à effacer l’image précédente avant d’afficher la suivante.

Le GIF créé contient environ 90 images pour le dessin courant.

**Applications :** les GIF sont pratiques pour partager une animation simple
sans lecteur vidéo spécialisé. Pour des animations longues ou très détaillées,
une vidéo ou une séquence d’images peut être plus adaptée en taille et en
qualité.

## 5. Sauvegarde réutilisable et chemins de fichiers

### Enregistrer à côté du script

Le chemin de sauvegarde est défini avec :

```python
ANIMATION_FILE = Path(__file__).with_name("Sunflower_animation.gif")
```

`__file__` désigne le fichier Python. La sauvegarde est donc placée à côté du
script, même si l’on lance celui-ci depuis un autre dossier.

**Applications :** `pathlib` évite de fabriquer manuellement des chemins avec
des séparateurs propres à Windows ou à d’autres systèmes.

### Réutiliser la sauvegarde et forcer sa recréation

Dans `main()`, `ANIMATION_FILE.exists()` vérifie si le GIF existe. S’il
manque, le script le crée. S’il existe, le programme le rejoue au lieu de
recalculer toute l’animation.

L’option `--regenerate`, définie avec `argparse`, force la création d’une
nouvelle version :

```powershell
python ".\Sunflower2.py" --regenerate
```

Sans cette option, le lancement normal réutilise le fichier :

```powershell
python ".\Sunflower2.py"
```

Chaque texte personnalisé produit un nom de GIF déterministe à partir d’une
empreinte SHA-256 du texte. Deux messages distincts ne partagent donc pas le
même cache, et relancer un message déjà généré permet de réutiliser sa
sauvegarde. Les GIF personnalisés sont ignorés par Git afin de ne pas publier
accidentellement des messages privés ; le GIF générique « Hello world » reste
le visuel d’aperçu du dépôt.

**Applications :** ce modèle de cache est utile pour éviter de refaire un
calcul coûteux, télécharger à nouveau des ressources ou recréer un aperçu à
chaque démarrage. Il faut prévoir une manière de régénérer le cache lorsque le
code ou les paramètres changent.

### Remplacement plus sûr du fichier

Le GIF est d’abord écrit dans `Sunflower_animation.tmp.gif`. Une fois
l’enregistrement terminé, `replace()` le renomme en `Sunflower_animation.gif`.
Ainsi, le fichier final existant n’est pas remplacé par un GIF partiellement
écrit si l’enregistrement échoue avant la fin. Le bloc `finally` supprime le
fichier temporaire restant.

**Applications :** écrire dans un fichier temporaire avant de remplacer la
version finale est une technique utilisée pour des sauvegardes, fichiers de
configuration et exports.

## 6. Afficher l’animation avec Tkinter

`play_animation()` crée une fenêtre Tkinter et ouvre le GIF avec Pillow. La
fonction imbriquée `show_frame(index)` :

1. sélectionne une image avec `seek(index)` ;
2. la convertit en image utilisable par Tkinter ;
3. l’affiche dans un `Label` ;
4. programme l’image suivante avec `root.after()`.

L’indice `(index + 1) % frame_count` revient à zéro après la dernière image et
permet la lecture en boucle. `root.mainloop()` garde la fenêtre active et
laisse Tkinter traiter les événements.

`label.image = frame` garde une référence Python vers l’image affichée ;
sans cette référence, certaines images Tkinter peuvent être libérées par le
ramasse-miettes.

**Applications :** le modèle d’événements Tkinter est utile pour les petits
lecteurs, outils de bureau, fenêtres de réglages et interfaces de visualisation.
`after()` permet d’attendre sans bloquer la boucle d’événements avec une boucle
de lecture manuelle.

## 7. Ligne de commande et chemins avec espaces

Les guillemets autour d’un chemin contenant des espaces doivent être traités
par le terminal comme des délimiteurs, et non comme des caractères du nom du
fichier. Depuis le dossier du projet, une commande PowerShell correcte est :

```powershell
python ".\Sunflower2.py"
```

Une erreur telle que `[Errno 22] Invalid argument` avec un chemin qui contient
des guillemets au milieu du nom peut indiquer que ceux-ci ont été transmis à
Python comme partie du chemin.

**Applications :** savoir lire la commande réellement exécutée aide à
diagnostiquer les problèmes de chemins, d’espaces, de répertoires courants et
d’interpréteurs différents.

## 8. Dépendances et environnements Python

Un import réussi dépend de l’environnement Python qui exécute le fichier. Le
projet a d’abord tenté d’importer `Scene` et `glow` depuis un paquet nommé
`bloom`, mais l’installation observée ne fournissait pas ces noms : il
s’agissait d’un autre projet Python appelé `bloom`.

La version actuelle dessine avec Pillow et Tkinter ; elle ne dépend plus de
`bloom`. Pillow doit toutefois être installée dans l’interpréteur effectivement
sélectionné par VS Code. Pour vérifier ou installer la dépendance dans cet
interpréteur :

```powershell
python -m pip show Pillow
python -m pip install Pillow
```

**Applications :** cette notion est essentielle dès qu’un poste possède
plusieurs versions de Python ou plusieurs environnements virtuels. Installer un
paquet dans un interpréteur ne l’installe pas automatiquement dans les autres.

## 9. Vérification et débogage

Pendant le projet, deux contrôles complémentaires ont été utilisés :

- le contrôle syntaxique et les diagnostics Pylance pour repérer les erreurs
  détectables sans ouvrir la fenêtre ;
- une simulation de l’API graphique pour vérifier la création du GIF, ses 90
  images et la réutilisation du cache au lancement suivant.

La simulation vérifie la logique du programme, mais ne remplace pas un essai
visuel sur l’ordinateur cible : l’ouverture de fenêtre dépend de Tkinter et de
l’environnement graphique.

**Applications :** tester séparément la génération, la sauvegarde, le cache et
l’affichage aide à localiser une panne. Une erreur de syntaxe, une dépendance
absente, un chemin incorrect et une fenêtre qui ne s’ouvre pas sont des
problèmes différents et ne se corrigent pas de la même façon.

## 10. Pistes pour réutiliser et améliorer le projet

- **Personnaliser un dessin :** transformer la taille, les couleurs et les
  positions en paramètres ou options de ligne de commande.
- **Créer un autre motif :** remplacer les formules des feuilles, pétales et
  graines tout en gardant la conversion de coordonnées et l’export GIF.
- **Ajouter une progression configurable :** offrir un mode rapide qui
  enregistre moins d’images, ou un mode détaillé qui enregistre chaque étape.
- **Ajouter un cache versionné :** recalculer la sauvegarde si les paramètres
  changent, au lieu de se fier uniquement à l’existence du fichier.
- **Séparer le projet en modules :** placer le dessin, la lecture de
  l’animation et les arguments de commande dans des fichiers distincts si le
  programme devient plus grand.
- **Partager le projet :** documenter la commande d’installation de Pillow et
  les commandes de lancement dans un fichier `README.md`.
