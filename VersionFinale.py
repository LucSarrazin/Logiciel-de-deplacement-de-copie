import os
import shutil
import re
import datetime
import PyPDF2


def traiter_fichier(fichier_source, destination_base):
    try:
        # Extraire uniquement la première lettre du prénom et le nom complet
        match = re.search(r'\.(\w)\w*-(\w+)\.pdf$', fichier_source)
        if match:
            initiale_prenom = match.group(1).upper()  # Première lettre du prénom en majuscule
            nom = match.group(2)  # Nom complet
            acronyme = initiale_prenom + nom  # LSarrazin
            print(f"Traitement du fichier : {fichier_source}")
            print(f"Acronyme pour le répertoire : {acronyme}")
        else:
            print(f"Nom de fichier invalide : {fichier_source}")
            return

        # Créer le répertoire pour cet acronyme
        destination_repertoire = os.path.join(destination_base, acronyme)
        os.makedirs(destination_repertoire, exist_ok=True)

        # Copier le fichier dans le répertoire
        x = datetime.datetime.now()
        nom_fichier_copie = f"{acronyme} corrigé {x.strftime('%Y-%m-%d')}.pdf"
        destination_fichier = os.path.join(destination_repertoire, nom_fichier_copie)
        shutil.copy(fichier_source, destination_fichier)
        print(f"Fichier copié dans : {destination_fichier}")

        # Ouvrir et lire le PDF
        with open(fichier_source, 'rb') as fichier_pdf:
            lecteur_pdf = PyPDF2.PdfReader(fichier_pdf)
            page = lecteur_pdf.pages[0]
            texte = page.extract_text() or "Aucun texte extrait. Vérifiez le PDF."
            print("Texte extrait du PDF :")
            print(texte)

            # Trouver les notes
            notes = re.findall(r'(\d+)\s*/\s*(\d+)', texte)

        # Enregistrer les notes dans un fichier texte
        file_path = os.path.join(destination_repertoire, f"{acronyme} résumé des notes {x.strftime('%Y-%m-%d')}.txt")
        with open(file_path, 'w') as file:
            try:
                file.write(f"Partie fermée : {notes[0][0]} / {notes[0][1]}\n")
                file.write(f"Partie ouverte : {notes[1][0]} / {notes[1][1]}\n")
                file.write(f"Bilan : {notes[2][0]} / {notes[2][1]}\n")
            except IndexError:
                file.write("Notes non trouvées ou format invalide.\n")

        print("Notes enregistrées.")
        print("-" * 50)

    except Exception as e:
        print(f"Erreur lors du traitement du fichier {fichier_source} : {e}")


# Configuration
destination_base = r"\\SRV-AD-01\Perso_Etudiants"
# destination_base = './corrigés'

# Demander un fichier spécifique ou tout traiter dans le répertoire courant
fichier_source = input("Entrez le nom du fichier PDF (laissez vide pour traiter tout le répertoire) : ").strip()

if fichier_source:  # Si un fichier spécifique est donné
    if not os.path.isfile(fichier_source):
        print("Fichier introuvable. Vérifiez le chemin.")
    else:
        traiter_fichier(fichier_source, destination_base)
else:  # Sinon, traiter tous les fichiers PDF dans le répertoire courant
    print("Aucun fichier spécifié. Recherche des fichiers PDF dans le répertoire courant...")
    repertoire_courant = os.getcwd()
    fichiers_pdf = [f for f in os.listdir(repertoire_courant) if f.lower().endswith('.pdf')]

    if not fichiers_pdf:
        print("Aucun fichier PDF trouvé dans le répertoire courant.")
    else:
        for fichier in fichiers_pdf:
            chemin_fichier = os.path.join(repertoire_courant, fichier)
            traiter_fichier(chemin_fichier, destination_base)
