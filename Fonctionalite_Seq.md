# Séquence pédagogique #
_**pySequence**_ permet de réaliser des fiches de description de séquence pédagogique : sur une seule page synthétique, sont représentés le déroulement des diverses activité, les objectifs, les prérequis, ...

De plus, depuis _**pySequence**_, la fiche permet l'accès directe au fichiers, dossiers, autres séquences et lien Internet en rapport avec la séquence.

[Présentation générale](Presentation.md) de la fenêtre de _**pySequence**_ en mode "Séquence"

## Principales fonctionnalités ##

  * [Une structure en arborescence](Fonctionnalites#Une%20structure%20en%20arborescence.md)

  * [Une fiche pédagogique graphique](Fonctionnalites#Une%20fiche%20p%C3A9dagogique%20graphique.md)

  * [Un seul fichier au centre des documents pédagogiques](Fonctionnalites#Un%20seul%20fichier%20au%20centre%20des%20documents%20p%C3A9dagogiques.md)

  * [Adaptable à toutes les spécialités de STI2D](Fonctionnalites#Adaptable_%C3%A0_toutes_les_sp%C3%A9cialit%C3%A9s_de_STI2D.md)





---

## Une structure en arborescence ##
_**pySequence**_ fourni une aide pour créer des séquences pédagogiques.
La séquence a une structure en _arborescence_ :
  * **[Classe](Classe.md)** (spécialité, effectifs, ...)
  * **Centre d'intérêt** abordé
  * **Prérequis** (savoirs ou autre séquence)
  * **Objectifs** (compétences ou savoirs attendus)
  * Déroulement (scénario) de la séquence
    * Enchainement de **[séances](creation_seance.md)**
    * Activités en _rotation_ ou bien en _parallèle_
      * ...
      * ...
    * ...
  * **[Systèmes](systeme_labo.md)** mis en œuvre dans la séquence.

Chaque élément de séquence possède des propriétés :
  * Séquence : intitulé, ...
  * Objectif : compétence, savoirs, ...
  * [Séances](creation_seance.md) : intitulé, type, démarche, effectif, durée, ...
  * [Systèmes](systeme_labo.md) : nom, quantité, ...

_[Haut de page](Fonctionnalites_Seq.md)_

---

## Une fiche pédagogique graphique ##
Au fur et à mesure de sa création, la séquence apparait sous forme graphique (**fiche**) dans la _fenêtre centrale_.
Cela permet de visualiser graphiquement son déroulement, ce qui offre notamment une aide pour élaborer des [séances](creation_seance.md) un peu complexes, comme des séries d'activités en rotation ou en parallèle (compatibilité des durées, des effectifs élève, ...)

Cette fiche est très simplement exportable au format pdf.

_[Haut de page](Fonctionnalites_Seq.md)_

---

## Un seul fichier au centre des documents pédagogiques ##
La séquence est [sauvegardée dans un fichier](ouverture_enregistrement.md) (extension .seq).

Grâce à des [liens](lier_fichiers.md), depuis _**pySequence**_, il est possible d'accéder à l'ensemble des documents qui la constitue : ressources pédagogique, activités, liens vers des sites Internet ...

_[Haut de page](Fonctionnalites_Seq.md)_

---

## Adaptable à toutes les spécialités de STI2D ##
Les _compétences_, _savoirs_ et _centres d'intérêts_ sont dépendants du type d'**enseignement technologique** dispensé à la classe :
  * Enseignement Technologique Transversal (ETT)
  * Enseignements de spécialité (SIN, AC, ITEC ou EE)
Il est possible de spécifier les **effectifs** de la classe et également d'adapter la liste des CI pour l'ETT à ceux choisis pour l'académie.

_[Haut de page](Fonctionnalites_Seq.md)_

---


_[Sommaire de l'aide](Aide.md)_