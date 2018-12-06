# Référentiels d'enseignement

Le dossier `referentiels` comporte :
 - des fichiers `.xml` : comportent tous les contenus des référentiels "officiels"
 - des fichiers `.xls` : ce sont les sources des fichiers .xml. Il permettent de modifier ou créer ses propres référentiels.
 - des fichiers `.html` : ce sont les _templates_ pour les fiches de validation de projet (pour certains enseignements seulement)
 - des fichiers "image" : logos, cases à cocher pour templates, ....
 
## Création d'un nouveau référentiel d'enseignement
Il est possible de créer un nouveau référentiel d'enseignement, utilisable dans les **Séquences**, les **Progressions** et les **Projets**.




Voici un petit résumé de la procédure à suivre, les indications plus précises étant disséminés sous forme de _commentaires_ dans les fichiers `.xls`.
1. Repérer parmi les référentiels existant celui qui ce rapproche le plus de celui que vous souhaitez créer.
2. Faire une copie du fichier `.xls` de ce référentiel et lui donner un nom simple mais explicite (pas d'espace - pas d'accents !).
3. 

La procédure est relativement longue, complexe, et **"sans filet"** : **_pySéquence_** ne démarrera plus si le fichier n'est pas conforme ! (mais il suffit de le supprimer pour revenir à la normale).

Conseils :
 * Procéder par **petites étapes**, pour bien comprendre le lien entre le contenu du fichier, et surtout pour comprendre et corriger ce qui fait planter **_pySéquence_** au démarrage.
 * Supprimer le fichier `.xml` à chaque modification du fichier `.xls` correspondant.

**En cas de réussite, merci d'en faire profiter à la communauté d'utilisateur** : utiliser la rubrique [Issues](https://github.com/cedrick-f/pySequence/issues) pour communiquer.
