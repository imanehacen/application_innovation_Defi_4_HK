import os
import pandas as pd

#variable globale qui va être utilisé dans une fonction, pour assurer la présence d'un verbe dans une phrase
containsVerb = 0

#Fonction qui va utiliser freeling pour analyser une phrase qu'on passe en parametre, et va stocker dans un fichier le resultat
def analyze(phrase):
    cmd = 'echo ' + str(phrase) + '> sentence.txt'
    os.system(cmd)
    cmdAnalyse = 'analyze -f fr.cfg < sentence.txt > result.mrf'
    os.system(cmdAnalyse)


#Fonction qui permet de lire un fichier et de retourner un dataFrame
def readFile(filepath):
    data = pd.read_csv(str(filepath), encoding='utf-8')
    # data = pd.read_table(str(filepath), encoding="utf8")

    return data


#Fonction qui genere le mot suivant à l'aide d'un mot precedent
def generateNextWord(word, data, sentence):

    anti_dictionnaire = ["tête", "ne", "se", "vous", "nous", "porte", "que", "plus", "de", "des", "pas"]
    pp_word = ["il", "elle", "ils", "je", "tu", "elles", "nous", "vous"]
    global containsVerb

    df1=data[data["mot1"] == word]
    df1.sort_values(by=['occurence'], inplace=True, ascending=False)
    df1.drop(df1[(df1['mot1']=="de") &  (df1['mot2']=="la")].index, inplace = True)

    print(df1)
    index = 0
    next_word=""
    if(len(df1)>index):
        next_word = df1.iat[index, 1]
        while(next_word in sentence):
            index = index + 1
            next_word = df1.iat[index, 1]
    else:
        return "."     
    
    if(containsVerb==1):
        os.system("echo '"+word+" "+next_word+"' > verifContainsVerbs.txt")
        cmdAnalyse = 'analyze -f fr.cfg < verifContainsVerbs.txt > verifContainsVerbs.mrf'
        os.system(cmdAnalyse)
        indexF = 0
        codeMot = ""
        with open("verifContainsVerbs.mrf",'r') as data_file:
            for line in data_file:
                data = line.split()
                if(indexF == 1):
                    codeMot = data[2][0]
                indexF = indexF + 1

            while((codeMot!="V") or (next_word in sentence) or (next_word in anti_dictionnaire)):
                next_word=""
                if(len(df1)>index):
                    next_word = df1.iat[index, 1]

                    os.system("echo '"+word+" "+next_word+"' > verifContainsVerbs.txt")
                    cmdAnalyse = 'analyze -f fr.cfg < verifContainsVerbs.txt > verifContainsVerbs.mrf'
                    os.system(cmdAnalyse)
                    indexV = 0
                    codeMot = ""
                    with open("verifContainsVerbs.mrf",'r') as data_file:
                        for line in data_file:
                            data = line.split()
                            if(indexV == 1):
                                codeMot = data[2][0]
                            indexV = indexV + 1
                    index = index + 1
                else:
                    return "."
            containsVerb=2
    elif(containsVerb==2):
        codeMot = ""
        while((next_word in sentence) or (next_word in anti_dictionnaire)):
            next_word=""
            if(len(df1)>index):
                next_word = df1.iat[index, 1]
                index = index + 1
            else:
                return "."

    elif(containsVerb==0):


        while((next_word in sentence) or (next_word in anti_dictionnaire)):
            next_word=""
            if(len(df1)>index):
                next_word = df1.iat[index, 1]

                index = index + 1
            else:
                return "."


        os.system("echo '"+word+" "+next_word+"' > verifContainsVerbs.txt")
        cmdAnalyse = 'analyze -f fr.cfg < verifContainsVerbs.txt > verifContainsVerbs.mrf'
        os.system(cmdAnalyse)
        indexAnalyze = 0
        codeMot = ""
        with open("verifContainsVerbs.mrf",'r') as data_file:
            for line in data_file:
                data = line.split()
                if((len(data)>0) and (indexAnalyze == 1)):
                    codeMot = data[2][0]+data[2][1]
                indexAnalyze = indexAnalyze + 1
            if(codeMot=="NC" or (word in pp_word)):
                containsVerb = 1



    return next_word

                
#Fonction qui genre une phrase
def generateSentence(start, sizeSentence, fusionFile):
    sentence = start
    while(sizeSentence > 0):
        splitSentence = sentence.split()
        if(len(splitSentence) >= 0):
            mot_suivant = str(generateNextWord( str(splitSentence[len(splitSentence) - 1]), fusionFile, splitSentence))
            if(mot_suivant != "."):
                sentence = sentence + " "+ mot_suivant
            else: 
                return sentence+mot_suivant

        else : 
             mot_suivant = generateNextWord( str(splitSentence[0]), fusionFile, splitSentence)
             sentence = sentence + " "+mot_suivant

        sizeSentence = sizeSentence - 1
        print(sentence)
    

    sentence_test = sentence.split()
    last_word = sentence_test[len(sentence_test)-1]
    return sentence
            


#Fonction qui va permettre de modifier une phrase qui a été génerer, pour éviter certaines fautes et avoir une phrase assez correcte.
def modifySentence(phrase, filepath, fusionFile):
    index = 0
    data = {}
    new_sentence=""
    infoSentence = []
    with open(str(filepath),'r') as data_file:
        for line in data_file:
            data = line.split()
            if(len(data)==4):
                infoSentence.append(data[2])
            elif(len(data)>0):
                infoSentence.append(data[0])
        
        lastWord = infoSentence[len(infoSentence)-1][0]+infoSentence[len(infoSentence)-1][1]
        os.system("echo '"+phrase+"' > result.txt")
        splitSentence = phrase.split()
        while(splitSentence[len(splitSentence)-1]=="qu" or lastWord=="DA" or lastWord=="VS" or lastWord=="DD" or lastWord=="RN" or lastWord=="CC" or lastWord=="PP" or lastWord=="RG" or lastWord=="CS" or lastWord=="DI" or lastWord=="DP" or lastWord=="SP"):
            phrase = phrase + " "+ generateNextWord( str(splitSentence[len(splitSentence) - 1]), fusionFile, splitSentence)
            os.system("echo '"+phrase+"' > result.txt")
            cmdAnalyse = 'analyze -f fr.cfg < result.txt > result.mrf'
            os.system(cmdAnalyse)
            with open(str(filepath),'r') as data_file:
                for line in data_file:
                    data = line.split()
                    if(len(data)==4):
                        infoSentence.append(data[2])
                    elif(len(data)>0):
                        infoSentence.append(data[0])
                lastWord = infoSentence[len(infoSentence)-1][0]+infoSentence[len(infoSentence)-1][1]
                splitSentence=phrase.split()
                os.system("echo '"+phrase+"' > sentence.txt")
        
    
    os.system("cat result.txt")
    cmdAnalyse = 'analyze -f fr.cfg < result.txt > result.mrf'
    os.system(cmdAnalyse)
    os.system("cat result.mrf")
    print("Phrase Finale : ", phrase)



nb_mot_phrase = 15
mot_depart = "tu"


fichier_fusion = readFile("fusion_final.txt")
phrase = generateSentence(mot_depart, nb_mot_phrase, fichier_fusion)
analyze(phrase)
modifySentence(phrase, "result.mrf", fichier_fusion)
