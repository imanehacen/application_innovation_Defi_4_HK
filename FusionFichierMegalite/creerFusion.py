from os import walk
import numpy as np
import pandas as pd
import os

path = "/mnt/c/Users/imane/Downloads/MEGALITE_FRANCAIS_bi"


def fusionner():
    print("Lancement fusion fichier ...")
    os.system("cat "+path+"/MEGALITE_FRANCAIS_bi/*/*.bi > lastFusion1/fusionBigramme.bi")

def suppCarSpecial():
    print("Suppression des caractères spécial ... ")
    os.system("cat lastFusion1/fusionBigramme.bi | tr -d '°' > lastFusion1/fusionBigramme_without_special.bi")

def suppLVide():
    print("Suppression des lignes vides ....")
    os.system(" sed -i '/^$/d' lastFusion1/fusionBigramme_without_special.bi ")

def suppHeaderBigramm():
    print("Suppression du BIGRAM du debut ...")
    os.system("sed '/BIGRAMAS/d' lastFusion1/fusionBigramme_without_special_v2.bi > lastFusion1/fusionBigramme_without_b.bi")

def suppUtf8():
    print("Suppression des caractères au format UTF-8....")
    os.system("sed 's/Œ/oe/g; s/à/a/g; s/â/a/g; s/é/e/g; s/è/e/g; s/ê/e/g; s/î/i/g; s/ç/c/g; s/ô/o/g;  s/û/u/g; s/È/E/g; s/ë/e/g; s/ï/i/g;' lastFusion1/fusionBigramme_without_b.bi > lastFusion1/fusionBigramme_without_b_v2.bi")

def suppWordLessThanThree():
    print("Suppression des lignes de moins de 3 mots ....")
    os.system("cat lastFusion1/fusionBigramme_without_b.bi | awk 'NF==3' > lastFusion1/fusion_v1.bi")


def creationCSVFile():
    print("Creation du fichier csv avec en-tête : mot1, mot2, occurence.....")
    os.system("echo 'mot1,mot2,occurence' > lastFusion1/fusion.txt")

def miseSeparatorCSV():
    print("Ajout des séparateurs ',' ....")
    os.system("sed -e 's/\s\+/,/g' lastFusion1/fusion_v1.bi > lastFusion1/fusion_v1.txt")


def fusionBigrammUnique():
    print("Procedure de fusion des bigrammes uniques ... ")
    os.system("datamash -t, -s -g 1,2 sum 3 < lastFusion1/fusion_v1.txt >> lastFusion1/fusion.txt")



# # fusionner()
# suppCarSpecial()
# suppLVide()
# suppHeaderBigramm()
# # suppUtf8()
# suppWordLessThanThree()
# creationCSVFile()
# miseSeparatorCSV()
# fusionBigrammUnique()




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

print("lancement fusion file ... ")
# fusionnerTwoPart()
fusion = fusionFinal()
print("sauvegarde ... ")
fichier_total = fusionGroup(fusion)
fichier_total.to_csv('lastFusion1/fusion_final.txt', index=False)

# fusionBigram()