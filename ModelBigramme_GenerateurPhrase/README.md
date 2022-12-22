Dans le fichier genererPhrase_ModelBigramme.py nous avons 5 fonctions qui sont les suivantes :
-analyze() => Permet d'analyser une phrase en donnant l'information de chaque mot de cette dernière, à l'aide de Freeling
-readFile() => Permet de lire un fichier .txt ou .csv avec la librairie panda et de retourner un DataFrame des données du fichier.
-generateNextWord() => Permet de retourner un mot suivant à l'aide d'un mot précédent, en utilisant la méthode bigramme
-generateSentence() => Permet de retourner une phrase générée.
-modifySentence() => Permet de modifier une phrase en enlevant certaines erreurs de grammaires et syntaxes.

Pour lancer l'execution de ce fichier python, il executant la commande suivant => "python3 genererPhrase_ModelBigramme.py".

Dans ce fichier python, nous pouvons donner un mot de départ pour construire la phrase et le nombre de mot que cette dernière contiendra.
Pour donner un mot de départ il faut modifier la variable "mot_depart".
Pour spécifier combien de mots vont être utilisé pour construire la phrase il faut modifier la variable "nb_mot_phrase".
