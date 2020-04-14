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



### Conseils généraux
 * Procéder par **petites étapes**, pour bien comprendre le lien entre le contenu du fichier, et surtout pour comprendre et corriger ce qui fait planter **_pySéquence 8_** au démarrage.
 * Supprimer le fichier `.xml` à chaque modification du fichier `.xls` correspondant.

**En cas de réussite, merci d'en faire profiter la communauté d'utilisateurs** : utiliser la rubrique [Issues](https://github.com/cedrick-f/pySequence/issues) pour communiquer.

### Signification des onglets (feuilles de calcul)
 * **Généralités** : nom du référentiel, répartition dans la(les) années de formation, lien vers les programmes officiels, dénomination des éventuels projets, ...
 * **CI** : liste des Centres d'intérêt / Thématiques / ... (le vocabulaire dépend du référentiel)
 * **Sav_S** : Savoirs / Connaissances / ... (le vocabulaire dépend du référentiel) de la discipline concernée par la séquence ou le projet
 * **Sav_** : Savoirs / Connaissances / ... (le vocabulaire dépend du référentiel) d'autres disciplines, et qui peuvent apparaitre dans les objectifs et/ou les prérequis
 * **Comp_S** : Compétence / Capacité / ... (le vocabulaire dépend du référentiel) de la discipline concernée par la séquence ou le projet
 * **Comp_** (_autant que nécessaire_) : Compétence / Capacité / ... (le vocabulaire dépend du référentiel) d'autres disciplines, et qui peuvent apparaitre dans les objectifs et/ou les prérequis
 * **Th** : Thèmes / Thématiques / ... (le vocabulaire dépend du référentiel) (voir exemple dans `Ref_Cycle4.xls`)
 * **Spe** : Spécialités de l'enseignement (voir exemple dans `Ref_STI2D.xls`)
 * **Dom** : Domaines (voir exemple dans `Ref_Cycle4.xls`)
 * **Séance** : beaucoup d'informations sur l'organisation des séances (Nature, Type d'activité, Effectifs, dénomonation du Matériel, Enseignements spécifiques, Niveaux taxonomiques (voir `Ref_STI2D.xls` pour un exemple assez complet)
 * **Labels** : quelques dénominations particulières au référentiel
 * **Phase_** (_une feuille par projet_): dénomination des différentes phase de chaque projet
 * **Grille_ _** (_une feuille par projet et par partie_): nom du fichier "grille d'évaluation" et cellules à renseigner
 * **Généralités_** (_une feuille par projet_) : éléments à renseigner, spécifiques au référentiel, pour définir le projet (voir [Cas des Projets](###Cas-des-Projets) )
 * **Fonctions** : Activités professionelles (voir exemple dans `Ref_STS_EE.xls`)
 * **Taches_** (_une feuille par projet_) : Tâches prédéfinies pour le projet (voir exemple dans `Ref_STS_SN.xls`)
 
 

### Cas des Projets
Les référentiels d'enseignement peuvent imposer plusieurs **Projets** (avec ou sans évaluation) : définis sur la feuille `Généralités`
Chaque projet est découpé en plusieurs **parties** (typiquement "conduite" et "soutenance"), définies sur la feuille des compétences `Comp_S`, à partir de la colonne `L`.
Pour que les projets soient correctement pris en compte, il faut qu'il y ait correspondance entre les _codes_ ou les _noms_ des projets entre ces deux feuilles :
`Généralités!B25` = `Comp_S!L2`
ou bien
`Généralités!B26` = `Comp_S!L2`

#### Généralités
_Feuilles de calcul :_ `Généralité_x`

Cette feuille comporte les caractéristiques de différents champs de saisie de propriété de chaque projet.

##### Attributs du projet
Codes | Type de saisie | Lieu de saisie | Sur la fiche
------------ | ----- | --- | -
`TIT` | Zone de texte | Onglet Propriétés générales | x
`PB` | Zone de texte | Onglet Propriétés générales | x
`ORI` | Zone de texte | Onglet spécifique | 
`CCF` | Zone de texte | Onglet spécifique | 
`OBJ` | Zone de texte | Onglet spécifique | 
`TYP` | Cases à cocher | Onglet spécifique | 
`DEC` | 2 zones de texte+nombre | Onglet spécifique | 
`PAR` | Zone de texte | Onglet commun avec `PRX` et `SRC` | 
`PRX` | Zone de texte | Onglet commun avec `PAR` et `SRC` | 
`SRC` | Zone de texte | Onglet commun avec `PRX` et `PAR` | 
`SYN` | Zone de texte | Onglet spécifique | 
`FIC` | ??? | ??? | 
`SML` | Selection de fichiers 'image' | Onglet spécifique | 


#### Grilles d'évaluation
_Feuilles de calcul :_ `Grille_x_y`


##### Fichier "grille"
 * Nom du fichier : lien vers le fichier .xls (à partir du dossier `tables`)
 * Type :
   * `I` pour _individuel_ (un classeur par élève/étudiant)
   * `C` pour _collectif_ (une feuille de calcul par élève/étudiant)

##### Cellules à renseigner
Certaines informations peuvent être automatiquement insérées dans les feuilles de calcul par **_pySéquence 8_**.

 * Code :
   * "Tit" : intitulé du Projet
   * "Des" : description complète du sujet (intitulé + problématique)
   * "Nom" : nom de l'élève/étudiant
   * "Pre" : prénom de l'élève/étudiant
   * "N-P" : nom et prénom de l'élève/étudiant
   * "Etab": nom de l'établissement
   * "Sess": session
   * "Prof" : liste des membres du jury
   * "EtabPrf" : liste des établissements des membres du jury
 * Feuille : nom de la feuille de calcul où insérer l'information
 * Ligne/Colonne : cellule où insérer l'information (à partir de 1)
 * Période : quand l'information est une liste, périodicité en nombre de lignes
 * Préfixe : texte à rajouter devant l'information


#### Les fiches de validation de projet en HTML
Les fiches de validation de projet doivent être des fichiers au format HTML. 
**_pySéquence 8_** les convertis en PDF lors de l'affichage ou l'export de ces fiches.
Les chemins (relatifs à `referentiels/`) de ces fichiers doivent être placés dans les cellules `Généralités_xxx!A19`.


Les renseignements qu'elle contiennent proviennent des données saisies dans **_pySéquence 8_**, et sont intégrées dans le document HTML sous la forme `[[code]]` :


Informations | Codes
------------ | -----
Généralités à propos du projet | codes des feuilles `Généralités_xxx` (`TIT`, `PB`, `ORI`, `CCF`, `OBJ`, `TYP`, `DEC`, `PAR`, `PRX`, `SRC`, `SYN`, `FIC`)
Académie | `ACA`
Établissement | `ETA`
Session | `SES`
Équipe pédagogique | `EQU`
Présentation | `PRE`
Liste des élèves ou étudiants | `ELE`
Nombre d'élèves ou d'étudiants | `NBE`
Tâches | `TCH`


[Syntaxe spécifique au convertisseur HTML/PDF](https://xhtml2pdf.readthedocs.io/en/latest/format_html.html#)

##### Classes intégrées
Il est possible de redéfinir les styles pour les classes suivantes
 * `typologie` (tables) : cases à cocher du champ typologie (`TYP`)
 * ...
 
 
 


