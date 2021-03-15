# -*- coding: utf-8 -*-

"""
Created on Sun Feb 28 16:09:56 2021

@author: Romain
"""

import copy as cp

"""Création classe Arret"""
class Arret():
    def __init__(self, nom):
        self.nom = nom
        
    def get_nom(self):
        return self.nom

"""Création classe Arc"""    
class Arc():
    def __init__(self, debut, fin, liste_horaire = []):
        self.debut = debut
        self.fin = fin
        self.liste_horaire = liste_horaire
        
    def get_debut(self):
        return self.debut
    
    def get_fin(self):
        return self.fin
    
    def get_liste_horaire(self):
        return self.liste_horaire

"""Création classe Ligne"""
class Ligne():
    def __init__(self, liste_horaire = []):
        self.liste_arc = []
        self.liste_horaire = liste_horaire
        self.liste_arret = []
        #Création des arrets ainsi qu'ajout a la liste_arret
        liste_horaire_arret = liste_horaire.split("\n")
        for line in liste_horaire_arret:
            nom = line.split(" ")[0]
            arret = Arret(nom)
            self.liste_arret.append(arret)
        
        #Créations des arcs ainsi qu'ajout à la liste_arc
        for i in range(0, len(liste_horaire_arret)-1):
            horaires = []
            horaires1 = liste_horaire_arret[i].split(" ")
            horaires2 = liste_horaire_arret[i+1].split(" ")
        
            #Création des paires d'horaires (heure de depart, heure d'arrivé)
            for h in range(1, len(horaires2)):
                #Filtre pour ne pas ajouter les horaires contenant des "-"
                if (horaires1[h] != "-" and horaires2[h] != "-"):
                    horaires.append((horaires1[h], horaires2[h]))
            if len(horaires) != 0:
                #arc = (Arret du départ, Arret de l'arrivé, la listes des paires d'horaires)
                arc = Arc(self.liste_arret[i], self.liste_arret[i+1], horaires)
                self.liste_arc.append(arc)
            elif i < len(liste_horaire_arret)-2:
                horaires = []
                horaires1 = liste_horaire_arret[i].split(" ")
                horaires2 = liste_horaire_arret[i+2].split(" ")
        
                #Création des paires d'horaires (heure de depart, heure d'arrivé)
                for h in range(1, len(horaires2)):
                    #Filtre pour ne pas ajouter les horaires contenant des "-"
                    if (horaires1[h] != "-" and horaires2[h] != "-"):
                        horaires.append((horaires1[h], horaires2[h]))
                if len(horaires) != 0:
                    #arc = (Arret du départ, Arret de l'arrivé, la listes des paires d'horaires)
                    arc = Arc(self.liste_arret[i], self.liste_arret[i+2], horaires)
                    self.liste_arc.append(arc)
            
    
    def get_liste_arc(self):
        return self.liste_arc
    
    def get_liste_arret(self):
        return self.ligne_arret
    
    def get_liste_horaire(self):
        return self.liste_horaire
      
"""Création classe réseau"""
class Reseau():
    def __init__(self, lignes = []):
        self.liste_ligne = []
        
        #Créations de toutes les lignes du réseau ainsi qu'ajout à la liste_ligne
        for a in lignes:
            l = Ligne(a)
            self.liste_ligne.append(l)
        
    def get_liste_ligne(self):
        return self.liste_ligne
    
    def afficher_ligne(self):
        for i in range(0, len(self.liste_ligne)):
            print("ligne", i+1, ":")
            for arret in self.liste_ligne[i].liste_arret:
                print("-", arret.get_nom())
            print("\n")

    #Crée la liste de tous les arrets du réseau
    def do_list_arret(self):
        liste = []
        for ligne in self.liste_ligne:
            for arret in ligne.liste_arret:
                if contient(liste, arret)==False :
                    liste.append(arret)
        return liste
    
    #Affiche la liste de tous les arrets du reseau
    def affiche_arret(self):
        liste = self.do_list_arret()
        print("Les arrets du réseaux sont :")
        for arret in liste:
            print(arret.get_nom())

#Renvoie True si elem est dans la liste                
def contient(liste, elem):
    for i in liste:
        if i.get_nom() == elem.get_nom():
            return True
    return False

"""Gestion du trajet"""

#Renvoie la liste de tous les arcs partant de l'arret en paramètre
def arc_de_larret(debut):
    arc_dispo = []
    for ligne in reseau.liste_ligne:
        for arc in ligne.liste_arc:
            if arc.debut.nom == debut.nom:
                arc_dispo.append(arc)
    return arc_dispo

#Trouver l'arret en faisant correspondre les noms
def trouver_arret(nom):
    for ligne in reseau.liste_ligne:
        for arret in ligne.liste_arret:
            if arret.nom == nom:
                return arret
    
#Renvoie True si arret est dans la liste_vu
def deja_vu(liste_vu, arret):
    res = False
    for i in liste_vu:
        if i.nom == arret.nom:
            res = True
    return res

#Renvoie une liste de tous les arrets parcours 
def find_trajet(debut, fin,liste_arret_fait, liste_trajet_possible):
    
    for arc in arc_de_larret(debut):    #Boucle sur tous les arc partant de départ
    
        copy_list = cp.deepcopy(liste_arret_fait) #Copie la liste des arret vue
        if (len(copy_list) > 50):
            break
        if deja_vu(copy_list, arc.fin): #Verifie si l'arrive de l'arc n'a pas deja été visité
            continue
        copy_list.append(arc.fin)
        if arc.fin.get_nom() == fin.get_nom():
            liste_trajet_possible.append(copy_list)
            return copy_list, liste_trajet_possible
        else:
            find_trajet(arc.fin, fin, copy_list, liste_trajet_possible)
    return liste_trajet_possible

#Renvoie le trajet le plus court(en nombre d'arc)
def shortest(liste_trajet):
    min = len(liste_trajet[0])
    res = liste_trajet[0]
    for trajet in liste_trajet:
        
        if type(trajet[0]) == list:
            continue
        
        if len(trajet) <= min:
            min = len(trajet)
            res = trajet
    return res

#Convertit un horaire de la forme (hh:mm) en minutes
def convertion_horaire(horaire):
    heure, minute = horaire.split(':')
    temps = int(heure) * 60 + int(minute)
    return temps

#Renvoie un string de la forme(hh:mm) pour un temps en minute
def convertion_temps_horaire(minute):
    temps_heure = minute // 60                 #Calcul du nombre d'heure
    temps_minute = minute % 60                 #calcul du nombre de minute
    
    if (temps_heure < 10):
        temps_heure = '0'+ str(temps_heure) #affichage plus clean avec ajout de 0 si valeur chiffre unique
    else:
        temps_heure = str(temps_heure)
        
    if (temps_minute < 10):
        temps_minute = '0'+ str(temps_minute)
    else:
        temps_minute = str(temps_minute)
    
    return(temps_heure+':'+temps_minute)    #renvoie un string avec(heure, : , minute)

#Trouve les horaire du prochain passage de bus
def trouver_horaire(liste_horaire, depart):     
    time_depart = convertion_horaire(depart)
    for i in range(0, len(liste_horaire)):
        heure_passage = convertion_horaire(liste_horaire[i][0])
        if heure_passage >= time_depart:
            return liste_horaire[i]
  
#Renvoie la liste des horaires pour les deux arcs en question
def get_liste_horaire(depart, arrive):
    for arc in arc_de_larret(depart):
        if arc.fin.nom == arrive.nom:
            return arc.get_liste_horaire()

#Fonction qui calcule le temps entre deux horaire
def calcul_temps(depart,arrive):        
    time_depart = convertion_horaire(depart)
    time_arrive = convertion_horaire(arrive)
    temps = time_arrive - time_depart       #Calcul de la duree en minute only
    if temps >= 0:
        return(temps)    #renvoie un string avec(heure, : , minute)
    else:
        return 9999

#Renvoie le trajet le plus rapide       
def fastest(liste_trajet, heure):
    temps = "23:59"
    res = liste_trajet[0]
    for trajet in liste_trajet:
        
        if type(trajet[0]) == list:
            continue
        
        heure_depart = trouver_horaire(get_liste_horaire(trajet[0], trajet[1]), heure)[0]
        heure = heure_depart 
        for i in range(0,len(trajet)-1):
            horaires = get_liste_horaire(trajet[i], trajet[i+1])
            heure_depart, heure_arrive = trouver_horaire(horaires, heure_depart)
            heure_depart = heure_arrive
        if calcul_temps(heure, heure_arrive) <= convertion_horaire(temps):
            temps = convertion_temps_horaire(calcul_temps(heure, heure_arrive))
            res = trajet
    return res, temps
             
#Renvoie le trajet qui arrive le plus tot à l'arrivee     
def foremost(liste_trajet, heure):
    temps = 9999
    res = liste_trajet[0]
    for trajet in liste_trajet:
        
        if type(trajet[0]) == list:
            continue
        
        heure_depart = trouver_horaire(get_liste_horaire(trajet[0], trajet[1]), heure)[0]
        heure = heure_depart 
        for i in range(0,len(trajet)-1):
            horaires = get_liste_horaire(trajet[i], trajet[i+1])
            heure_depart, heure_arrive = trouver_horaire(horaires, heure_depart)
            heure_depart = heure_arrive
        harrive = convertion_horaire(heure_arrive)
        if harrive < temps:
            temps = harrive
            res = trajet
    temps = convertion_temps_horaire(temps)
    return res, temps   

#Renvoie True si le format d'heure est correct
def format_heure(temps):
    if len(temps.split(":")) != 2:
        return False
    heure, minute = temps.split(":")
    if ((0 <= int(heure)) and (int(heure) <= 23) and (0 <= int(minute)) and (int(minute) <= 59)):
        return True
    else:
        return False

#Affiche les noms pour une liste(d'arret)
def print_liste_arret(liste):
    for arret in liste:
        print(arret.get_nom)
    
"""Création des lignes"""
data_file_name1 = '1_Poisy-ParcDesGlaisins.txt'
data_file_name2 = '2_Piscine-Patinoire_Campus.txt'

try:
    with open(data_file_name1, 'r',encoding='utf-8') as f:
        content1 = f.read()
    with open(data_file_name2, 'r',encoding='utf-8') as f:
        content2 = f.read()
except OSError:
    # 'File not found' error message.
    print("File not found")

slited_content1 = content1.split("\n\n")
regular_path1 = slited_content1[0]
regular_date_go1 = slited_content1[1]
regular_date_back1 = slited_content1[2]
we_holidays_path1 = slited_content1[3]
we_holidays_date_go1 = slited_content1[4]
we_holidays_date_back1 = slited_content1[5]

slited_content2 = content2.split("\n\n")
regular_path2 = slited_content2[0]
regular_date_go2 = slited_content2[1]
regular_date_back2 = slited_content2[2]
we_holidays_path2 = slited_content2[3]
we_holidays_date_go2 = slited_content2[4]
we_holidays_date_back2 = slited_content2[5]



"""Création des deux réseaux"""
#Liste des horaires des lignes en fonctions de regular ou we_holidays
horaires_reguliers = [regular_date_go1, regular_date_back1, regular_date_go2, regular_date_back2]
horaires_speciaux = [we_holidays_date_go1, we_holidays_date_back1, we_holidays_date_go2, we_holidays_date_back2]

reseau_regulier = Reseau(horaires_reguliers)
reseau_special = Reseau(horaires_speciaux)

reseau = reseau_regulier



        
"""Question à l'utilisateur"""

#Choix Régulier/Week-end_Vacance
date = input("Etes vous en période régulière ou en période de vacance ou week-end?\n(\"re\"->regulier\t\"we\"->week-end ou vacance)\n")
while((date != "re") and (date != "we")):
    print("Vous avez saisis une mauvaise entré, veuillez ressaisir svp")
    date = input("Etes vous en période régulière ou en période de vacance ou week-end?\n(\"re\"->regulier\t\"we\"->week-end ou vacance)\n")

if date == "re":
    reseau = reseau_regulier
else:
    reseau = reseau_special

reseau.affiche_arret()

#Choix de l'arret de départ
debut = input("Quel est l'arret de départ?\n")
depart = trouver_arret(debut)
while (depart == False):
    print("Vous avez du mal taper le nom de l'arret ou alors il n'est pas encore pris en compte par le système.\nVeuillez recommencer svp")
    debut = input("Quel est l'arret de départ?\n")
    depart = trouver_arret(debut)

#Choix de l'arret d'arrivé
arrive = input("Quel est l'arret d'arrivé?\n")
fin = trouver_arret(arrive)
while (fin == False):
    print("Vous avez du mal taper le nom de l'arret ou alors il n'est pas encore pris en compte par le système.\nVeuillez recommencer svp")
    arrive = input("Quel est l'arret d'arrivé?\n")
    fin = trouver_arret(arrive)

#Choix de l'heure de départ
heure = input("A quelle heure voulez vous partir? (sous forme hh:mm)\n")
while (format_heure(heure) == False):
    print("Vous avez du mal taper l'heure\nVeuillez recommencer svp")
    heure = input("A quelle heure voulez vous partir? (sous forme hh:mm)\n")

trajet = find_trajet(depart, fin, [depart], [])

#Choix du mode de trajet
mode = input("Quel type de trajet voulez vous?(l'écrire sans majuscule)\n-shortest\n-fastest\n-foremost\n")
while ((mode != "shortest") and (mode != "fastest") and (mode != "foremost")):
    print("Vous avez du mal taper le mode de trajet, veuillez recommencer svp")
    mode = input("Quel type de trajet voulez vous?(l'écrire sans majuscule)\n-shortest\n-fastest\n-foremost\n")

print("\n")
if (mode == "shortest"):
    s2 = shortest(trajet)
    print("Trajet le plus court entre",debut,"et",arrive,"est:")
    for i in s2:
        print(i.nom)

elif (mode == "fastest"):
    s3, t3 = fastest(trajet, heure)
    print("Trajet le plus rapide entre",debut,"et",arrive,"est:")
    for i in s3:
        print(i.nom)
    print("Le trajet mettra", t3,"minutes")

elif (mode == "foremost"):
    s4, t4 = foremost(trajet, heure)
    print("Trajet arrivant le plus tot entre",debut,"et",arrive,"est:")
    for i in s4:
        print(i.nom)
    print("Vous arriverez à", t4)
