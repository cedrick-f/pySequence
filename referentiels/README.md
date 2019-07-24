# Référentiels d'enseignement

Le dossier `referentiels` comporte :
 - des fichiers `.xml` : comportent tous les contenus des référentiels "officiels"
 - des fichiers `.xls` : ce sont les sources des fichiers .xml. Il permettent de modifier ou créer ses propres référentiels.
 - des fichiers `.html` : ce sont les _templates_ pour les fiches de validation de projet (pour certains enseignements seulement)
 - des fichiers "image" : logos, cases à cocher pour templates, ....
 
## Création d'un nouveau référentiel d'enseignement
Il est possible de créer un nouveau référentiel d'enseignement, utilisable dans les **Séquences**, les **Progressions** et les **Projets**.

Voici un petit résumé de la procédure à suivre, les indications plus précises étant disséminées sous forme de _commentaires_ dans les fichiers `.xls`.
1. Repérer parmi les référentiels existant celui qui ce rapproche le plus de celui que vous souhaitez créer.
2. Faire une copie du fichier `.xls` de ce référentiel et lui donner un nom simple mais explicite (pas d'espace - pas d'accents !).
3. Modifier le contenu de ce nouveau fichier `.xls`.
4. Relancer **_pySéquence 8_** pour voir les effets

La procédure est relativement longue, complexe, et **"sans filet"** : **_pySéquence 8_** ne démarrera plus si le fichier n'est pas conforme ! (mais il suffit de le supprimer pour revenir à la normale).

## Conseils
 * Procéder par **petites étapes**, pour bien comprendre le lien entre le contenu du fichier, et surtout pour comprendre et corriger ce qui fait planter **_pySéquence 8_** au démarrage.
 * Supprimer le fichier `.xml` à chaque modification du fichier `.xls` correspondant.

**En cas de réussite, merci d'en faire profiter la communauté d'utilisateurs** : utiliser la rubrique [Issues](https://github.com/cedrick-f/pySequence/issues) pour communiquer.

## Les fiches de validation de projet en HTML
Les fiches de validation de projet doivent être des fichiers au format HTML. 
**_pySéquence 8_** les convertis en PDF lors de l'affichage ou l'export de ces fiches.
Les chemins (relatifs à `referentiels/`) de ces fichiers doivent être placés dans les cellules `Généralités_xxx!A19`.


Les renseignements qu'elle contiennent proviennent des données saisies dans **_pySéquence 8_**, et sont intégrées dans le document HTML sous la forme `[[code]]` :
Informations | Codes
------------ | -------------
Généralités à propos du projet | codes des feuilles `Généralités_xxx` (`TIT`, `PB`, `ORI`, `CCF`, `OBJ`, `TYP`, `DEC`, `PAR`, `PRX`, `SRC`, `SYN`, `FIC`)
Académie | `ACA`
Établissement | `ETA`
Session | `SES`
Équipe pédagogique | `EQU`
Présentation | `PRE`
Liste des élèves ou étudiants | `ELE`
Nombre d'élèves ou d'étudiants | `NBE`
Tâches  | `TCH`



