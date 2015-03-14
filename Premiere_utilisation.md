# Première utilisation #

## Choix du type de document à créer ##
Il est possible de créer :
  * des **fiches de validation projet** (Cf. [Elaboration d'une fiche de projet](Elaboration_projet.md)).
  * des fiches de **séquence** (Cf. [Elaboration d'une fiche de séquence](Elaboration_sequence.md))

**Pour choisir le type de document :**
  * menu : _Fichier/nouveau_
ou
  * bouton : ![http://pysequence.googlecode.com/svn/trunk/images_aide/Bouton_nouveau.png](http://pysequence.googlecode.com/svn/trunk/images_aide/Bouton_nouveau.png)

http://pysequence.googlecode.com/svn/trunk/images_aide/nouveau_fichier.PNG

Ce qui suit est valable dans les deux cas...

_[Haut de page](Premiere_utilisation.md)_

---

## Configuration de la classe ##

Avant de démarrer la création d'un document, il est préférable de **configurer** correctement la **[classe](Classe.md)** :
  * **type d'enseignement** (STI2D ETT ou spécialité, SSI)
> > ![http://pysequence.googlecode.com/svn/trunk/images_aide/type_d_enseignement.png](http://pysequence.googlecode.com/svn/trunk/images_aide/type_d_enseignement.png)
  * nom de l'**établissement** (lycée, collège, ...)
  * **découpage de la classe** en groupes
  * **centres d'intérêt** choisis pour l'ETT (impossible à partir de la version 5 : voir [classe](Classe.md))

Remarque : par défaut, les **centres d'intérêt** sont définis pour l'académie de **Clermont-Ferrand**, mais il est possible de les modifier à partir d'une sélection d'un fichier _Excel_, ou bien manuellement. (voir [Modifier un programme d'enseignement](Modifier_programme.md))


_[Haut de page](Premiere_utilisation.md)_

---

## Paramètres de classe préférés ##
Il est possible de conserver pour les futures fiches de séquence certains paramètres de classe :
  * l'**effectif** et le **découpage** en groupes
  * l'établissement
  * les **centres d'intérêt** choisis pour l'ETT (impossible à partir de la version 5 : voir [classe](Classe.md))

Une fois les paramètres choisis (voir [Modification des Centres d'Intérêt](ModificationCI.md)), cliquer sur le bouton ![http://pysequence.googlecode.com/svn/trunk/images_aide/Bouton_valid_pref.png](http://pysequence.googlecode.com/svn/trunk/images_aide/Bouton_valid_pref.png). : les paramètres sont alors sauvegardés dans un fichier nommé _sequence.cfg_. Il seront automatiquement utilisés lors de la création des futures fiches. Toutefois, les fichiers .seq créés avec d'autres paramètres les conserveront.

Pour rétablir les paramètres de classe par défaut, cliquer sur le bouton ![http://pysequence.googlecode.com/svn/trunk/images_aide/Bouton_defaut_pref.png](http://pysequence.googlecode.com/svn/trunk/images_aide/Bouton_defaut_pref.png)


_[Haut de page](Premiere_utilisation.md)_

---

## Inscription de pySequence ##
En cas d'utilisation de la version **portable** de _**pySequence**_, et afin que votre PC reconnaisse le type de fichier **.seq** ou **.prj**, il est nécessaire d'enregistrer le logiciel dans la _base de registre_ de Windows.

  * Lancer _**pySequence**_ (il faut pour cela avoir les **droits d'Administrateur**, et sous Windows **Vista** ou ultérieur, exécuter _**pySequence**_ **"en tant qu'administrateur"**)
  * Depuis le menu, faire _Outils/Inscrire dans la base de registre_.

![http://pysequence.googlecode.com/svn/trunk/images_aide/registre.png](http://pysequence.googlecode.com/svn/trunk/images_aide/registre.png)


---

_[Sommaire de l'aide](Aide.md)_

> _[Tutoriels de pySequence](Tutoriels.md)_