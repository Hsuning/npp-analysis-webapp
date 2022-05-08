import pandas as pd
import glob


def BasedeDonneeOne():
    #Fonction pour lire tous les fichiers csv dans un DataFrame
    path = r'./Fichier_interventions'
    allFiles = glob.glob(path + "/*.csv")
    frame = pd.DataFrame()
    liste = []
    for file in allFiles:
        df = pd.read_csv(file,index_col=None, sep=';', header=0)
        liste.append(df)
    BDD_Intervention = pd.concat(liste)
    return BDD_Intervention

def listederoulante(BDD1):
    listeEntreprise = []
    listeSpecialite = []
    listeMatricule = []
    for i in range(0, len(BDD1)):
        entreprise = BDD1.iloc[i]["Raison sociale"]
        specialite = BDD1.iloc[i]["Specialite"]
        matricule = BDD1.iloc[i]["Matricule"]
        if entreprise not in listeEntreprise:
            listeEntreprise.append(entreprise)
        if specialite not in listeSpecialite:
            listeSpecialite.append(specialite)
        if matricule not in listeMatricule:
            listeMatricule.append(matricule)
    listeEntreprise.sort()
    listeSpecialite.sort()
    listeMatricule.sort()
    return listeEntreprise, listeSpecialite, listeMatricule