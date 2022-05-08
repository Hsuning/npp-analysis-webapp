import pandas as pd
import glob


def BasedeDonneeTwo():
    #Fonction pour lire tous les fichiers csv dans un DataFrame
    path = r'./Fichier_outillage'
    allFiles = glob.glob(path + "/*.csv")
    frame = pd.DataFrame()
    liste = []
    for file in allFiles:
        df = pd.read_csv(file,index_col=None, sep=',', header=0)
        liste.append(df)
    BDD_Outillage = pd.concat(liste)
    return BDD_Outillage


def listederoulante(BDD2):
    listeEntreprise = []
    listeClient = []
    listeMagasin = []
    for i in range(0, len(BDD2)):
        magasin = BDD2.iloc[i]["CODE"]
        client = BDD2.iloc[i]["UTILISATEUR"]
        entreprise = BDD2.iloc[i]["BNU"]
        if magasin not in listeMagasin:
            listeMagasin.append(magasin)
        if client not in listeClient:
            listeClient.append(client)
        if entreprise not in listeEntreprise:
            listeEntreprise.append(entreprise)
    listeMagasin.sort()
    listeClient.sort()
    listeEntreprise.sort()
    return listeMagasin, listeClient, listeEntreprise