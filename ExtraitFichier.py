import os
import shutil
import re
import PyPDF2
import datetime
import msvcrt

# Demander la source du fichier
fichier_source = input("Entrez le chemin complet du fichier source : ")
if not os.path.isfile(fichier_source):
    print("Fichier introuvable. Vérifiez le chemin.")
    exit(1)

x = datetime.datetime.now()

# Extraire l'acronyme
match = re.search(r'\.(\w)\w*-(\w+)\.pdf$', fichier_source)
if match:
    initiale_prenom = match.group(1).upper()  # Première lettre du prénom en majuscule
    nom = match.group(2)  # Nom complet
    acronyme = initiale_prenom + nom  # LSarrazin
    print(f"Acronyme pour le répertoire : {acronyme}")
else:
    print("Nom de fichier invalide.")
    exit(1)

# Définir les destinations

destination_base = './corrigé/'
destination_repertoire = os.path.join(destination_base, acronyme)
os.makedirs(destination_repertoire, exist_ok=True)

'''
destination = './corrigé/'
destinationEleves = os.path.join(destination, acronyme)
acronyme3 = f"{acronyme} corrigé {x.strftime('%Y-%m-%d')}.pdf"
os.makedirs(destinationEleves, exist_ok=True)
destinationFinal = os.path.join(destinationEleves, acronyme3)
'''

x = datetime.datetime.now()
nom_fichier_copie = f"{acronyme} corrigé {x.strftime('%Y-%m-%d')}.pdf"
destination_fichier = os.path.join(destination_repertoire, nom_fichier_copie)

# Copier le fichier
shutil.copy(fichier_source, destination_fichier)
print(f"Fichier copié dans : {destination_fichier}")

# Copier le fichier
'''
shutil.copy(fichier_source, destinationFinal)
print(f"Fichier copié vers : {destinationFinal}")
'''

# Ouvrir et lire le PDF
try:
    with open(fichier_source, 'rb') as fichier_pdf:
        lecteur_pdf = PyPDF2.PdfReader(fichier_pdf)
        page = lecteur_pdf.pages[0]
        texte = page.extract_text() or "Aucun texte extrait. Vérifiez le PDF."
        print("Texte extrait du PDF :")
        print(texte)

        # Trouver les notes
        notes = re.findall(r'(\d+)\s*/\s*(\d+)', texte)
except Exception as e:
    print(f"Erreur lors de la lecture du PDF : {e}")
    exit(1)

# Enregistrer les notes
file_path = os.path.join(destination_repertoire, f"{acronyme} résumé des notes {x.strftime('%Y-%m-%d')}.txt")
with open(file_path, 'w') as file:
    try:
        file.write(f"Partie fermée : {notes[0][0]} / {notes[0][1]}\n")
        file.write(f"Partie ouverte : {notes[1][0]} / {notes[1][1]}\n")
        file.write(f"Bilan : {notes[2][0]} / {notes[2][1]}\n")
    except IndexError:
        file.write("Notes non trouvées ou format invalide.\n")

print("Notes enregistrées.")

# Pause avant de quitter
print("\nAppuyez sur n'importe quelle touche pour quitter la console...")
msvcrt.getch()
