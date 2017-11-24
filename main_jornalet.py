# -*-coding:Utf-8 -*
#main_jornalet.py
#créé le: 01/10/2017
# par Eve Séguier
# Le but de ce programme est de déterminer les dialectes des articles du corpus occitan du Jornalet (https://www.jornalet.com) et d'introduire le code  de ce dialecte dans fichier xml
# les articles sont compris entre les balises  <item ...> et </item>

import re
import csv
import os
import html

from Biblio.fct_divers import *
from Biblio.fct_segmentation import *



trace = open("trace/trace_main.txt", "w", encoding='utf-8')
#fichier à traiter n 
entree = "corpus_jornalet/sindica_tots_sansdata.xml"
#fichier de sortie
sortie =  open("corpus_jornalet/sindica_tots_sansdata_avec_code_dial.xml", "w", encoding='utf-8')
#On suppose que le fichier a au moins une ligne

#Chargement profils dialectes 
profil = charge_profils()

#Chargement des exceptions du genre maldespièch del
excepcions = charge_excepcions()

# Traitement du fichier 

nbarticles = 0

with open(entree, "r", encoding='utf-8') as html_doc:
    findansarticle = 0
    L1 = html_doc.readline()
    L2 = html_doc.readline()
	
	# tant qu'il y a des lignes
    while 1:
	
        # si fin de fichier
        if L2 =='':
            sortie.write(L1)
            break

        #si pas de <item> on ecrit directement la ligne dans le fichier de sortie
        if  not re.search("<item>",L1):
            #echappement des entities du style Mus&egrave;u --> Musèu
            L1 = html.unescape(L1)
            sortie.write(L1)
            L1  = L2
            L2 = html_doc.readline()
			
        # Si balise item on met dans un tampon les lignes jusqu'à </item> 
		# pour les réinjecter dans le fichier de sortie une fois modifié
        # On stocke aussi le texte dans tampon et on l'écrit dans article.xhtml pour le segmenter et tester dialecte
        # Si on trouve une fin de fichier, on envoie le message "Document mal formé"
        else :
            nbarticles += 1
            article = open("trace/article.xhtml", "w", encoding='utf-8')
            tampon=[]
            findansarticle = 0	
            tampon.append(L1)
            article.write(L1) 		
            L1  = L2
            L2 = html_doc.readline()
			
            # rencontre de fin de fichier avant fermeture de la balise </item>
            if L2 =='':
                print ("Document mal formé")
                break
				
            # tant qu'on n'a pas rencontré la balise </item>
            # on écrit les lignes dans tampon et dans article.xhtml
            while not re.search("\/item",L2):  	
                L1 = html.unescape(L1)	
                article.write(L1) 
                tampon.append(L1)
                L1  = L2
                L2 = html_doc.readline()
                if L2 =='':
                    print ("Document mal formé")                   
                    break
 
            article.close()
			
            # Traitement de l'article
            article = open("trace/article.xhtml", "r", encoding='utf-8')  
			
            # extraction du texte (suppression des balises)
            extract_jornalet(article)
            article.close()
			
            #segmentation du texte
            tokenize("trace/article.txt",excepcions)
			
            # elaboration du profil de l'article
            result = profil_texte("trace/article_segmente.txt",4)
            nbAA = result[0]
            nbAL = result[1]	
            nbmots = result[2]	
            profngram = result[3]	
			
            # détection du dialecte de l'article
            dialecte_detecte = detect(profil,profngram,nbAL,nbAA,nbmots)
            print(dialecte_detecte)
			
            # introduction code dialecte dans fichier xml
            tampon[0] =  tampon[0].replace('<item>','<item  xml:lang="'+dialecte_detecte[0]+'" >')
			
            # sauvegarde du fichier article sans balise et du fichier article segmenté
            if os.path.isfile("articles/jornalet/"+dialecte_detecte[0]+"-article"+str(nbarticles)+".txt") : 
                os.remove("articles/jornalet/"+dialecte_detecte[0]+"-article"+str(nbarticles)+".txt")
            if os.path.isfile("articles_segmentes/jornalet/"+dialecte_detecte[0]+"-article"+str(nbarticles)+".txt") : 
                os.remove("articles_segmentes/jornalet/"+dialecte_detecte[0]+"-article"+str(nbarticles)+".txt")
            os.rename("trace/article.txt", "articles/jornalet/"+dialecte_detecte[0]+"-article"+str(nbarticles)+".txt")  
            os.rename("trace/article_segmente.txt", "articles_segmentes/jornalet/"+dialecte_detecte[0]+"-article"+str(nbarticles)+".txt")    
            trace.write("article"+str(nbarticles)+".txt , "+dialecte_detecte[0]+" , "+ dialecte_detecte[2]+" , "+str(dialecte_detecte[1])+" , "+str(dialecte_detecte[3])+"\n")		
           
# fermeture des fichiers
sortie.close()
html_doc.close()
trace.close()