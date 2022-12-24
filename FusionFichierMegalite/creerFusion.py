from os import walk
import numpy as np
import pandas as pd
import os

path = "/mnt/c/Users/imane/Downloads/MEGALITE_FRANCAIS_bi"


def suppHeaderBigramm():
    print("Suppression du BIGRAM du debut ...")
    os.system("sed '/BIGRAMAS/d' lastFusion1/fusionBigramme.bi > lastFusion1/fusionBigramme_without_b.txt")


def split2():
    os.system("split -n2 lastFusion1/fusionBigramme_without_b.txt")
    os.system("mv xaa fil1.txt")
    os.system("mv xaa fil2.txt")
    os.system("cp fil1.txt lastFusion1/")
    os.system("cp fil2.txt lastFusion1/")

def fusionBigram(): 
    print("Lancement fusion fichier ...")
    os.system("cat "+path+"/MEGALITE_FRANCAIS_bi/*/*.bi > lastFusion1/fusionBigramme.txt")


def ouvrirFichier():
    # liste_mots = pd.read_table('lastFusion1/fusionBigramme_without_b.txt' , names= ['mots', 'occurence'] , delimiter = '\t', dtype={'mots': str, 'occurence': int}, header=None, index_col=None, encoding='utf8', skip_blank_lines=True)
    liste_mots_part1 = pd.read_table('lastFusion1/fil1.txt', names= ['mots', 'occurence'],  dtype={'mots': str, 'occurence': int}, delimiter = '\t', header=None, index_col=None, encoding='utf8'  )
    liste_mots_part2 = pd.read_table('lastFusion1/file2.txt', names= ['mots', 'occurence'],  dtype={'mots': str, 'occurence': int},  delimiter = '\t', header=None, index_col=None, encoding='utf8'  )
    return liste_mots_part1, liste_mots_part2

def groupBigramm(data1, data2):
    group1 = data1.groupby(["mots"], as_index=False)["occurence"].sum()
    group2 = data2.groupby(["mots"], as_index=False)["occurence"].sum()
    print(' group 1 : \n', group1)
    print(' group 2 : \n', group2)
    # print('mot :: \n', group)
    # mots = group.mots.str.split(pat=' ', expand=True)
    
    # mot1 = mots[0]
    # mot2 = mots[1]
    # fichier = pd.DataFrame(data={'mot1' :  mot1, 'mot2': mot2, 'occurence': group.occurence})
    return group1, group2

def fusionnerTwoPart():
    os.system("cat lastFusion1/fusion_1.txt > lastFusion1/fusion_part.txt")
    os.system("cat lastFusion1/fusion_2.txt >> lastFusion1/fusion_part.txt")

def fusionFinal():
    liste_mots = pd.read_table('lastFusion1/fusion_part.txt' , names=['mots','occurence'], dtype={'mots':str,'occurence':int},  sep=',', encoding='utf8' , header=1)

    return liste_mots

def fusionGroup(data):
    group  = data.groupby(["mots"], as_index=False)["occurence"].sum()
    group.sort_values(by=['occurence'])
    # print(" group -- \n", group.loc[group['mots']=="de la"].reset_index())
    
    # print('List mots \n', liste_mots)
    # print( "list group --- \n", liste_mots)
    # group  = liste_mots.groupby(["mots"])["occurence"].sum()
    # print(" GROUP -------------- ", group)
    mots = group.mots.str.split(' ', expand=True)
    mot1 = mots[0]
    mot2 = mots[1]
    fichier = pd.DataFrame(data={'mot1' :  mot1, 'mot2': mot2, 'occurence': group.occurence})
    return fichier 


# print('ouverture file... ')
# data1, data2 = ouvrirFichier()
# print( "data 1 \n", data1)
# print( "data 2 \n", data2)
# print(" fusion file.." )
# group1,group2 = groupBigramm(data1,data2)
# group1.to_csv('lastFusion1/fusion_1.txt', index=False)
# group2.to_csv('lastFusion1/fusion_2.txt', index=False)

# print("lancement fusion file ... ")
# # fusionnerTwoPart()
# fusion = fusionFinal()
# print("sauvegarde ... ")
# fichier_total = fusionGroup(fusion)
# fichier_total.to_csv('lastFusion1/fusion_final.txt', index=False)

# # fusionBigram()



####################################################################################################
                            # FUSION FICHIER 
####################################################################################################


# on fusionne
fusionBigram() 

# on enleve les en-tête /BIGRAMS/
suppHeaderBigramm()

# on split en 2 
split2()

# on lit nos deux fichiers 
data1, data2 = ouvrirFichier()

# on enleve les doublons 
group1,group2 = groupBigramm(data1,data2)

# on les save 
group1.to_csv('lastFusion1/fusion_1.txt', index=False)
group2.to_csv('lastFusion1/fusion_2.txt', index=False)

# on regroupe tout dans un fichier
fusionnerTwoPart()

# on lit le nouveau tableua fusionner 
fusion = fusionFinal()

# on regroupe encore en enlevant les doublons 
fichier_total = fusionGroup(fusion)

# on sauvegarde le fichier final 
fichier_total.to_csv('lastFusion1/fusion_final.txt', index=False)