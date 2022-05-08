import cherrypy
import os.path
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('Templates'))
import Statistique_Intervention as SI
import Controleur as ct
import Statistique_Outillage as SO
from bokeh.plotting import figure
from bokeh.embed import components
import numpy as np
from datetime import datetime as dt

class uranium(object):

    @cherrypy.expose
    #Page d'accueil
    def index(self):
        file = open('./Templates/WebApp.html', 'r')
        htmlTemplate = file.read()
        file.close()

        """Graphic d'accueil
        figure : Une sous-classe de Plot
        qui simplifie la création de graphique avec des axes, des grilles et des outils par défaut
        Ici, on définit la taille de graphique et l'emplacement de toolbar
        """
        plot = figure(width=1000, height=600,
                      toolbar_location="above")

        #utiliser les maths pour dessiner un coueur
        t = np.arange(0, 2 * np.pi, 0.1)
        x = 16 * np.sin(t) ** 3
        y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
        #utiliser la méthode cicrcle() de figure
        plot.circle(x=x, y=y)
        #Renvoie les composants individuels pour un encastrement en ligne à l'aide de la fonction components ().
        #<script> : contient les données de votre intrigue
        #balise <div> : associée à laquelle la vue de parcelle est chargée
        script, div = components(plot)

        #Les informations à afficher
        info = "<p> Bienvenue. Veuillez commencer votre recherche. </p>"

        #Appeler le fichier html
        template = env.get_template('WebApp.html')
        #Le fichier contient deux templates, on assigne les valeurs pour ces templates

        #Les listes pour ajouter dans les listes déroulantes dans html
        templatesEntreprises = ct.templatesOption("lE")
        templatesSpecialites = ct.templatesOption("lS")
        templatesIntervenants = ct.templatesOption("lN")
        templatesEntreprises2 = ct.templatesOption("lE2")
        templatesMagasins = ct.templatesOption("lM")
        templatesClients = ct.templatesOption("lC")


        return template.render(entreprise=templatesEntreprises, specialite=templatesSpecialites, intervenant = templatesIntervenants,
                               entreprise2=templatesEntreprises2, magasin=templatesMagasins, client=templatesClients,
                               infomation=info, divforBokeh=script+div)


    @cherrypy.expose
    #0-Nb de personnes présentes par horaire et période
    def type0(self, site, dateDe, dateA, timeDe, timeA, periode):
        templatesEntreprises = ct.templatesOption("lE")
        templatesSpecialites = ct.templatesOption("lS")
        templatesIntervenants = ct.templatesOption("lN")
        templatesEntreprises2 = ct.templatesOption("lE2")
        templatesMagasins = ct.templatesOption("lM")
        templatesClients = ct.templatesOption("lC")

        #Transformer les strings "date" en type datetime
        userDateDebut = dateDe + " " + timeDe
        userDateDebut = dt.strptime(userDateDebut, "%Y-%m-%d %H:%M")
        userDateFin = dateA + " " + timeA
        userDateFin = dt.strptime(userDateFin, "%Y-%m-%d %H:%M")
        #Vérifier si la date de début est inférieure à la date de fin
        if not userDateDebut < userDateFin:
            dataInfo = "<h1 style=\"color:red\">Erreur de saisie</h1>"
            div = "<h2>La date de début est supérieure à la date de fin</h2>"
        else :
            #Utiliser la fonction dans SI
            data, dataInfo = SI.nbPresence_HorairePeriode(site, dateDe, timeDe, dateA, timeA, periode)
            getX, getY, getZ, dataInfo = ct.traitement(data, dataInfo)
            #controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
            script, div = ct.controleur("Nb de personnes présentées selon horaire et période", getX, getY, getZ, 'Datetime', 'NbPers', "NbPers", "blue")
            div = script+div
        template = env.get_template('WebApp.html')
        return template.render(entreprise=templatesEntreprises, specialite=templatesSpecialites, intervenant = templatesIntervenants,
                               entreprise2=templatesEntreprises2, magasin=templatesMagasins, client=templatesClients,
                               infomation = dataInfo, divforBokeh = div)

    @cherrypy.expose
    #1-Nb de personnes présentes par horaire
    def type1(self, site, dateDe, dateA, timeDe, timeA):
        templatesEntreprises = ct.templatesOption("lE")
        templatesSpecialites = ct.templatesOption("lS")
        templatesIntervenants = ct.templatesOption("lN")
        templatesEntreprises2 = ct.templatesOption("lE2")
        templatesMagasins = ct.templatesOption("lM")
        templatesClients = ct.templatesOption("lC")

        userDateDebut = dateDe + " " + timeDe
        userDateDebut = dt.strptime(userDateDebut, "%Y-%m-%d %H:%M")
        userDateFin = dateA + " " + timeA
        userDateFin = dt.strptime(userDateFin, "%Y-%m-%d %H:%M")
        if not userDateDebut < userDateFin:
            dataInfo = "<h1 style=\"color:orange\">Erreur de saisie</h1>"
            div = "<h2>La date de début est supérieure à la date de fin</h2>"
        else:
            # Utiliser la fonction dans SI
            data, dataInfo = SI.nbPresence_HorairePeriode(site, dateDe, timeDe, dateA, timeA, "60")
            getX, getY, getZ, dataInfo = ct.traitement(data, dataInfo)
            # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
            script, div = ct.controleur("Nb de personnes présentées selon horaire", getX, getY, getZ, 'Datetime', 'NbPers', "NbPers", "blue")
            div = script + div

        template = env.get_template('WebApp.html')
        return template.render(entreprise=templatesEntreprises, specialite=templatesSpecialites,
                               intervenant=templatesIntervenants,
                               entreprise2=templatesEntreprises2, magasin=templatesMagasins, client=templatesClients,
                               infomation=dataInfo, divforBokeh=div)


    @cherrypy.expose
    #2-Nb de personnes présentes par temps de présence
    def type2(self, site, dateDe, dateA):
        templatesEntreprises = ct.templatesOption("lE")
        templatesSpecialites = ct.templatesOption("lS")
        templatesIntervenants = ct.templatesOption("lN")
        templatesEntreprises2 = ct.templatesOption("lE2")
        templatesMagasins = ct.templatesOption("lM")
        templatesClients = ct.templatesOption("lC")

        userDateDebut = dateDe + " " + "00:00"
        userDateDebut = dt.strptime(userDateDebut, "%Y-%m-%d %H:%M")
        userDateFin = dateA + " " + "23:59"
        userDateFin = dt.strptime(userDateFin, "%Y-%m-%d %H:%M")
        if not userDateDebut < userDateFin:
            dataInfo = "<h1 style=\"color:orange\">Erreur de saisie</h1>"
            div = "<h2>La date de début est supérieure à la date de fin</h2>"
        else:
            # Utiliser la fonction dans SI
            data, dataInfo = SI.nbPers_TempsPresence(site, dateDe, dateA, "", "")
            getX, getY, getZ, dataInfo = ct.traitement(data, dataInfo)
            # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
            script, div = ct.controleur("Nb de personnes présentées selon le temps de présence", getX, getY, getZ, 'Temps de présence', 'NbPers', "NbPers", "blue")
            div = script + div

        template = env.get_template('WebApp.html')
        return template.render(entreprise=templatesEntreprises, specialite=templatesSpecialites,
                               intervenant=templatesIntervenants,
                               entreprise2=templatesEntreprises2, magasin=templatesMagasins, client=templatesClients,
                               infomation=dataInfo, divforBokeh=div)

    @cherrypy.expose
    #3-Nb de personnes présentes par entreprise
    def type3(self, site, dateDe, dateA):
        templatesEntreprises = ct.templatesOption("lE")
        templatesSpecialites = ct.templatesOption("lS")
        templatesIntervenants = ct.templatesOption("lN")
        templatesEntreprises2 = ct.templatesOption("lE2")
        templatesMagasins = ct.templatesOption("lM")
        templatesClients = ct.templatesOption("lC")

        userDateDebut = dateDe + " " + "00:00"
        userDateDebut = dt.strptime(userDateDebut, "%Y-%m-%d %H:%M")
        userDateFin = dateA + " " + "23:59"
        userDateFin = dt.strptime(userDateFin, "%Y-%m-%d %H:%M")
        if not userDateDebut < userDateFin:
            dataInfo = "<h1 style=\"color:orange\">Erreur de saisie</h1>"
            div = "<h2>La date de début est supérieure à la date de fin</h2>"
        else:
            # Utiliser la fonction dans SI
            data, dataInfo = SI.nbPers_listes(site, dateDe, dateA, "", "Raison sociale", "", "", "")
            getX, getY, getZ, dataInfo = ct.traitement(data, dataInfo)
            # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
            script, div = ct.controleur("Nb de personnes présentées selon entreprise", getX, getY, getZ,
                                        'Entreprise', 'NbPers', "NbPers", "blue")
            div = script+div
        template = env.get_template('WebApp.html')
        return template.render(entreprise=templatesEntreprises, specialite=templatesSpecialites,
                               intervenant=templatesIntervenants,
                               entreprise2=templatesEntreprises2, magasin=templatesMagasins, client=templatesClients,
                               infomation=dataInfo, divforBokeh=div)

    @cherrypy.expose
    # 4-Nb de personnes présentes par spécialité
    def type4(self, site, dateDe, dateA):
        templatesEntreprises = ct.templatesOption("lE")
        templatesSpecialites = ct.templatesOption("lS")
        templatesIntervenants = ct.templatesOption("lN")
        templatesEntreprises2 = ct.templatesOption("lE2")
        templatesMagasins = ct.templatesOption("lM")
        templatesClients = ct.templatesOption("lC")

        userDateDebut = dateDe + " " + "00:00"
        userDateDebut = dt.strptime(userDateDebut, "%Y-%m-%d %H:%M")
        userDateFin = dateA + " " + "23:59"
        userDateFin = dt.strptime(userDateFin, "%Y-%m-%d %H:%M")
        if not userDateDebut < userDateFin:
            dataInfo = "<h1 style=\"color:orange\">Erreur de saisie</h1>"
            div = "<h2>La date de début est supérieure à la date de fin</h2>"
        else:
            # Utiliser la fonction dans SI
            data, dataInfo = SI.nbPers_listes(site, dateDe, dateA, "", "Specialite", "", "", "")
            getX, getY, getZ, dataInfo = ct.traitement(data, dataInfo)
            # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
            script, div = ct.controleur("Nb de personnes présentées selon spécialité", getX, getY, getZ,
                                        'Spécialité', 'NbPers', "NbPers", "blue")
            div = script + div

        template = env.get_template('WebApp.html')
        return template.render(entreprise=templatesEntreprises, specialite=templatesSpecialites,
                               intervenant=templatesIntervenants,
                               entreprise2=templatesEntreprises2, magasin=templatesMagasins, client=templatesClients,
                               infomation=dataInfo, divforBokeh=div)

    @cherrypy.expose
    # 5-Nb de personnes présentes par contrat
    def type5(self, site, dateDe, dateA):
        templatesEntreprises = ct.templatesOption("lE")
        templatesSpecialites = ct.templatesOption("lS")
        templatesIntervenants = ct.templatesOption("lN")
        templatesEntreprises2 = ct.templatesOption("lE2")
        templatesMagasins = ct.templatesOption("lM")
        templatesClients = ct.templatesOption("lC")

        userDateDebut = dateDe + " " + "00:00"
        userDateDebut = dt.strptime(userDateDebut, "%Y-%m-%d %H:%M")
        userDateFin = dateA + " " + "23:59"
        userDateFin = dt.strptime(userDateFin, "%Y-%m-%d %H:%M")
        if not userDateDebut < userDateFin:
            dataInfo = "<h1 style=\"color:orange\">Erreur de saisie</h1>"
            div = "<h2>La date de début est supérieure à la date de fin</h2>"
        else:
            # Utiliser la fonction dans SI
            data, dataInfo = SI.nbPers_listes(site, dateDe, dateA, "", "Nature du contrat de travail", "", "", "")
            getX, getY, getZ, dataInfo = ct.traitement(data, dataInfo)
            # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
            script, div = ct.controleur("Nb de personnes présentées selon contrat", getX, getY, getZ,
                                        'Nature du contrat', 'NbPers', "NbPers", "blue")
            div = script + div
        template = env.get_template('WebApp.html')
        return template.render(entreprise=templatesEntreprises, specialite=templatesSpecialites, intervenant=templatesIntervenants,
                               entreprise2=templatesEntreprises2, magasin=templatesMagasins, client=templatesClients,
                               infomation=dataInfo, divforBokeh=div)


    @cherrypy.expose
    #6- Statistique des intervenants par entreprise
    def type6(self, site, dateDe, dateA, entreprise):
        templatesEntreprises = ct.templatesOption("lE")
        templatesSpecialites = ct.templatesOption("lS")
        templatesIntervenants = ct.templatesOption("lN")
        templatesEntreprises2 = ct.templatesOption("lE2")
        templatesMagasins = ct.templatesOption("lM")
        templatesClients = ct.templatesOption("lC")

        userDateDebut = dateDe + " " + "00:00"
        userDateDebut = dt.strptime(userDateDebut, "%Y-%m-%d %H:%M")
        userDateFin = dateA + " " + "23:59"
        userDateFin = dt.strptime(userDateFin, "%Y-%m-%d %H:%M")
        if not userDateDebut < userDateFin:
            dataInfo = "<h1 style=\"color:orange\">Erreur de saisie</h1>"
            div = "<h2>La date de début est supérieure à la date de fin</h2>"
        else:

            # Utiliser la fonction dans SI
            data, dataInfo = SI.nbPers_listes(site, dateDe, dateA, entreprise, "Raison sociale", "", "", "")

            #Vérifier si le programme a trouvé les informations ou pas
            if not data:
                div = "<div align=\"center\" style=\"color:red;\"><h2> Pas d'intervenants pour cette entreprise </h2></div>"
            else:
                titre = "<h2>Intervenants selon entreprise<h2>"
                dataInfo = titre + dataInfo

                #Fonction pour retourner les différentes résultats de statistques sous forme de dictionnaire

                #Ensuite on convertit les différentes résultats en graphique
                dicContrat, dicEntrep, dicSpec, dicEntree, dicSortie, dicTemps = SI.statistique_intervention(data)
                getX, getY, getZ, dataInfo = ct.traitement(dicContrat, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script1, div1 = ct.controleur("Nb de personnes présentées selon nature du contrat", getX, getY, getZ,
                                              'Nature du contrat', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicEntrep, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script2, div2 = ct.controleur("Nb de personnes présentées selon entreprise", getX, getY, getZ,
                                              'Entreprise', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicSpec, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script3, div3 = ct.controleur("Nb de personnes présentées selon spécialité", getX, getY, getZ,
                                              'Spécialité', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicEntree, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script4, div4 = ct.controleur("Nb de personnes présentées selon heure d'entrée", getX, getY, getZ,
                                              'Heure d\'entrée', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicSortie, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script5, div5 = ct.controleur("Nb de personnes présentées selon heure de sortie", getX, getY, getZ,
                                              'Heure de sortie', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicTemps, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script6, div6 = ct.controleur("Nb de personnes présentées selon le temps de présence", getX, getY, getZ,
                                              'Temps de présence', 'NbPers', "NbPers", "blue")

                tableInfo = ct.intervenants_Info(data)
                div = script1 + div1 + script2 + div2 + script3 + div3 + script4 + div4 + script5 + div5 + script6 + div6 + tableInfo

        template = env.get_template('WebApp.html')
        return template.render(entreprise=templatesEntreprises, specialite=templatesSpecialites,
                               intervenant=templatesIntervenants,
                               entreprise2=templatesEntreprises2, magasin=templatesMagasins, client=templatesClients,
                               infomation=dataInfo, divforBokeh=div)

    @cherrypy.expose
    #7- Statistique des intervenants par specialité
    def type7(self, site, dateDe, dateA, specialite):
        templatesEntreprises = ct.templatesOption("lE")
        templatesSpecialites = ct.templatesOption("lS")
        templatesIntervenants = ct.templatesOption("lN")
        templatesEntreprises2 = ct.templatesOption("lE2")
        templatesMagasins = ct.templatesOption("lM")
        templatesClients = ct.templatesOption("lC")

        userDateDebut = dateDe + " " + "00:00"
        userDateDebut = dt.strptime(userDateDebut, "%Y-%m-%d %H:%M")
        userDateFin = dateA + " " + "23:59"
        userDateFin = dt.strptime(userDateFin, "%Y-%m-%d %H:%M")
        if not userDateDebut < userDateFin:
            dataInfo = "<h1 style=\"color:orange\">Erreur de saisie</h1>"
            div = "<h2>La date de début est supérieure à la date de fin</h2>"
        else:

            # Utiliser la fonction dans SI
            data, dataInfo = SI.nbPers_listes(site, dateDe, dateA, specialite, "Specialite", "", "", "")

            if not data:
                div = "<div align=\"center\" style=\"color:orange\"><h2> Pas d'intervenants pour cette spécialité </h2></div>"
            else:
                titre = "<h2>Intervenants selon spécialité<h2>"
                dataInfo = titre + dataInfo

                dicContrat, dicEntrep, dicSpec, dicEntree, dicSortie, dicTemps = SI.statistique_intervention(data)
                getX, getY, getZ, dataInfo = ct.traitement(dicContrat, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script1, div1 = ct.controleur("Nb de personnes présentées selon nature du contrat", getX, getY, getZ,
                                              'Nature du contrat', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicEntrep, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script2, div2 = ct.controleur("Nb de personnes présentées selon entreprise", getX, getY, getZ,
                                              'Entreprise', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicSpec, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script3, div3 = ct.controleur("Nb de personnes présentées selon spécialité", getX, getY, getZ,
                                              'Spécialité', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicEntree, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script4, div4 = ct.controleur("Nb de personnes présentées selon heure d'entrée", getX, getY, getZ,
                                              'Heure d\'entrée', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicSortie, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script5, div5 = ct.controleur("Nb de personnes présentées selon heure de sortie", getX, getY, getZ,
                                              'Heure de sortie', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicTemps, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script6, div6 = ct.controleur("Nb de personnes présentées selon le temps de présence", getX, getY, getZ,
                                              'Temps de présence', 'NbPers', "NbPers", "blue")

                tableInfo = ct.intervenants_Info(data)
                div = script1 + div1 + script2 + div2 + script3 + div3 + script4 + div4 + script5 + div5 + script6 + div6 + tableInfo

        template = env.get_template('WebApp.html')
        return template.render(entreprise=templatesEntreprises, specialite=templatesSpecialites,
                               intervenant=templatesIntervenants,
                               entreprise2=templatesEntreprises2, magasin=templatesMagasins, client=templatesClients,
                               infomation=dataInfo, divforBokeh=div)

    @cherrypy.expose
    #8- Statistique des intervenants par heure d'entrée
    def type8(self, site, dateDe, timeDe, dateA, timeA):
        templatesEntreprises = ct.templatesOption("lE")
        templatesSpecialites = ct.templatesOption("lS")
        templatesIntervenants = ct.templatesOption("lN")
        templatesEntreprises2 = ct.templatesOption("lE2")
        templatesMagasins = ct.templatesOption("lM")
        templatesClients = ct.templatesOption("lC")

        userDateDebut = dateDe + " " + timeDe
        userDateDebut = dt.strptime(userDateDebut, "%Y-%m-%d %H:%M")
        userDateFin = dateA + " " + timeA
        userDateFin = dt.strptime(userDateFin, "%Y-%m-%d %H:%M")
        if not userDateDebut <= userDateFin:
            dataInfo = "<h1 style=\"color:orange\">Erreur de saisie</h1>"
            div = "<h2>La date de début est supérieure à la date de fin</h2>"
        else:

            # Utiliser la fonction dans SI
            data, dataInfo = SI.nbPers_listes(site, dateDe, dateA, "", "Horodatage Entree", timeDe, timeA, "")

            if not data:
                div = "<div align=\"center\" style=\"color:orange\"><h2> Pas d'intervenants pendant l'heure d'entrée </h2></div>"
            else:
                titre = "<h2>Intervenants selon heure d'entrée<h2>"
                dataInfo = titre + dataInfo

                dicContrat, dicEntrep, dicSpec, dicEntree, dicSortie, dicTemps = SI.statistique_intervention(data)
                getX, getY, getZ, dataInfo = ct.traitement(dicContrat, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script1, div1 = ct.controleur("Nb de personnes présentées selon nature du contrat", getX, getY, getZ,
                                              'Nature du contrat', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicEntrep, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script2, div2 = ct.controleur("Nb de personnes présentées selon entreprise", getX, getY, getZ,
                                              'Entreprise', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicSpec, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script3, div3 = ct.controleur("Nb de personnes présentées selon spécialité", getX, getY, getZ,
                                              'Spécialité', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicEntree, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script4, div4 = ct.controleur("Nb de personnes présentées selon heure d'entrée", getX, getY, getZ,
                                              'Heure d\'entrée', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicSortie, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script5, div5 = ct.controleur("Nb de personnes présentées selon heure de sortie", getX, getY, getZ,
                                              'Heure de sortie', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicTemps, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script6, div6 = ct.controleur("Nb de personnes présentées selon le temps de présence", getX, getY, getZ,
                                              'Temps de présence', 'NbPers', "NbPers", "blue")

                tableInfo = ct.intervenants_Info(data)
                div = script1 + div1 + script2 + div2 + script3 + div3 + script4 + div4 + script5 + div5 + script6 + div6 + tableInfo

        template = env.get_template('WebApp.html')
        return template.render(entreprise=templatesEntreprises, specialite=templatesSpecialites,
                               intervenant=templatesIntervenants,
                               entreprise2=templatesEntreprises2, magasin=templatesMagasins, client=templatesClients,
                               infomation=dataInfo, divforBokeh=div)


    @cherrypy.expose
    #9- Statistique des intervenants par heure de sortie
    def type9(self, site, dateDe, timeDe, dateA, timeA):
        templatesEntreprises = ct.templatesOption("lE")
        templatesSpecialites = ct.templatesOption("lS")
        templatesIntervenants = ct.templatesOption("lN")
        templatesEntreprises2 = ct.templatesOption("lE2")
        templatesMagasins = ct.templatesOption("lM")
        templatesClients = ct.templatesOption("lC")

        userDateDebut = dateDe + " " + timeDe
        userDateDebut = dt.strptime(userDateDebut, "%Y-%m-%d %H:%M")
        userDateFin = dateA + " " + timeA
        userDateFin = dt.strptime(userDateFin, "%Y-%m-%d %H:%M")
        if not userDateDebut <= userDateFin:
            dataInfo = "<h1 style=\"color:orange\">Erreur de saisie</h1>"
            div = "<h2>La date de début est supérieure à la date de fin</h2>"
        else:

            # Utiliser la fonction dans SI
            data, dataInfo = SI.nbPers_listes(site, dateDe, dateA, "", "Horodatage Sortie", timeDe, timeA, "")

            if not data:
                div = "<div align=\"center\" style=\"color:orange\"><h2> Pas d'intervenants pendant l'heure d'entrée </h2></div>"
            else:
                titre = "<h2>Intervenants selon heure de sortie<h2>"
                dataInfo = titre + dataInfo

                dicContrat, dicEntrep, dicSpec, dicEntree, dicSortie, dicTemps = SI.statistique_intervention(data)
                getX, getY, getZ, dataInfo = ct.traitement(dicContrat, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script1, div1 = ct.controleur("Nb de personnes présentées selon nature du contrat", getX, getY, getZ,
                                              'Nature du contrat', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicEntrep, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script2, div2 = ct.controleur("Nb de personnes présentées selon entreprise", getX, getY, getZ,
                                              'Entreprise', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicSpec, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script3, div3 = ct.controleur("Nb de personnes présentées selon spécialité", getX, getY, getZ,
                                              'Spécialité', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicEntree, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script4, div4 = ct.controleur("Nb de personnes présentées selon heure d'entrée", getX, getY, getZ,
                                              'Heure d\'entrée', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicSortie, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script5, div5 = ct.controleur("Nb de personnes présentées selon heure de sortie", getX, getY, getZ,
                                              'Heure de sortie', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicTemps, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script6, div6 = ct.controleur("Nb de personnes présentées selon le temps de présence", getX, getY, getZ,
                                              'Temps de présence', 'NbPers', "NbPers", "blue")

                tableInfo = ct.intervenants_Info(data)
                div = script1 + div1 + script2 + div2 + script3 + div3 + script4 + div4 + script5 + div5 + script6 + div6 + tableInfo

        template = env.get_template('WebApp.html')
        return template.render(entreprise=templatesEntreprises, specialite=templatesSpecialites,
                               intervenant=templatesIntervenants,
                               entreprise2=templatesEntreprises2, magasin=templatesMagasins, client=templatesClients,
                               infomation=dataInfo, divforBokeh=div)


    @cherrypy.expose
    #10- Statistique des intervenants par temps de présence
    def type10(self, site, dateDe, dateA, temps):
        templatesEntreprises = ct.templatesOption("lE")
        templatesSpecialites = ct.templatesOption("lS")
        templatesIntervenants = ct.templatesOption("lN")
        templatesEntreprises2 = ct.templatesOption("lE2")
        templatesMagasins = ct.templatesOption("lM")
        templatesClients = ct.templatesOption("lC")

        userDateDebut = dateDe + " " + "00:00"
        userDateDebut = dt.strptime(userDateDebut, "%Y-%m-%d %H:%M")
        userDateFin = dateA + " " + "23:59"
        userDateFin = dt.strptime(userDateFin, "%Y-%m-%d %H:%M")
        if not userDateDebut <= userDateFin:
            dataInfo = "<h1 style=\"color:orange\">Erreur de saisie</h1>"
            div = "<h2>La date de début est supérieure à la date de fin</h2>"
        else:

            # Utiliser la fonction dans SI
            data, dataInfo = SI.nbPers_listes(site, dateDe, dateA, "", "", "", "", temps)


            if not data:
                div = "<div align=\"center\" style=\"color:orange\"><h2> Pas d'intervenants pour le temps de présence </h2></div>"
            else:
                titre = "<h2>Intervenants selon temps de présence<h2>"
                dataInfo = titre + dataInfo

                dicContrat, dicEntrep, dicSpec, dicEntree, dicSortie, dicTemps = SI.statistique_intervention(data)
                getX, getY, getZ, dataInfo = ct.traitement(dicContrat, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script1, div1 = ct.controleur("Nb de personnes présentées selon nature du contrat", getX, getY, getZ,
                                              'Nature du contrat', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicEntrep, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script2, div2 = ct.controleur("Nb de personnes présentées selon entreprise", getX, getY, getZ,
                                              'Entreprise', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicSpec, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script3, div3 = ct.controleur("Nb de personnes présentées selon spécialité", getX, getY, getZ,
                                              'Spécialité', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicEntree, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script4, div4 = ct.controleur("Nb de personnes présentées selon heure d'entrée", getX, getY, getZ,
                                              'Heure d\'entrée', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicSortie, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script5, div5 = ct.controleur("Nb de personnes présentées selon heure de sortie", getX, getY, getZ,
                                              'Heure de sortie', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicTemps, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script6, div6 = ct.controleur("Nb de personnes présentées selon le temps de présence", getX, getY, getZ,
                                              'Temps de présence', 'NbPers', "NbPers", "blue")

                tableInfo = ct.intervenants_Info(data)
                div = script1 + div1 + script2 + div2 + script3 + div3 + script4 + div4 + script5 + div5 + script6 + div6 + tableInfo

        template = env.get_template('WebApp.html')
        return template.render(entreprise=templatesEntreprises, specialite=templatesSpecialites,
                               intervenant=templatesIntervenants,
                               entreprise2=templatesEntreprises2, magasin=templatesMagasins, client=templatesClients,
                               infomation=dataInfo, divforBokeh=div)

    @cherrypy.expose
    #11- Statistique des intervenants par date donnée
    def type11(self, site, dateDe, dateA):
        templatesEntreprises = ct.templatesOption("lE")
        templatesSpecialites = ct.templatesOption("lS")
        templatesIntervenants = ct.templatesOption("lN")
        templatesEntreprises2 = ct.templatesOption("lE2")
        templatesMagasins = ct.templatesOption("lM")
        templatesClients = ct.templatesOption("lC")

        userDateDebut = dateDe + " " + "00:00"
        userDateDebut = dt.strptime(userDateDebut, "%Y-%m-%d %H:%M")
        userDateFin = dateA + " " + "23:59"
        userDateFin = dt.strptime(userDateFin, "%Y-%m-%d %H:%M")
        if not userDateDebut <= userDateFin:
            dataInfo = "<h1 style=\"color:orange\">Erreur de saisie</h1>"
            div = "<h2>La date de début est supérieure à la date de fin</h2>"
        else:

            # Utiliser la fonction dans SI
            data, dataInfo = SI.recherche_Intervenant(site, dateDe, dateA, "")

            if not data:
                div = data+"<div align=\"center\" style=\"color:orange\"><h2> Pas d'intervenants pendant ces deux dates </h2></div>"
            else:
                titre = "<h2>Intervenants selon date donnée<h2>"
                dataInfo = titre + dataInfo

                dicContrat, dicEntrep, dicSpec, dicEntree, dicSortie, dicTemps = SI.statistique_intervention(data)
                getX, getY, getZ, dataInfo = ct.traitement(dicContrat, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script1, div1 = ct.controleur("Nb de personnes présentées selon nature du contrat", getX, getY, getZ,
                                              'Nature du contrat', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicEntrep, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script2, div2 = ct.controleur("Nb de personnes présentées selon entreprise", getX, getY, getZ,
                                              'Entreprise', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicSpec, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script3, div3 = ct.controleur("Nb de personnes présentées selon spécialité", getX, getY, getZ,
                                              'Spécialité', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicEntree, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script4, div4 = ct.controleur("Nb de personnes présentées selon heure d'entrée", getX, getY, getZ,
                                              'Heure d\'entrée', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicSortie, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script5, div5 = ct.controleur("Nb de personnes présentées selon heure de sortie", getX, getY, getZ,
                                              'Heure de sortie', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicTemps, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script6, div6 = ct.controleur("Nb de personnes présentées selon le temps de présence", getX, getY, getZ,
                                              'Temps de présence', 'NbPers', "NbPers", "blue")

                tableInfo = ct.intervenants_Info(data)
                div = script1 + div1 + script2 + div2 + script3 + div3 + script4 + div4 + script5 + div5 + script6 + div6 + tableInfo

        template = env.get_template('WebApp.html')
        return template.render(entreprise=templatesEntreprises, specialite=templatesSpecialites,
                               intervenant=templatesIntervenants,
                               entreprise2=templatesEntreprises2, magasin=templatesMagasins, client=templatesClients,
                               infomation=dataInfo, divforBokeh=div)

    @cherrypy.expose
    #12- Rechercher un intervenant
    def type12(self, site, dateDe, dateA, intervenant):
        templatesEntreprises = ct.templatesOption("lE")
        templatesSpecialites = ct.templatesOption("lS")
        templatesIntervenants = ct.templatesOption("lN")
        templatesEntreprises2 = ct.templatesOption("lE2")
        templatesMagasins = ct.templatesOption("lM")
        templatesClients = ct.templatesOption("lC")

        userDateDebut = dateDe + " " + "00:00"
        userDateDebut = dt.strptime(userDateDebut, "%Y-%m-%d %H:%M")
        userDateFin = dateA + " " + "23:59"
        userDateFin = dt.strptime(userDateFin, "%Y-%m-%d %H:%M")
        if not userDateDebut <= userDateFin:
            dataInfo = "<h1 style=\"color:orange\">Erreur de saisie</h1>"
            div = "<h2>La date de début est supérieure à la date de fin</h2>"
        else:

            # Utiliser la fonction dans SI
            data, dataInfo = SI.recherche_Intervenant(site, dateDe, dateA, intervenant)

            if not data:
                div = data + "<div align=\"center\" style=\"color:orange\"><h2> Pas de cet intervenant </h2></div>"
            else:
                titre = "<h2>Recherche d'intervenant<h2>"
                dataInfo = titre + dataInfo

                dicContrat, dicEntrep, dicSpec, dicEntree, dicSortie, dicTemps = SI.statistique_intervention(data)
                getX, getY, getZ, dataInfo = ct.traitement(dicContrat, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script1, div1 = ct.controleur("Nb de personnes présentées selon nature du contrat", getX, getY, getZ,
                                              'Nature du contrat', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicEntrep, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script2, div2 = ct.controleur("Nb de personnes présentées selon entreprise", getX, getY, getZ,
                                              'Entreprise', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicSpec, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script3, div3 = ct.controleur("Nb de personnes présentées selon spécialité", getX, getY, getZ,
                                             'Spécialité', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicEntree, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script4, div4 = ct.controleur("Nb de personnes présentées selon heure d'entrée", getX, getY, getZ,
                                              'Heure d\'entrée', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicSortie, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script5, div5 = ct.controleur("Nb de personnes présentées selon heure de sortie", getX, getY, getZ,
                                              'Heure de sortie', 'NbPers', "NbPers", "blue")

                getX, getY, getZ, dataInfo = ct.traitement(dicTemps, dataInfo)
                # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
                script6, div6 = ct.controleur("Nb de personnes présentées selon le temps de présence", getX, getY, getZ,
                                              'Temps de présence', 'NbPers', "NbPers", "blue")

                tableInfo = ct.intervenants_Info(data)
                div = script1 + div1 + script2 + div2 + script3 + div3 + script4 + div4 + script5 + div5 + script6 + div6 + tableInfo

        template = env.get_template('WebApp.html')
        return template.render(entreprise=templatesEntreprises, specialite=templatesSpecialites,
                               intervenant=templatesIntervenants,
                               entreprise2=templatesEntreprises2, magasin=templatesMagasins, client=templatesClients,
                               infomation=dataInfo, divforBokeh=div)


    @cherrypy.expose
    # 20-Nb de sorties d'outils selon horaire
    def type20(self, site, dateDe, dateA, timeDe, timeA):
        templatesEntreprises = ct.templatesOption("lE")
        templatesSpecialites = ct.templatesOption("lS")
        templatesIntervenants = ct.templatesOption("lN")
        templatesEntreprises2 = ct.templatesOption("lE2")
        templatesMagasins = ct.templatesOption("lM")
        templatesClients = ct.templatesOption("lC")
        
        # Utiliser la fonction dans SO
        data, dataInfo = SO.nbOutils_HorairePeriode(site, dateDe, timeDe, dateA, timeA, "60")
        getX, getY, getZ, dataInfo = ct.traitement(data, dataInfo)
        # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
        script, div = ct.controleur("Nb de sorties d'outils selon horaire", getX, getY, getZ, 'Datetime', 'NbOutils', "NbOutils", "blue")
        template = env.get_template('WebApp.html')
        return template.render(entreprise2=templatesEntreprises2, magasin=templatesMagasins, client=templatesClients,
                               entreprise=templatesEntreprises, specialite=templatesSpecialites, intervenant=templatesIntervenants,
                               infomation=dataInfo, divforBokeh=script + div)

    @cherrypy.expose
    #21-Nb d'outils délivrés au guichet selon horaire et période
    def type21(self, site, dateDe, dateA, timeDe, timeA, periode):
        templatesEntreprises = ct.templatesOption("lE")
        templatesSpecialites = ct.templatesOption("lS")
        templatesIntervenants = ct.templatesOption("lN")
        templatesEntreprises2 = ct.templatesOption("lE2")
        templatesMagasins = ct.templatesOption("lM")
        templatesClients = ct.templatesOption("lC")
        
        #Utiliser la fonction dans SO
        data, dataInfo = SO.nbEmprunts_HorairePeriode(site, dateDe, timeDe, dateA, timeA, periode, "EMPCLI", "TYPE_MOUVEMENT")
        getX, getY, getZ, dataInfo = ct.traitement(data, dataInfo)
        #controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
        script, div = ct.controleur("Nb d'outils délivrés au guichet selon horaire et période", getX, getY, getZ, 'Datetime', 'NbOutils', "NbOutils", "blue")
        template = env.get_template('WebApp.html')
        return template.render(entreprise2=templatesEntreprises2, magasin=templatesMagasins, client=templatesClients,
                               entreprise=templatesEntreprises, specialite=templatesSpecialites,
                               intervenant=templatesIntervenants,
                               infomation=dataInfo, divforBokeh=script + div)
    @cherrypy.expose
    # 22-Nb de clients servis (dont prolongations d'emprunt)
    def type22(self, site, dateDe, dateA, timeDe, timeA, periode):
        templatesEntreprises = ct.templatesOption("lE")
        templatesSpecialites = ct.templatesOption("lS")
        templatesIntervenants = ct.templatesOption("lN")
        templatesEntreprises2 = ct.templatesOption("lE2")
        templatesMagasins = ct.templatesOption("lM")
        templatesClients = ct.templatesOption("lC")
        
        # Utiliser la fonction dans SO
        data, dataInfo = SO.nbOutils_User3(site, dateDe, timeDe, dateA, timeA, periode, "EMPCLI", "PROEMP", "TYPE_MOUVEMENT", "", "")
        getX, getY, getZ, dataInfo = ct.traitement(data, dataInfo)
        # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
        script, div = ct.controleur("Nb de clients servis y compris prolongés", getX, getY, getZ, 'Datetime', 'NbClientsServis', "NbCLientsServis", "blue")
        template = env.get_template('WebApp.html')
        return template.render(entreprise2=templatesEntreprises2, magasin=templatesMagasins, client=templatesClients,
                               entreprise=templatesEntreprises, specialite=templatesSpecialites, intervenant=templatesIntervenants,
                               infomation=dataInfo, divforBokeh=script + div)
    @cherrypy.expose
    # 23-Nb de sorties pour anomalie selon horaire
    def type23(self, site, dateDe, dateA, timeDe, timeA):
        templatesEntreprises = ct.templatesOption("lE")
        templatesSpecialites = ct.templatesOption("lS")
        templatesIntervenants = ct.templatesOption("lN")
        templatesEntreprises2 = ct.templatesOption("lE2")
        templatesMagasins = ct.templatesOption("lM")
        templatesClients = ct.templatesOption("lC")
        # Utiliser la fonction dans SO
        data, dataInfo = SO.nbEmprunts_HorairePeriode(site, dateDe, timeDe, dateA, timeA, "60", "SORANO", "TYPE_MOUVEMENT")
        getX, getY, getZ, dataInfo = ct.traitement(data, dataInfo)
        # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
        script, div = ct.controleur("Nb de sorties pour anomalie selon horaire", getX, getY, getZ, 'Datetime', 'NbAnomalies', "NbAnomalies", "blue")
        template = env.get_template('WebApp.html')
        return template.render(entreprise2=templatesEntreprises2, magasin=templatesMagasins, client=templatesClients,
                               entreprise=templatesEntreprises, specialite=templatesSpecialites, intervenant=templatesIntervenants,
                               infomation=dataInfo, divforBokeh=script + div)
    @cherrypy.expose
    #24-Nb de rebus selon horaire
    def type24(self, site, dateDe, dateA, timeDe, timeA):
        templatesEntreprises = ct.templatesOption("lE")
        templatesSpecialites = ct.templatesOption("lS")
        templatesIntervenants = ct.templatesOption("lN")
        templatesEntreprises2 = ct.templatesOption("lE2")
        templatesMagasins = ct.templatesOption("lM")
        templatesClients = ct.templatesOption("lC")

        # Utiliser la fonction dans SO
        data, dataInfo = SO.nbEmprunts_HorairePeriode(site, dateDe, timeDe, dateA, timeA, "60", "REBUT", "TYPE_MOUVEMENT")
        getX, getY, getZ, dataInfo = ct.traitement(data, dataInfo)
        # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
        script, div = ct.controleur("Nb de rebus selon horaire", getX, getY, getZ, 'Datetime', 'NbRebus', "NbRebus", "blue")
        template = env.get_template('WebApp.html')
        return template.render(entreprise2=templatesEntreprises2, magasin=templatesMagasins, client=templatesClients,
                               entreprise=templatesEntreprises, specialite=templatesSpecialites,
                               intervenant=templatesIntervenants,
                               infomation=dataInfo, divforBokeh=script + div)
    @cherrypy.expose
    #25-Nb de mouvements selon magasin
    def type25(self, site, dateDe, timeDe, dateA, timeA, periode, magasin):
        templatesEntreprises = ct.templatesOption("lE")
        templatesSpecialites = ct.templatesOption("lS")
        templatesIntervenants = ct.templatesOption("lN")
        templatesEntreprises2 = ct.templatesOption("lE2")
        templatesMagasins = ct.templatesOption("lM")
        templatesClients = ct.templatesOption("lC")

        # Utiliser la fonction dans SO
        data, dataInfo = SO.nbOutils_User(site, dateDe, timeDe, dateA, timeA, periode, magasin, "CODE")
        getX, getY, getZ, dataInfo = ct.traitement(data, dataInfo)
        # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
        script, div = ct.controleur("Nb de mouvements selon magasin", getX, getY, getZ, 'Magasin', 'NbMouvements', "NbMouvements", "blue")
        template = env.get_template('WebApp.html')
        return template.render(entreprise2=templatesEntreprises2, magasin=templatesMagasins, client=templatesClients,
                               entreprise=templatesEntreprises, specialite=templatesSpecialites,
                               intervenant=templatesIntervenants,
                               infomation=dataInfo, divforBokeh=script + div)
    @cherrypy.expose
    # 26-Nb de rebus/sorties pour anomalie selon magasin
    def type26(self, site, dateDe, timeDe, dateA, timeA, magasin):
        templatesEntreprises = ct.templatesOption("lE")
        templatesSpecialites = ct.templatesOption("lS")
        templatesIntervenants = ct.templatesOption("lN")
        templatesEntreprises2 = ct.templatesOption("lE2")
        templatesMagasins = ct.templatesOption("lM")
        templatesClients = ct.templatesOption("lC")
        # Utiliser la fonction dans SO
        data, dataInfo = SO.nbOutils_User3(site, dateDe, timeDe, dateA, timeA, "60", "SORANO", "REBUT", "TYPE_MOUVEMENT", magasin, "CODE")
        getX, getY, getZ, dataInfo = ct.traitement(data, dataInfo)
        # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
        script, div = ct.controleur("Nb de rebus/anomalies selon magasin", getX, getY, getZ, 'Magasin', 'NbDefauts', "NbDefauts", "blue")
        template = env.get_template('WebApp.html')
        return template.render(entreprise2=templatesEntreprises2, magasin=templatesMagasins, client=templatesClients,
                               entreprise=templatesEntreprises, specialite=templatesSpecialites,
                               intervenant=templatesIntervenants,
                               infomation=dataInfo, divforBokeh=script + div)
    @cherrypy.expose
    # 27-Nb d'emprunts selon client
    def type27(self, site, dateDe, timeDe, dateA, timeA, periode, client):
        templatesEntreprises = ct.templatesOption("lE")
        templatesSpecialites = ct.templatesOption("lS")
        templatesIntervenants = ct.templatesOption("lN")
        templatesEntreprises2 = ct.templatesOption("lE2")
        templatesMagasins = ct.templatesOption("lM")
        templatesClients = ct.templatesOption("lC")
        # Utiliser la fonction dans SO
        data, dataInfo = SO.nbOutils_User2(site, dateDe, timeDe, dateA, timeA, periode, "EMPCLI", "TYPE_MOUVEMENT", client, "UTILISATEUR")
        getX, getY, getZ, dataInfo = ct.traitement(data, dataInfo)
        # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
        script, div = ct.controleur("Nb d'emprunts selon client", getX, getY, getZ, 'Magasin', 'NbEmprunts', "NbEmprunts", "blue")
        template = env.get_template('WebApp.html')
        return template.render(entreprise2=templatesEntreprises2, magasin=templatesMagasins, client=templatesClients,
                               entreprise=templatesEntreprises, specialite=templatesSpecialites,
                               intervenant=templatesIntervenants,
                               infomation=dataInfo, divforBokeh=script + div)
    @cherrypy.expose
    # 28-Nb de mouvements selon entreprise
    def type28(self, site, dateDe, timeDe, dateA, timeA, entreprise2):
        templatesEntreprises = ct.templatesOption("lE")
        templatesSpecialites = ct.templatesOption("lS")
        templatesIntervenants = ct.templatesOption("lN")
        templatesEntreprises2 = ct.templatesOption("lE2")
        templatesMagasins = ct.templatesOption("lM")
        templatesClients = ct.templatesOption("lC")
        # Utiliser la fonction dans SO
        data, dataInfo = SO.nbOutils_User(site, dateDe, timeDe, dateA, timeA, "60", entreprise2, "BNU")
        getX, getY, getZ, dataInfo = ct.traitement(data, dataInfo)
        # controleur(titre, dataX, dataY, dataLabel, x_axis_label, y_axis_label, legend, color)
        script, div = ct.controleur("Nb de mouvements selon entreprise", getX, getY, getZ, 'Entreprise', 'NbMouvements', "NbMouvements", "blue")
        template = env.get_template('WebApp.html')
        return template.render(entreprise2=templatesEntreprises2, magasin=templatesMagasins, client=templatesClients,
                               entreprise=templatesEntreprises, specialite=templatesSpecialites,
                               intervenant=templatesIntervenants,
                               infomation=dataInfo, divforBokeh=script + div)

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/Templates': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './Templates/'
        },
        '/Templates/images': {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": 'Templates/images/'
        }
    }
    cherrypy.quickstart(uranium(), '/', conf)