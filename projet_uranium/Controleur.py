from collections import OrderedDict
import BDD_Intervention as BDD1
import BDD_Outillage as BDD2
from bokeh.models import LabelSet, ColumnDataSource
from bokeh.plotting import figure
from bokeh.embed import components
import datetime

#La création de la base de données
BaseDeDonnee1 = BDD1.BasedeDonneeOne()
#La création de trois listes entreprises, spécialités et intervenants
lE, lS, lN= BDD1.listederoulante(BaseDeDonnee1)

BaseDeDonnee2 = BDD2.BasedeDonneeTwo()
lM, lC, lE2 =  BDD2.listederoulante(BaseDeDonnee2)    


def templatesOption(type):
    option = ""
    if type == "lM":
        for e in lM:
            option =  option+ "<option value=\"" + str(e) + "\">" + str(e) + "</option>"
    elif type == "lC":
        for e in lC:
            option =  option + "<option value=\"" + str(e) + "\">" + str(e) + "</option>"
    elif type == "lE":
        for e in lE:
            option =  option + "<option value=\"" + str(e) + "\">" + str(e) + "</option>"
    if type == "lE2":
        for e in lE2:
            option =  option+ "<option value=\"" + str(e) + "\">" + str(e) + "</option>"
    elif type == "lS":
        for e in lS:
            option =  option + "<option value=\"" + str(e) + "\">" + str(e) + "</option>"
    elif type == "lN":
        for e in lN:
            option =  option + "<option value=\"" + str(e) + "\">" + str(e) + "</option>"
    return option


#Fonction pour retouner une table avec les informations d'intervention
def intervenants_Info(dict2):
    index = ["Matricule", "Contrat",
             "Entreprise", "Spécialite", "Horodatage Entree",
             "Horodatage Sortie", "Temps présenté"]

    t = """<table style="width:80%;text-align:center;"><tr>"""
    for i in index:
        t = t + """<th style="padding:5px 0px;color:#fff;background-color:#d6d6a5;">""" + i + "</th>"
    t = t + "</tr>"

    for keys, values in dict2.items():
        for l1 in values:
            t = t + "<tr>"
            for e in l1:
                t = t + """<td style="padding:5px 0px;color:#555;background-color:#fff;border-bottom:1px solid #915957;">""" + str(e) +" </td>"
            t = t + "<tr>"
    t = t + "</table>"
    return t


"""Fonction utilisé pour toute fonction statistique pour
    - traiter les résultats statistiques
    - les traiter afin de sortir les infos utilisés par graphique
"""
def traitement(dictionary, dataInfo):
    finalDic = {}
    for keys, values in dictionary.items():
        #compter il y a combien de valeurs pour chaque dict
        #par exemple pour un clé "30/06/2017 10:00 y a 10 valeurs
        #cela veut dire il y a 10 personnes
        if not isinstance(values, int):
            finalDic[keys] = len(values)
        else:
            finalDic = dictionary

    #Organiser les valeurs afin de les mettre en ordre (10:30, 10:00, 9:00) -> (9:00, 10:00, 10:30)
    finalDic = OrderedDict((k, v) for k, v in sorted(finalDic.items()))
    x = []
    y = []
    z = []
    for keys, values in finalDic.items():
        #Pour le cas où le clé est de type datetime
        if isinstance(keys, datetime.datetime):
            keys = keys.strftime('%d_%m_%Hh%M')
        x.append(keys)
        y.append(values)
        #Z est pour les annotations, donc on change le type en string
        z.append(str(values))

    return x, y, z, dataInfo


"""Fonction pour créer la graphique et générer un <div> et un <script>
    afin de pouvoir insérer dans le fichier.html et afficher le graphique sur l'application web
    On définit :
    titre : string, le titre de graphique
    dataX : x sorti par traitement, data pour afficher dans la zone horizontal
    dataY : y sorti par traitement, data pour afficher dans la zone vertical
    dataLabel : z sorti par traitement, data pour afficher les annotations
    x_axis_label : le titre de la zone horizontal
    y_axis_label : le titre de la zone vertical
    legend : le titre de la ligne / point sur la graphique
    color : couleur de la ligne/point
    EX:
    script, div = ct.controleur("Nb de personnes présentées selon horaire et période", getX, getY, getZ, 'Datetime', 'NbPers', "NbPers", "blue")
    """
def controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color):

    #Convertir les données x, y, z en dataframe
    source = ColumnDataSource(data=dict(dataX=dataX,
                                   dataY=dataY,
                                   dataLabel=dataLabel))

    #Création une figure pour mettre la graphique avec
    plot = figure(title=titre,
                      x_range=dataX,  #la gamme de dataX
                      plot_width=1000,
                      plot_height=600,
                      x_axis_label=x_axis_label,
                      y_axis_label=y_axis_label,
                      toolbar_location="above") #mettre le bar à l'outil en haut

    """La combinaison de glyphes multiples 
    sur un seul complot consiste à appeler plus d'une méthode glyph sur une seule figure"""
    plot.line(source=source,
              x='dataX',
              y='dataY',
              legend=legend,
              color=color,
              alpha=1)
    plot.circle(source=source, x='dataX', y='dataY', legend=legend, fill_color="white", size=8)

    #Ajouter des annotations
    labels = LabelSet(x='dataX', y='dataY', text='dataLabel', level='glyph',
                          x_offset=5, y_offset=5, source=source, render_mode='canvas')
    plot.add_layout(labels)

    script, div = components(plot)

    return script, div

