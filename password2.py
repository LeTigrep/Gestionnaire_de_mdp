import secrets
import string
import json
import tkinter as tk
from tkinter import messagebox
import pyperclip 

FICHIER_MDP = "mots_de_passe.json"

def generer_mot_de_passe(longueur=12):

    caracteres = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    caracteres_ambigus = 'l1O0'
    caracteres = ''.join(c for c in caracteres if c not in caracteres_ambigus)
    mot_de_passe = ''.join(secrets.choice(caracteres) for _ in range(longueur))
    return mot_de_passe


def valider_mot_de_passe(mot_de_passe):
    if len(mot_de_passe) < 8:
        return False, "Le mot de passe doit contenir au moins 8 caractères."
    if not any(c.islower() for c in mot_de_passe):
        return False, "Le mot de passe doit contenir au moins une lettre minuscule."
    if not any(c.isupper() for c in mot_de_passe):
        return False, "Le mot de passe doit contenir au moins une lettre majuscule."
    if not any(c.isdigit() for c in mot_de_passe):
        return False, "Le mot de passe doit contenir au moins un chiffre."
    if not any(c in string.punctuation for c in mot_de_passe):
        return False, "Le mot de passe doit contenir au moins un caractère spécial."
    return True, ""


def charger_mots_de_passe():
    try:
        with open(FICHIER_MDP, 'r') as file:
            mots_de_passe = json.load(file)
    except FileNotFoundError:
        mots_de_passe = {}
    return mots_de_passe


def sauvegarder_mots_de_passe(mots_de_passe):
    try:
        with open(FICHIER_MDP, 'w') as file:
            json.dump(mots_de_passe, file, indent=4)
    except IOError as e:
        messagebox.showerror("Erreur de fichier", f"Une erreur est survenue lors de la sauvegarde : {e}")


def ajouter_mot_de_passe(site, identifiant, mot_de_passe):
    mots_de_passe = charger_mots_de_passe()
    mots_de_passe[site] = {'identifiant': identifiant, 'mot_de_passe': mot_de_passe}
    sauvegarder_mots_de_passe(mots_de_passe)


# Classe pour gérer l'interface utilisateur
class GestionnaireMotsDePasse:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Mots de Passe")
        
        # Interface pour le site
        
        self.label_site = tk.Label(root, text="Site:")
        self.label_site.grid(row=0, column=0, padx=10, pady=10)
        self.entree_site = tk.Entry(root)
        self.entree_site.grid(row=0, column=1, padx=10, pady=10)

        # Interface pour l'identifiant
        
        self.label_identifiant = tk.Label(root, text="Identifiant:")
        self.label_identifiant.grid(row=1, column=0, padx=10, pady=10)
        self.entree_identifiant = tk.Entry(root)
        self.entree_identifiant.grid(row=1, column=1, padx=10, pady=10)

        # Interface pour le mot de passe
        
        self.label_mot_de_passe = tk.Label(root, text="Mot de Passe:")
        self.label_mot_de_passe.grid(row=2, column=0, padx=10, pady=10)
        self.entree_mot_de_passe = tk.Entry(root)
        self.entree_mot_de_passe.grid(row=2, column=1, padx=10, pady=10)
        
        # Bouton pour générer un mot de passe
        
        self.bouton_generer = tk.Button(root, text="Générer un Mot de Passe", command=self.generer_mot_de_passe)
        self.bouton_generer.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        
        # Bouton pour ajouter le site et mot de passe
        
        self.bouton_ajouter = tk.Button(root, text="Ajouter le Mot de Passe", command=self.ajouter_mot_de_passe)
        self.bouton_ajouter.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        
        # Création de la zone de texte pour afficher les mots de passe enregistrés
        self.zone_mots_de_passe = tk.Text(root, height=10, width=40)
        self.zone_mots_de_passe.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        
       

        self.afficher_mots_de_passe()


    def ajouter_mot_de_passe(self):
        site = self.entree_site.get()
        identifiant = self.entree_identifiant.get()
        mot_de_passe = self.entree_mot_de_passe.get()
        
        est_valide, message_erreur = valider_mot_de_passe(mot_de_passe)
        
        if not est_valide:
            messagebox.showwarning("Erreur de mot de passe", message_erreur)
            return

        if site and identifiant and mot_de_passe:
            ajouter_mot_de_passe(site, identifiant, mot_de_passe)
            messagebox.showinfo("Succès", f"Mot de passe pour {site} ajouté !")
            self.entree_site.delete(0, tk.END)
            self.entree_identifiant.delete(0, tk.END)
            self.entree_mot_de_passe.delete(0, tk.END)
            self.afficher_mots_de_passe()
        else:
            messagebox.showwarning("Erreur de saisie", "Veuillez entrer un site, un identifiant et un mot de passe.")



    def copier_dans_presse_papier(self, texte):
        pyperclip.copy(texte)
        messagebox.showinfo("Copié", "Copié dans le presse-papier !")
    
    
    def generer_mot_de_passe(self):
        mot_de_passe = generer_mot_de_passe()  
        self.entree_mot_de_passe.delete(0, tk.END)  # Efface l'entrée de mot de passe actuelle
        self.entree_mot_de_passe.insert(0, mot_de_passe)
        
        
        
    def afficher_mots_de_passe(self):
        self.zone_mots_de_passe.delete(1.0, tk.END)  
        mots_de_passe = charger_mots_de_passe()  
        # Affiche chaque site et ses informations de connexion
        for site, infos in mots_de_passe.items():
            self.zone_mots_de_passe.insert(tk.END, f"Site: {site}\n")
            self.zone_mots_de_passe.insert(tk.END, f"Identifiant: {infos['identifiant']}\n")
            self.zone_mots_de_passe.insert(tk.END, f"Mot de Passe: {infos['mot_de_passe']}\n\n")


# Lancement 
if __name__ == "__main__":
    root = tk.Tk()
    app = GestionnaireMotsDePasse(root)
    root.mainloop()
