import os
import shutil
import re
import PyPDF2
import datetime
import msvcrt

fichier_source = input("Entrez la source du fichier ")

x = datetime.datetime.now()


# Extraire acronyme du fichier
nom_fichier = "./copie.Luc-Sarrazin.pdf"
acronyme1 = re.search(r'\.(\w)', fichier_source).group(1)
acronyme2 = re.search(r'\.(\w+)-(\w+)', fichier_source).group(2)
acronyme = str(acronyme1)+str(acronyme2)
print("Acronyme = " + acronyme)


# Trouver et copier un fichier
destination = 'C:/Users/User/Desktop/Python/corrigé/'
destinationEleves = 'C:/Users/User/Desktop/Python/corrigé/' + acronyme
acronyme3 = acronyme + " corrigé " + x.strftime("%Y-%m-%d") + ".pdf"
print("Acronyme 3 = " + acronyme3)
destinationFinal = os.path.join(destinationEleves, acronyme3)
shutil.copy(fichier_source, destinationFinal)



# Ouvrir le PDF
with open(fichier_source, 'rb') as fichier_pdf:
    lecteur_pdf = PyPDF2.PdfReader(fichier_pdf)
    page = lecteur_pdf.pages[0]
    texte = page.extract_text()
    notes = re.findall(r'(\d+)\s*/\s*(\d+)', texte)

print(texte)  # Affiche le texte extrait du PDF

print(notes)

destinationEleves = os.path.join('C:/Users/User/Desktop/Python/corrigé', acronyme)
file_path = os.path.join(destinationEleves, acronyme + " résumé des notes " + x.strftime("%Y-%m-%d") + ".txt")
with open(file_path, 'w') as file:
    file.write("Partie fermee : " + str(notes[0][0]) + " / " + str(notes[0][1]) + "\n" + " Partie Ouverte : " + str(notes[1][0]) + " / " + str(notes[1][1]) + "\n" + " Bilan : " + str(notes[2][0]) + " / " + str(notes[2][1]) + "\n")

print("")
print("Appuyez sur n'importe quelle touche pour quitter la console...")
msvcrt.getch()