import BDD_Intervention as BDD1
from datetime import datetime as dt
from datetime import timedelta
import time
from collections import Counter

BDD1 = BDD1.BasedeDonneeOne()


"""Fonction afin de calculer le temps de présence en fonction de l'horaire d'entrée et de sortie"""
def tempsdePresence(entreeDT, sortieDT):
    #Fonction pour obtenir un nombre de type float (secondes), pour la compatibilité avec le temps ().
    entreeDT_ts = time.mktime(entreeDT.timetuple())
    sortieDT_ts = time.mktime(sortieDT.timetuple())
    a = sortieDT_ts-entreeDT_ts
    #secondes => minutes
    temps_presence = int(a/60)
    return temps_presence


"""Fonction afin de calculer le nombre d'intervenants qui présenter durant dateDe et dateA
       par une période données"""
def nbPresence_HorairePeriode(site, dateDe, timeDe, dateA, timeA, periode):

    """Les dates et les horaires qu'on a récupéré sont de type string
    Afin de pouvoir comparer les dates avec les dates dans le fichier,
    on joind la date et l'horaire puis reformer afin d'avoir le même format que la date dans le fichier
    technique : (string->datetime->string->datetime)
    """
    userDateDebut = dateDe + " " + timeDe
    userDateDebut = dt.strptime(userDateDebut, "%Y-%m-%d %H:%M")
    userDateDebut = userDateDebut.strftime('%d/%m/%Y %H:%M')
    userDateDebut = dt.strptime(userDateDebut, "%d/%m/%Y %H:%M")
    #utiliser pour ajouter la période
    compareDateDebut = userDateDebut
    userDateFin = dateA + " " + timeA
    userDateFin = dt.strptime(userDateFin, "%Y-%m-%d %H:%M")
    userDateFin = userDateFin.strftime('%d/%m/%Y %H:%M')
    userDateFin = dt.strptime(userDateFin, "%d/%m/%Y %H:%M")

    """Afin de pouvoir compter le nombre de personnes présentées d'une période,
    on compte d'abord qu'il y a combien de minutes entre deux datetimes,
    ensuite on divise les minutes avec la période pour obtenir le nb de fois qu'on doit ajouter la période
    """
    userDateDebut_ts = time.mktime(userDateDebut.timetuple())
    userDateFin_ts = time.mktime(userDateFin.timetuple())
    addPeriodeFois = ((userDateFin_ts - userDateDebut_ts) / 60) / int(periode)

    dic = {}
    #Les informations à afficher sur la page
    dataInfo = "<p>Site : " + site + "</p>" + \
               "<p>Date début : " + dateDe + "</p>" + \
               "<p>Heure début : " + timeDe + "</p>" + \
               "<p>Date fin : " + dateA + "</p>" + \
               "<p>Heure fin : " + timeA + "</p>" + \
               "<p>Période : " + periode + "</p>"

    #Si la date de début est inférieure à la date de fin
    if userDateDebut <= userDateFin:

        #Boucle pour parcourir tous les éléments dans la base de données (dataframe)
        for i in range(0, len(BDD1)):
            #Si le site correspond au site défini par l'utilisateur
            if BDD1.iloc[i]["Site"] == site:

                #Récupérer l'horodatage entrée de chaque intervenant
                entreeDT = dt.strptime(BDD1.iloc[i]["Horodatage Entree"], "%d/%m/%Y %H:%M")

                #Vérifier si l'horodatage est entre deux dates définies
                if userDateDebut <= entreeDT and userDateFin >= entreeDT:
                    # Pour le nombre de fois à ajouter la période
                    for fois in range(0, int(addPeriodeFois)):
                        # Date 1 est l'horodatege entrée + période*fois (commencé par 0) donc la 1er fois on ajoute pas
                        compareDateDebut1 = compareDateDebut + timedelta(minutes=int(periode) * fois)
                        compareDateDebut2 = compareDateDebut + timedelta(minutes=int(periode) * (fois + 1))
                        if compareDateDebut1 <= entreeDT < compareDateDebut2:
                            # Mettre le type de valeur de dictionnaire qui est une liste
                            dic.setdefault(compareDateDebut1, [])
                            # Ajouter l'horodatage entrée conforme à la dictionnaire
                            # La clé de dictionnaire est la DateDebut1
                            dic[compareDateDebut1].append(entreeDT)

    return dic, dataInfo


"""Cette fonction permet de compter
    >  le nombre de personnes selon le temps de présence (site, dateDe, dateA, "", "")
    >  le nombre de personnes de chaque entreprise selon le temps de présence (site, dateDe, dateA, "", "Raison sociale")
    >  le nombre de personnes de chaque spécialité selon le temps de présence (site, dateDe, dateA, "", "Specialite")
    >  le nombre de personnes d'une entreprise selon le temps de présence (site, dateDe, dateA, entreprise, "Raison sociale")
    >  le nombre de personnes d'une spécialité selon le temps de présence (site, dateDe, dateA, specialite, "Specialite")
"""
def nbPers_TempsPresence(site, dateDe, dateA, entreOUSpec, type):
    userDateDebut = dateDe + " " + "00:00"
    userDateDebut = dt.strptime(userDateDebut, "%Y-%m-%d %H:%M")
    userDateDebut = userDateDebut.strftime('%d/%m/%Y %H:%M')
    userDateDebut = dt.strptime(userDateDebut, "%d/%m/%Y %H:%M")
    userDateFin = dateA + " " + "11:59"
    userDateFin = dt.strptime(userDateFin, "%Y-%m-%d %H:%M")
    userDateFin = userDateFin.strftime('%d/%m/%Y %H:%M')
    userDateFin = dt.strptime(userDateFin, "%d/%m/%Y %H:%M")

    dic = {}
    dataInfo = "<p>Site : " + site + "</p>" + \
               "<p>Date début : " + dateDe + "</p>" + \
               "<p>Date fin : " + dateA + "</p>"
    if(entreOUSpec!=""):
        dataInfo = dataInfo + "<p>" + type + " : " + entreOUSpec + "</p>"


    if userDateDebut <= userDateFin:
        listeTemps = ["0h30", "1H", "1H30", "2H", "2H30", "3H", "3H30", "4H", "4H30", "5H", "5H30", "6H", "6H30", ">7H"]
        for i in range(0, len(BDD1)):
            if BDD1.iloc[i]["Site"] == site:
                entreeDT = dt.strptime(BDD1.iloc[i]["Horodatage Entree"], "%d/%m/%Y %H:%M")
                if userDateDebut <= entreeDT and userDateFin >= entreeDT:
                    if (entreOUSpec != "" and entreOUSpec == BDD1.iloc[i][type]):
                        sortieDT = dt.strptime(BDD1.iloc[i]["Horodatage Sortie"], "%d/%m/%Y %H:%M")
                        temps_presence_tm = tempsdePresence(entreeDT, sortieDT)
                        for i in range(0, len(listeTemps)):
                            de = 30*i
                            a = 30*(i+1)
                            if de <= temps_presence_tm < a:
                                dic.setdefault(listeTemps[i], [])
                                dic[listeTemps[i]].append(temps_presence_tm)
                    elif entreOUSpec == "":
                        sortieDT = dt.strptime(BDD1.iloc[i]["Horodatage Sortie"], "%d/%m/%Y %H:%M")
                        temps_presence_tm = tempsdePresence(entreeDT, sortieDT)
                        for i in range(0, len(listeTemps)):
                            de = 30 * i
                            a = 30 * (i + 1)
                            if de <= temps_presence_tm < a:
                                dic.setdefault(listeTemps[i], [])
                                dic[listeTemps[i]].append(temps_presence_tm)

    return dic, dataInfo



"""Pour l'affichage d'une liste de personnes selon
    > Entreprise
    > Spécialité
    > Heure d'entrée
    > Heure de sortie
Cette fonction est utilisé avec les fonctions statistique_intervention et intervenants_Info() dans le contrôleur
Ex:
dicContrat, dicEntrep, dicSpec, dicEntree, dicSortie, dicTemps = SI.statistique_intervention(data)
dic, dataInfo = SI.nbPers_listes(site, dateDe, dateA, entreprise, spec, "Raison sociale")
tableInfo = ct.intervenants_Info(dic)
"""
def nbPers_listes(site, dateDe, dateA, entreOUspec, type, timeDe, timeA, temps):
    selontime = timeDe
    dic = {}
    dataInfo = "<p>Site : " + site + "</p>" + \
               "<p>Date début : " + dateDe + "</p>"
    if entreOUspec!="":
        dataInfo = dataInfo + "<p>Date fin : " + dateA + "</p>" \
                   + "<p>" + type + " : " + entreOUspec + "</p>"
        timeDe = "00:00"
        timeA = "23:59"
    elif timeDe!="":
        dataInfo = dataInfo + "<p>Heure début : " + timeDe + "</p>" + \
               "<p>Date fin : " + dateA + "</p>" + "<p>Heure fin : " + timeA + "</p>"
    elif temps!="":
        dataInfo = dataInfo + "<p>Date fin : " + dateA + "</p>" + "<p>Le temps de présence : " + temps + "</p>"
        timeDe = "00:00"
        timeA = "23:59"
    else:
        dataInfo = dataInfo + "<p>Date fin : " + dateA + "</p>"
        timeDe = "00:00"
        timeA = "23:59"

    userDateDebut = dateDe + " " + timeDe
    userDateDebut = dt.strptime(userDateDebut, "%Y-%m-%d %H:%M")
    userDateDebut = userDateDebut.strftime('%d/%m/%Y %H:%M')
    userDateDebut = dt.strptime(userDateDebut, "%d/%m/%Y %H:%M")
    userDateFin = dateA + " " + timeA
    userDateFin = dt.strptime(userDateFin, "%Y-%m-%d %H:%M")
    userDateFin = userDateFin.strftime('%d/%m/%Y %H:%M')
    userDateFin = dt.strptime(userDateFin, "%d/%m/%Y %H:%M")

    if userDateDebut <= userDateFin:
        #Liste des informations à afficher
        index = ["Matricule", "Nature du contrat de travail",
                 "Raison sociale", "Specialite",
                 "Horodatage Entree", "Horodatage Sortie"]
        listeTemps = ["0H30", "1H", "1H30", "2H", "2H30", "3H", "3H30", "4H", "4H30", "5H", "5H30", "6H", "6H30", ">7H"]
        for i in range(0, len(BDD1)):
            if BDD1.iloc[i]["Site"] == site:
                entreeDT = dt.strptime(BDD1.iloc[i]["Horodatage Entree"], "%d/%m/%Y %H:%M")
                if userDateDebut <= entreeDT and userDateFin >= entreeDT:
                    sortieDT = dt.strptime(BDD1.iloc[i]["Horodatage Sortie"], "%d/%m/%Y %H:%M")
                    temps_presence_tm = tempsdePresence(entreeDT, sortieDT)

                    if temps!="":
                        info = []
                        for i in range(0, len(listeTemps)):
                            if temps == listeTemps[i]:
                                de = 30*i
                                a = 30*(i+1)
                                if de <= temps_presence_tm < a:
                                    for j in index:
                                        info.append(BDD1.iloc[i][j])
                                    info.append(temps_presence_tm)
                                    dic.setdefault(temps, [])
                                    dic[temps].append(info)
                    elif selontime != "":
                        keys = BDD1.iloc[i][type]
                        info = []
                        for j in index:
                            info.append(BDD1.iloc[i][j])
                        info.append(temps_presence_tm)
                        dic.setdefault(keys, [])
                        dic[keys].append(info)
                    elif  BDD1.iloc[i][type] == entreOUspec:
                        info = []
                        for j in index:
                            info.append(BDD1.iloc[i][j])
                        info.append(temps_presence_tm)
                        dic.setdefault(entreOUspec, [])
                        dic[entreOUspec].append(info)
                    elif entreOUspec == "":
                        isEntreORisSpec = BDD1.iloc[i][type]
                        info = []
                        for j in index:
                            info.append(BDD1.iloc[i][j])
                        info.append(temps_presence_tm)
                        dic.setdefault(isEntreORisSpec, [])
                        dic[isEntreORisSpec].append(info)


    return dic, dataInfo


"""
    Fonction pour
    1. affichier une liste d'intervenants qui présentent durant deux dates
    2. rechercher un intervenant et tous ces intervenants durant deux dates

Cette fonction est utilisé avec les fonctions statistique_intervention et intervenants_Info() dans le contrôleur
Ex:
dicContrat, dicEntrep, dicSpec, dicEntree, dicSortie, dicTemps = SI.statistique_intervention(data)
dic, dataInfo = SI.nbPers_listes(site, dateDe, dateA, entreprise, spec, "Raison sociale")
tableInfo = ct.intervenants_Info(dic)
"""
def recherche_Intervenant(site, dateDe, dateA, intervenant):

    dic = {}
    dataInfo = "<p>Site : " + site + "</p>" + \
               "<p>Date début : " + dateDe + "</p>" + \
               "<p>Date fin : " + dateA + "</p>"

    if intervenant!="":
        dataInfo = dataInfo + "<p>Intervenant : " + intervenant + "</p>"
    timeDe = "00:00"
    timeA = "23:59"

    userDateDebut = dateDe + " " + timeDe
    userDateDebut = dt.strptime(userDateDebut, "%Y-%m-%d %H:%M")
    userDateDebut = userDateDebut.strftime('%d/%m/%Y %H:%M')
    userDateDebut = dt.strptime(userDateDebut, "%d/%m/%Y %H:%M")
    compareDateDebut = userDateDebut
    userDateFin = dateA + " " + timeA
    userDateFin = dt.strptime(userDateFin, "%Y-%m-%d %H:%M")
    userDateFin = userDateFin.strftime('%d/%m/%Y %H:%M')
    userDateFin = dt.strptime(userDateFin, "%d/%m/%Y %H:%M")

    userDateDebut_ts = time.mktime(userDateDebut.timetuple())
    userDateFin_ts = time.mktime(userDateFin.timetuple())
    addPeriodeFois = int(((userDateFin_ts - userDateDebut_ts) / 60) / 1439)

    if userDateDebut <= userDateFin:
        #Liste des informations à afficher
        index = ["Matricule", "Nature du contrat de travail",
                 "Raison sociale", "Specialite",
                 "Horodatage Entree", "Horodatage Sortie"]
        listeTemps = ["0H30", "1H", "1H30", "2H", "2H30", "3H", "3H30", "4H", "4H30", "5H", "5H30", "6H", "6H30", ">7H"]

        for i in range(0, len(BDD1)):
            if BDD1.iloc[i]["Site"] == site:
                entreeDT = dt.strptime(BDD1.iloc[i]["Horodatage Entree"], "%d/%m/%Y %H:%M")
                if userDateDebut <= entreeDT and userDateFin >= entreeDT:
                    sortieDT = dt.strptime(BDD1.iloc[i]["Horodatage Sortie"], "%d/%m/%Y %H:%M")
                    temps_presence_tm = tempsdePresence(entreeDT, sortieDT)
                    if BDD1.iloc[i]["Matricule"] == intervenant:
                        for fois in range(0, addPeriodeFois):
                            # Date 1 est l'horodatege entrée + période*fois (commencé par 0) donc la 1ere fois on n'ajoute pas
                            compareDateDebut1 = compareDateDebut + timedelta(days=1 * fois)
                            compareDateDebut2 = compareDateDebut + timedelta(days=1 * (fois + 1))
                            if compareDateDebut1 <= entreeDT < compareDateDebut2:
                                info = []
                                for j in index:
                                    info.append(BDD1.iloc[i][j])
                                info.append(temps_presence_tm)
                                dic.setdefault(compareDateDebut1, [])
                                dic[compareDateDebut1].append(info)

                    elif intervenant=="":
                        for fois in range(0, int(addPeriodeFois)):
                            # Date 1 est l'horodatege entrée + période*fois (commencé par 0) donc la 1ere fois on n'ajoute pas
                            compareDateDebut1 = compareDateDebut + timedelta(days=1 * fois)
                            compareDateDebut2 = compareDateDebut + timedelta(days=1 * (fois + 1))
                            if compareDateDebut1 <= entreeDT < compareDateDebut2:
                                info = []
                                for j in index:
                                    info.append(BDD1.iloc[i][j])
                                info.append(temps_presence_tm)
                                dic.setdefault(compareDateDebut1, [])
                                dic[compareDateDebut1].append(info)

    return dic, dataInfo


"""Fonction pour faire les statistiques
    - nb de personnes présentées selon entreprise
    - nb de personnes présentées selon spécialité
    - nb de personnes présentées selon heure d'entrée
    - nb de personnes présentées selon le temps de présence
"""
def statistique_intervention(dic):
    listeContrat = []
    listeEntrep = []
    listeSpec = []
    listeEntree = []
    listeSortie = []
    listeTemps = []
    for keys, values in dic.items():
        for element in values:
            listeContrat.append(element[1])
            listeEntrep.append(element[2])
            listeSpec.append(element[3])
            dateEntre = element[4].split(' ')
            dateEntre = dateEntre[1].split(':')
            listeEntree.append(dateEntre[0])
            dateSortie = element[5].split(' ')
            dateSortie = dateSortie[1].split(':')
            listeSortie.append(dateSortie[0])
            listeTemps.append(element[6])

    dicContrat = dict(Counter(listeContrat))
    dicEntrep = dict(Counter(listeEntrep))
    dicSpec = dict(Counter(listeSpec))
    dicEntree = dict(Counter(listeEntree))
    dicSortie = dict(Counter(listeSortie))
    dicTemps = {}
    temps = ["0H30", "1H", "1H30", "2H", "2H30", "3H", "3H30", "4H", "4H30", "5H", "5H30", "6H", "6H30", ">7H"]
    for t in listeTemps:
        for i in range(0, len(temps)):
            de = 30 * i
            a = 30 * (i + 1)
            if de <= t < a:
                dicTemps.setdefault(temps[i], [])
                dicTemps[temps[i]].append(t)
    return dicContrat, dicEntrep, dicSpec, dicEntree, dicSortie, dicTemps

