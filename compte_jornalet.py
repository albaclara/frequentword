# -*-coding:Utf-8 -*
#compte_jornalet.py
#créé le: 01/10/2017
# par Eve Séguier
# Le but de ce programme est de calculer pour chaque dialecte la frequence des mots du corpus occitan jornalet 
# composé d'articles stockés dans le répertoire articles_segmentes
import re
import csv
import os
import html

from Biblio.fct_divers import *
from Biblio.fct_segmentation import *
mots = {}
nboccurences = 0

# calcul de la fréquence de chaque mot
for article in os.listdir('articles_segmentes/jornalet/LA/'):
	
    with open('articles_segmentes/jornalet/LA/'+article, newline='', encoding='utf-8') as fichier:
        
        for line in fichier:
            nboccurences +=1;
            line = line.rstrip()
            if line in mots.keys()  :
                    mots[line] +=1
            else :
                mots[line]=1	
					
        fichier.close()
		
# écriture du résultat dans le fichier csv
frequence =  open("frequence.csv", "w", encoding='utf-8')

for key,value in mots.items() :
    frequence.write(key+","+str(value)+"\n")
print(nboccurences)