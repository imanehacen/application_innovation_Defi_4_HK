from os import walk
import numpy as np
import pandas as pd 
from scipy.spatial import distance

from numpy import (array, dot, arccos, clip)
from numpy.linalg import norm
import os


def lirePhrase():
    # lire phrase
    sentence  = open("/mnt/c/Users/imane/OneDrive/Bureau/appInn/GenerateurPhrase/genererPhraseEtape2/sentence.txt", "r")
    
    # lire le fichier sentence
    sentence = sentence.read()
    lines = sentence.split('\n')
    return lines[0].lower()


#####################################################################################################################

def getVector():

    # ouvrire le flux avec le fichier embedding 
    #embedding  = open("/mnt/c/Users/imane/OneDrive/Bureau/appInn/GenerateurPhrase/genererPhraseEtape2/test.txt", "r")
    embedding  = open("/mnt/c/Users/imane/OneDrive/Bureau/appInn/embeddings-Fr.txt", "r")
    
    # lire le fichier embeddings
    embedding = embedding.read()
    
    # split par saut de ligne pour récuperer les mots et leurs coordonnées 
    lines = embedding.split('\n')

    #  creatin d'un tableau pour recupere un tableau avec 
    # col[0] pour le mot 
    # col[1] pour les coords
    col=[]
    for i in range (0,len(lines)-1):
        col.append(str(lines[i]).split('\t'))
    # print(col)

    #  va contenir la liste des mots 
    mot = []
    #  va contenir la liste des coord pour chaque mots
    coord = []


    #  remplir les différents tableaux 
    for i in range ( 0, len(col)-1):
        mot.append(col[i][0])
        coord.append(col[i][1])

    # print(mot[0])
    # print(np.array(coord[0]))
    # print(np.array(coord[1]))


    # pour passé d'une tableau de string à float 
    coordF=[]
    for i in range ( len(coord)):
        coordi=[]
        # enlever le debut de tableau [
        coord[i]= coord[i].replace('[', '')
        # enlever la fin de tableau ]
        coord[i]=coord[i].replace(']', '')
        # pour retirer les espaces inutiles séparant les coord par des virgules 
        coord[i]=coord[i].replace(' ', ',')
        # pour split par virgules, et recup chaque coord 
        coordij=coord[i].split(',')
        #  pour parser le tableau coordij
        for j in coordij:
            # pour ne pas prendre les cases vides 
            if ( j!=''):
                # convertir les string en float 
                coordi.append(float(j))
        #  on l'ajoute a notre tab général 
        coordF.append(coordi)
       
    # print("---------------------------------------- \n", coordF[0])


    # on redonne coord 
    coord = coordF

    # on donne la base des datas pour le dataframe
    dt = {
    "mot":mot,
    "coord" : coord
    }
    #  on crée le dataframe 
    data = pd.DataFrame(dt)

    return data


#####################################################################################################################

def calculAngle(coord):
    # 
    # TEST CALCUL ANGLES 
    #  
    angle = getAngle(coord['coord'][0],coord['coord'][0]) # doit être maximiser 
    print('angle : ', angle)


#####################################################################################################################

def recuperationCoordMot(data, word):
    return data['coord'].where(data['mot']==word)[0]



#####################################################################################################################

def recupererCodeMot(phrase):
    os.system("echo '"+phrase+"' > phrase.txt")
    os.system("analyze -f fr.cfg < phrase.txt > phrase.mrf")

    freeling = open("phrase.mrf", "r")

    codes = freeling.read()
    codesLines = codes.split('\n')
    print(codesLines)
    codesCols=[]
    for i in range (len(codesLines)):
        codesCols.append(codesLines[i].split(' '))

    code = []
    words = []
    for  i in range (len(codesCols)):
        if(codesCols[i][0]!=''):
            print(codesCols[i])
            words.append(codesCols[i][0])
            code.append(codesCols[i][2])

    # print(code)
    # print(words)
    
    # on donne la base des datas pour le dataframe
    dt = {
    "code":code,
    "mots" : words
    }
    #  on crée le dataframe 
    data = pd.DataFrame(dt)
    # print(data)
    return data


#####################################################################################################################

# 
# issu de : https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python
# 
def getAngle(u,v):
    # u = array(u)
    # v =  array(v)
    # c = dot(u,v)/norm(u)/norm(v) # -> cosine of the angle
    sum_sq = np.sum(np.square(np.array(u) - np.array(v)))
    return np.sqrt(sum_sq)
    # angle = arccos(clip(c, -1, 1)) # if you really want the angle


#####################################################################################################################

def lireAntidictionnaire():

    donnee = pd.read_csv("/mnt/c/Users/imane/OneDrive/Bureau/appInn/antidictionnaire.txt",  header=None, index_col=False)
    datas = donnee[~donnee[0].str.contains("#", na=False)]
     # on donne la base des datas pour le dataframe
   
    dt = {
    "mot":[],
    }
    #  on crée le dataframe 
    data = pd.DataFrame(dt)
    data['mot']=datas
    return data


#####################################################################################################################

def givePhraseWithoutAntidic(phrase, anti):
    mot_phrase = phrase.split(' ')
    sentense=[]
    mot_supp=[]
    for i in range (len(mot_phrase)):
        if( len(anti[anti['mot']==mot_phrase[i]].values) == 0):
            sentense.append(mot_phrase[i])

        else:
            mot_supp.append(mot_phrase[i])
    
    print(" mot à remplacer : ", sentense)
    print("mot à ne pas prendre en compte: ", mot_supp)
    
    return sentense, mot_supp


#####################################################################################################################

def recupListMot():
    # ouvrir le flux avec la table associative 
    associative  = open("/mnt/c/Users/imane/OneDrive/Bureau/appInn/TableAssociative", "r")

    # lire le fichier embeddings
    associative = associative.read()

    # split par saut de ligne pour récuperer les codes et leurs mots 
    lines = associative.split('\n')

    associative = pd.read_csv("/mnt/c/Users/imane/OneDrive/Bureau/appInn/TableAssociative", header=None)
    # print(associative)

    assoc = associative[0]


    #  creation d'un tableau pour recupere un tableau avec 
    # col[0] pour le codes 
    # col[1] pour les mots
    col=[]
    for i in range (0,len(lines)-1):
        col.append(str(lines[i]).split('\t'))
    # print(" cole , " , col[len(col)-1])

    #  va contenir la liste des codes des mots  
    code = []
    # #  va contenir la liste des mots pour chaque codes
    mots = []


    #  remplir les différents tableaux 
    for i in range ( 0, len(col)-1):
        code.append(col[i][0])
        mots.append(col[i][1:])
  

    

    # on donne la base des datas pour le dataframe
    dt = {
    "code":code,
    "mots" : mots
    }
    # #  on crée le dataframe 
    data = pd.DataFrame(dt)

    # print(data)
    # print(data.loc[data['code'] == 'NCMN000'])


    return data
     







#####################################################################################################################

def getVectorByContext(context):
    word=  data_embedding.loc[data_embedding['mot']==context].reset_index()
    print("word conntext \n ", word)
    return word['coord']

#####################################################################################################################


def recupListMotByCode(code, data):
    return data.loc[data['code'] == code]


#####################################################################################################################

def getListMotCode(code_mot, mot_a_remplacer, data_embeding, code_associative, context, context_word, phrase):

    print("=== ",mot_a_remplacer )
    mot=[]
    code=[]
    for i in range (len(mot_a_remplacer)):
        print(" - ", mot_a_remplacer[i] )
        if( mot_a_remplacer[i][len(mot_a_remplacer[i])-1]== "," or  mot_a_remplacer[i][len(mot_a_remplacer[i])-1]== "." ):
            mot_a_remplacer[i]= mot_a_remplacer[i][:-1]
        mot.append(code_mot[code_mot['mots']==mot_a_remplacer[i]]['mots'].values[0])
        code.append(code_mot[code_mot['mots']==mot_a_remplacer[i]]['code'].values[0])
        # print(code_mot[code_mot['mots']==mot_a_remplacer[i]])

    print(code)
    print(mot)

    list_mot_code =  pd.DataFrame([], columns=['code','mots'])
    for i in range (0, len(mot_a_remplacer)):
        index = mot.index(mot_a_remplacer[i])
        df = recupListMotByCode(code[index], code_associative)
        list_mot_code = pd.concat([list_mot_code,df], ignore_index=True)

    list_mot_code = list_mot_code.reset_index()
    print('list code mot :: \n', list_mot_code)

    # mettre la col mots de list_mot_code sous forme de tableau 

    mots =[]
    for i in range(0, len(list_mot_code)):

        mots_aux = str(list_mot_code['mots'][i])
        
        mots_aux= mots_aux.replace('[', '')
        mots_aux= mots_aux.replace(']', '')
        mots_aux= mots_aux.replace(' ', '')
        mots_aux= mots_aux.replace("'", '')
        mots_aux= mots_aux.replace('"', '')
        mots_aux = mots_aux.split(',')
        # print( "mots auc ", list_mot_code['mots'][i], " \n ", mots_aux)
        mots.append(mots_aux)

        
    
    # print("tab mot \n " , mots)


    print(" mot a remplacer ", mot_a_remplacer)
    
    word_max =[]
    for j in range(0, len(mot_a_remplacer)):
        print( " mot a remplacer - ", mot_a_remplacer[j])
        dist_max = 100000
        mot_replace =""

        for wo in mots[j]:
            # print( data_embedding)
            # print("mot ;;  --- > ", wo)
            
            word = data_embedding.loc[data_embedding['mot']==wo].reset_index()
            # print("word : ", word)
            if((word.empty==False) and (wo!=context_word) and (wo not in word_max)):
                #    print( " coord context ::: \n ",context[0])
                # print( " coord word ::: \n ", word['coord'])
                dist = getAngle(np.squeeze(context), np.squeeze(word['coord'][0]))
                
                if (dist_max > dist):
                    dist_max = dist
                    mot_replace =wo
                    print(' mot ', wo, " dist : ", dist )
                
        print(" " , mot_a_remplacer[j], " -> ", mot_replace)
        word_max.append(mot_replace)
        
    print(word_max)
    new_phrase = phrase.split(' ')
    for i in range(0,len(mot_a_remplacer)):
        if( mot_a_remplacer[i][len(mot_a_remplacer[i])-1]== "," or  mot_a_remplacer[i][len(mot_a_remplacer[i])-1]== "." ):
            mot_a_remplacer[i]= mot_a_remplacer[i][:-1]
        inde = new_phrase.index(mot_a_remplacer[i])
        print("inde : ", inde)
        print("i : ", i)
        print("word phra ", word_max)
        print(" phra ", new_phrase)
        new_phrase[inde]=word_max[i]

    new_phrases = ''.join(new_phrase)
    return new_phrase
        

    # list_mot_code = recupListMotByCode(' ')

    # recuperer les mots de ce code ci 


####################################################################################################################
# CORRECTION GRAMMAIRE 
#####################################################################################################################

def correctionGrammaire(phrase):
    dict = [ "le", "la", "de", "je", "me", "te", "se", "ce", "ne", "que", "qu"]
    phraseWord = phrase.split(' ')
    print(phraseWord)
    nvll=[]
    for i in range (0, len(phraseWord)):
        # print( " word i ", phraseWord[i])
        if( (i+1) < len(phraseWord)-1):
            print(" first ", phraseWord[i+1][0])
            print(" last ", phraseWord[i][len(phraseWord[i])-1])
            if ( phraseWord[i+1][0] == phraseWord[i][len(phraseWord[i])-1] ):
                print("premier - ",phraseWord[i][len(phraseWord[i])-1] , " --- --- - ", phraseWord[i], " --- ", phraseWord[i+1] )
                print(" - suivant ",phraseWord[i+1][0])
                if ( phraseWord[i] in dict):
                    newWord= phraseWord[i][:-1]+ "'"
                    nvll.append(newWord)
            else:
                nvll.append(phraseWord[i])
        else:
            nvll.append(phraseWord[i])
    ligne = miseEnPhrase(nvll)
    return ligne 

        




#####################################################################################################################

def miseEnPhrase(phra):
    s=''
    for i in range(0, len(phra)):
         s=s+phra[i]+" "
    s = s+ "."
    s = s.capitalize()
    return s


#####################################################################################################################

#####################################################################################################################

#####################################################################################################################

    
# process
# je cherche le mot contexte dans le fichier embedding 
# je lis alos la phrase source avec freeling 
# je lis la table associative, à la même ligne que le coed gramatical auquel appartient 
# le mot que je dois remplacer.
# je calcul la distance entre chacun des mots contenus sur la ligne du code grammatical 
    
# je parcours la liste des mots dont le code est le même que celui à remplacer 
# pour chacun de ces mots, je recupere dans l'embedding sa position, pour calculer l'angle 




# correctionGrammaire ("je Regrette par la allégresse et elle jubiler demain")


print(' recuperation antidictionnaire ....')
# je recupere les mots de l'antidictionnaire
antidictionnaire = lireAntidictionnaire()

phrase = lirePhrase()
print(" phrase : ", phrase)
# ['Regrette', 'allégresse', 'jubiler']
#  mot à remplacer :  ['vais', 'porte', 'voir']
# nouvelle phrase : je Regrette par la allégresse et elle jubiler demain

print('recuperation mots à remplacer .... ')
# je recupere les mots que je vais devoir remplacer, et ceux que je vais ne pas prendre en compte
mot_a_remplacer,mot_de_phrase = givePhraseWithoutAntidic(phrase, antidictionnaire)


print(" recuperation des codes des mots à remplacer ...")
# je recupere les codes des mots de la phrases 
code_mot = recupererCodeMot(phrase)


print('recuperation du tableau des embeddings ....')
# recuperer les vecteurs embedding 
data_embedding  = getVector()



print("recuperation des codes des mots , et des listes des mots grâce au tab associative ...")
# recuperer le tableau associative: code -> liste de mots 
code_mots_associative = recupListMot()

# print(getAngle(data_embedding['coord'][0],data_embedding['coord'][0]))
# sum_sq = np.sum(np.square(np.array(data_embedding['coord'][0]) - np.array(data_embedding['coord'][0])))
# print(" -?  --", np.sqrt(sum_sq))

print(" recuperation des coordonnées du context ... ")
context_word ='joie'
# recuperer les coords du context 
coordContext = getVectorByContext(context_word)

print("recuperation des nouveaux mots ... ")
# recuperer les mots associé au code du mot 
phr = getListMotCode(code_mot, mot_a_remplacer, data_embedding, code_mots_associative, coordContext, context_word, phrase)

print( " phrase de debut ;;;; \n", phrase)

newPhrase = miseEnPhrase(phr)
print(" new phrase avant correction ", newPhrase)
phraseGram = correctionGrammaire(newPhrase)
print( " phrase TRANSFORMER  ;;;; \n",phraseGram)




# data = getVectorContext()
# calculAngle(data)   
# coord_moot = recuperationCoordMot(data, 'de')

