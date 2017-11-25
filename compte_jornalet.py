# -*-coding:Utf-8 -*
#compte_jornalet.py
#créé le: 25/11/2017
# par Eve Séguier
# Le but de ce programme est de calculer pour chaque dialecte la frequence des mots du corpus occitan jornalet 
# composé d'articles stockés dans le répertoire articles_segmentes

import re
import csv
import os
import html

# initialisation
mots = {}
nboccurences = 0
RepArticles = 'articles_segmentes/jornalet/'
dialecte = "LI"
FicResult = 'frequence.csv'

# calcul de la fréquence de chaque mot
for article in os.listdir(RepArticles+'/'+dialecte+'/'):
	
    with open(RepArticles+'/'+dialecte+'/'+article, newline='', encoding='utf-8') as fichier:
        
        for line in fichier:
            nboccurences +=1;
            line = line.rstrip()
            if line in mots.keys()  :
                    mots[line] +=1
            else :
                mots[line]=1	
					
        fichier.close()
		
# écriture du résultat dans le fichier csv
frequence =  open(FicResult, "w", encoding='utf-8')
frequence.write('"Nb total occurences : ",'+str(nboccurences)+"\n")
for key,value in mots.items() :
    frequence.write('"'+key+'",'+str(value)+"\n")
	