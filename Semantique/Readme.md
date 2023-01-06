

le fichier contient les differentes méthodes, pour generer des phrases par homosyntaxe.
Elle fermet de donner de la sémentique à la phase génerer à précédente l'étape .
- La  méthode "lirethrase()" permet de lire la phrase generer précedement , cette
derniere étant stocker dans un fichier texte.
- La méthode "getVector()" pernet de recuperer le fichier embeddings dans un
datapframe structurée. Le dataframe est constitué de 2 colonnes: mot , et coord, qui
correspond au vecteur de coordonnés du mot.
- la méthode "CalculAngle()" et "getAngle()" permet de recuperer la distance entre deux vecteurs ( mot).
- La méthode "récuperationCoordMot()", pernet de recuperer les coordonnées d´un mot donné.
- la méthode "recupéreCodeMot()", permet de recuperer les POSTAG de chacun des mots composant la
phrase.
- la méthode "lireAntidictionnaire()" permet de lire le fichiers "Antidictionnaire.txt"
- la méthode "givePhraseWithoutAntidic()" permet d'identifier grâce à l'antidictionnaire quels mots
doivent être remplacés.
- la méthode "recupListMot()" permet de récupérer la liste de tous les mots ayant les mêmes POSTAG grâce a la table associative.
- la méthode "getVectorByContext()" permet de récupérer les coordonnées du mot contexte.
- la méthode "getListMotCode()" Fermer de récupérer les mots qui vont être remplacé dans la phrase le départ cela grâce au mot contexte qui 
aura été donné par l'utilisateur au départ fermer de récupérer les mots qui vont être remplacé dans la phrase le départ cela grâce au mot contexte qui aura 
été donnée par l'utilisateur au départ. pour ce faire nous prenons la plus courte distance entre ce mot contexte est le mot qui aurait été pris dans la boucle 
parmi les mots de la table associatif correspondant au même Postag. -
