import BDD_Outillage as BDD2
from datetime import datetime as dt
from datetime import timedelta
import time

BDD2 = BDD2.BasedeDonneeTwo()


def nbOutils_HorairePeriode(site, dateDe, timeDe, dateA, timeA, periode):

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
        for i in range(0, len(BDD2)):
            #Si le site correspond au site défini par l'utilisateur
            if BDD2.iloc[i]["SITE_CODE"] == site:

                #Récupérer l'horodatage entrée de chaque intervenant
                datemvtDT = dt.strptime(BDD2.iloc[i]["DATE_MOUVEMENT"], "%d/%m/%Y %H:%M")

                #Vérifier si l'horodatage est entre deux dates définies
                if userDateDebut <= datemvtDT and userDateFin >= datemvtDT:
                    # Pour le nombre de fois à ajouter la période
                    for fois in range(0, int(addPeriodeFois)):
                        # Date 1 est l'horodatege entrée + période*fois (commencé par 0) donc la 1er fois on ajoute pas
                        compareDateDebut1 = compareDateDebut + timedelta(minutes=int(periode) * fois)
                        compareDateDebut2 = compareDateDebut + timedelta(minutes=int(periode) * (fois + 1))
                        if compareDateDebut1 <= datemvtDT < compareDateDebut2:
                            # Mettre le type de valeur de dictionnaire qui est une liste
                            dic.setdefault(compareDateDebut1, [])
                            # Ajouter l'horodatage entrée conforme à la dictionnaire
                            # La clé de dictionnaire est la DateDebut1
                            dic[compareDateDebut1].append(datemvtDT)

    return dic, dataInfo

def nbEmprunts_HorairePeriode(site, dateDe, timeDe, dateA, timeA, periode, defautOUclient, type):

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
               "<p>Période : " + periode + "</p>" + \
               "<p>" + type + " : " + defautOUclient + "</p>"

    #Si la date de début est inférieure à la date de fin
    if userDateDebut <= userDateFin:

        #Boucle pour parcourir tous les éléments dans la base de données (dataframe)
        for i in range(0, len(BDD2)):
            #Si le site correspond au site défini par l'utilisateur
            if BDD2.iloc[i]["SITE_CODE"] == site:

                #Récupérer l'horodatage entrée de chaque intervenant
                datemvtDT = dt.strptime(BDD2.iloc[i]["DATE_MOUVEMENT"], "%d/%m/%Y %H:%M")

                #Vérifier si l'horodatage est entre deux dates définies
                if userDateDebut <= datemvtDT and userDateFin >= datemvtDT:
                    if (defautOUclient != "" and defautOUclient == BDD2.iloc[i][type]):
                        # Pour le nombre de fois à ajouter la période
                        for fois in range(0, int(addPeriodeFois)):
                            # Date 1 est l'horodatege entrée + période*fois (commencé par 0) donc la 1ere fois on n'ajoute pas
                            compareDateDebut1 = compareDateDebut + timedelta(minutes=int(periode) * fois)
                            compareDateDebut2 = compareDateDebut + timedelta(minutes=int(periode) * (fois + 1))
                            if compareDateDebut1 <= datemvtDT < compareDateDebut2:
                                # Mettre le type de valeur de dictionnaire qui est une liste
                                dic.setdefault(compareDateDebut1, [])
                                # Ajouter l'horodatage entrée conforme à la dictionnaire
                                # La clé de dictionnaire est la DateDebut1
                                dic[compareDateDebut1].append(datemvtDT)

    return dic, dataInfo


"""Cette fonction permet de compter :
    >  le nombre d'outils selon la période (site, dateDe, dateA, "", "")
    >  le nombre d'outils d'une entreprise selon la période (site, dateDe, dateA, entreprise, "BNU")
    >  le nombre d'outils d'un magasin selon la période (site, dateDe, dateA, magasin, "CODE")
    >  le nombre d'emprunts d'un client selon la période (site, dateDe, dateA, client, "UTILISATEUR")
"""
def nbOutils_User(site, dateDe, timeDe, dateA, timeA, periode, entreOUmagOUuser, type):
    userDateDebut = dateDe + " " + timeDe
    userDateDebut = dt.strptime(userDateDebut, "%Y-%m-%d %H:%M")
    userDateDebut = userDateDebut.strftime('%d/%m/%Y %H:%M')
    userDateDebut = dt.strptime(userDateDebut, "%d/%m/%Y %H:%M")
    # utiliser pour ajouter la période
    compareDateDebut = userDateDebut
    userDateFin = dateA + " " + timeA
    userDateFin = dt.strptime(userDateFin, "%Y-%m-%d %H:%M")
    userDateFin = userDateFin.strftime('%d/%m/%Y %H:%M')
    userDateFin = dt.strptime(userDateFin, "%d/%m/%Y %H:%M")

    userDateDebut_ts = time.mktime(userDateDebut.timetuple())
    userDateFin_ts = time.mktime(userDateFin.timetuple())
    addPeriodeFois = ((userDateFin_ts - userDateDebut_ts) / 60) / int(periode)

    dic = {}
    if(entreOUmagOUuser!=""):
        dataInfo = "<p>Site : " + site + "</p>" + \
                   "<p>Date début : " + dateDe + "</p>" + \
                   "<p>Heure début : " + timeDe + "</p>" + \
                   "<p>Date fin : " + dateA + "</p>" + \
                   "<p>Heure fin : " + timeA + "</p>" + \
                   "<p>" + type + " : " + entreOUmagOUuser + "</p>"
    else:
        dataInfo = "<p>Site : " + site + "</p>" + \
                     "<p>Date début : " + dateDe + "</p>" + \
                     "<p>Date fin : " + dateA + "</p>"

    if userDateDebut <= userDateFin:
        for i in range(0, len(BDD2)):
            if BDD2.iloc[i]["SITE_CODE"] == site:
                datemvtDT = dt.strptime(BDD2.iloc[i]["DATE_MOUVEMENT"], "%d/%m/%Y %H:%M")
                if userDateDebut <= datemvtDT and userDateFin >= datemvtDT:
                    if (entreOUmagOUuser != "" and entreOUmagOUuser == BDD2.iloc[i][type]):
                        for fois in range(0, int(addPeriodeFois)):
                            compareDateDebut1 = compareDateDebut + timedelta(minutes=int(periode) * fois)
                            compareDateDebut2 = compareDateDebut + timedelta(minutes=int(periode) * (fois + 1))
                            if compareDateDebut1 <= datemvtDT < compareDateDebut2:
                                dic.setdefault(compareDateDebut1, [])
                                dic[compareDateDebut1].append(datemvtDT)

    return dic, dataInfo

def nbOutils_User2(site, dateDe, timeDe, dateA, timeA, periode, mouvement, type, entreOUmagOUuser, type2):
    userDateDebut = dateDe + " " + timeDe
    userDateDebut = dt.strptime(userDateDebut, "%Y-%m-%d %H:%M")
    userDateDebut = userDateDebut.strftime('%d/%m/%Y %H:%M')
    userDateDebut = dt.strptime(userDateDebut, "%d/%m/%Y %H:%M")
    # utiliser pour ajouter la période
    compareDateDebut = userDateDebut
    userDateFin = dateA + " " + timeA
    userDateFin = dt.strptime(userDateFin, "%Y-%m-%d %H:%M")
    userDateFin = userDateFin.strftime('%d/%m/%Y %H:%M')
    userDateFin = dt.strptime(userDateFin, "%d/%m/%Y %H:%M")

    userDateDebut_ts = time.mktime(userDateDebut.timetuple())
    userDateFin_ts = time.mktime(userDateFin.timetuple())
    addPeriodeFois = ((userDateFin_ts - userDateDebut_ts) / 60) / int(periode)

    dic = {}
    if(entreOUmagOUuser!=""):
        dataInfo = "<p>Site : " + site + "</p>" + \
                   "<p>Date début : " + dateDe + "</p>" + \
                   "<p>Heure début : " + timeDe + "</p>" + \
                   "<p>Date fin : " + dateA + "</p>" + \
                   "<p>Heure fin : " + timeA + "</p>" + \
                   "<p>" + type + " : " + mouvement + "</p>" + \
                   "<p>" + type2 + " : " + entreOUmagOUuser + "</p>"
    else:
        dataInfo = "<p>Site : " + site + "</p>" + \
                     "<p>Date début : " + dateDe + "</p>" + \
                     "<p>Date fin : " + dateA + "</p>"

    if userDateDebut <= userDateFin:
        for i in range(0, len(BDD2)):
            if BDD2.iloc[i]["SITE_CODE"] == site:
                datemvtDT = dt.strptime(BDD2.iloc[i]["DATE_MOUVEMENT"], "%d/%m/%Y %H:%M")
                if userDateDebut <= datemvtDT and userDateFin >= datemvtDT:
                    if (entreOUmagOUuser != "" and entreOUmagOUuser == BDD2.iloc[i][type]):
                        for fois in range(0, int(addPeriodeFois)):
                            compareDateDebut1 = compareDateDebut + timedelta(minutes=int(periode) * fois)
                            compareDateDebut2 = compareDateDebut + timedelta(minutes=int(periode) * (fois + 1))
                            if compareDateDebut1 <= datemvtDT < compareDateDebut2:
                                dic.setdefault(compareDateDebut1, [])
                                dic[compareDateDebut1].append(datemvtDT)

    return dic, dataInfo

def nbOutils_User3(site, dateDe, timeDe, dateA, timeA, periode, mouvement, mouvement2, type, entreOUmagOUuser, type2):
    userDateDebut = dateDe + " " + timeDe
    userDateDebut = dt.strptime(userDateDebut, "%Y-%m-%d %H:%M")
    userDateDebut = userDateDebut.strftime('%d/%m/%Y %H:%M')
    userDateDebut = dt.strptime(userDateDebut, "%d/%m/%Y %H:%M")
    # utiliser pour ajouter la période
    compareDateDebut = userDateDebut
    userDateFin = dateA + " " + timeA
    userDateFin = dt.strptime(userDateFin, "%Y-%m-%d %H:%M")
    userDateFin = userDateFin.strftime('%d/%m/%Y %H:%M')
    userDateFin = dt.strptime(userDateFin, "%d/%m/%Y %H:%M")

    userDateDebut_ts = time.mktime(userDateDebut.timetuple())
    userDateFin_ts = time.mktime(userDateFin.timetuple())
    addPeriodeFois = ((userDateFin_ts - userDateDebut_ts) / 60) / int(periode)

    dic = {}
    if(mouvement!=""):
        dataInfo = "<p>Site : " + site + "</p>" + \
                   "<p>Date début : " + dateDe + "</p>" + \
                   "<p>Heure début : " + timeDe + "</p>" + \
                   "<p>Date fin : " + dateA + "</p>" + \
                   "<p>Heure fin : " + timeA + "</p>" + \
                   "<p>" + type + " : " + mouvement + " & " + mouvement2 + "</p>" + \
                   "<p>" + type2 + " : " + entreOUmagOUuser + "</p>"
    else:
        dataInfo = "<p>Site : " + site + "</p>" + \
                     "<p>Date début : " + dateDe + "</p>" + \
                     "<p>Date fin : " + dateA + "</p>"

    if userDateDebut <= userDateFin:
        for i in range(0, len(BDD2)):
            if BDD2.iloc[i]["SITE_CODE"] == site:
                datemvtDT = dt.strptime(BDD2.iloc[i]["DATE_MOUVEMENT"], "%d/%m/%Y %H:%M")
                if userDateDebut <= datemvtDT and userDateFin >= datemvtDT:
                    if (entreOUmagOUuser != "" and entreOUmagOUuser == BDD2.iloc[i][type]):
                        for fois in range(0, int(addPeriodeFois)):
                            compareDateDebut1 = compareDateDebut + timedelta(minutes=int(periode) * fois)
                            compareDateDebut2 = compareDateDebut + timedelta(minutes=int(periode) * (fois + 1))
                            if compareDateDebut1 <= datemvtDT < compareDateDebut2:
                                dic.setdefault(compareDateDebut1, [])
                                dic[compareDateDebut1].append(datemvtDT)

    return dic, dataInfo




