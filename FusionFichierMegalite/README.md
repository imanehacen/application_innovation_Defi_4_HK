Ce fichier contient l'ensemble des méthodes permettant de faire fusionner l'ensemble des fichiers contenus dans le megalite.
On trouve alors les méthodes suivantes:
- " fusionBigramm() " : Cette méthode permet de fusionner l'ensemble des fichiers du megalite, mais les doublons et potentiel erreurs
ne sont pas corrigés.
- la méthode "SuppHeaderBigramm()" : permet de supprimer toutes les occurences du terme "BIGRAMAS" contenu en debut chaque fichiers
du megalite.
- la méthode "Split2()" fermet de diviser en deux le fichier generer par la méthode "fusionBigramm()" , car ce fichier est trop
 volumineux. On se retrouve alors avec deux fichiers : file1.txt et file2.txt
- la méthode "ouvrirfichier()"lit les deux fichiers file1.txt et file2.txt puis retourne deux dataframe avec le contenu des
 respectif de chacun des fichiers.
- la méthode "groupBigramm()" regroupe les doublons de bigrammes, et additionne leurs occurences.
- la méthode "fusionnerTwoPart()" va fusionner le résultat du regroupement des bigramms et de leurs occurences. 
- la méthode "fusionFinale()" lit et renvoie un dataframe contenant les deux fichiers fusionnés .
_ la méthode "fusionGroup()" reitère l'operation précedente, c-à-d ,rassemble les doublons de bigrammes, et additionne leurs
occurences.
- et, la ligne 124 permet de sauvegarder le dataframe contenant le megalite fusionné et sans doublons.
