# Import statement
import requests
import os
import re
import unicodecsv as csv
from bs4 import BeautifulSoup

# Used mostly to make it easier to generate the csv
class Enseignant(object):
	nom = ''
	image = ''
	departement = ''

	def __init__(self, nom, image, departement):
		self.nom = nom
		self.image = image
		self.departement = departement

# Used to clarify the code in general, makes it more readable and easier to understand. 
class Departement(object):
    nom = ''
    lien = ''
    enseignants = []

    # The class "constructor" - It's actually an initializer 
    def __init__(self, nom, lien):
        self.nom = nom
        self.lien = lien
        self.enseignants = []

departements = [
	Departement('informatique','https://informatique.cstjean.qc.ca/enseignants'),
	Departement('electronique','https://electronique.cstjean.qc.ca/enseignants'),
	Departement('architecture','http://architecture.cstjean.qc.ca/enseignants'),
	Departement('travail-social','https://travail-social.cstjean.qc.ca/enseignants'),
	Departement('genie-mecanique','https://genie-mecanique.cstjean.qc.ca/enseignants'),
	Departement('design-interieur','https://design-interieur.cstjean.qc.ca/enseignants'),
	Departement('comptabilite-gestion','https://comptabilite-gestion.cstjean.qc.ca/enseignants'),
	Departement('entreprise-agricole','https://entreprise-agricole.cstjean.qc.ca/enseignants'),
	Departement('gestion-commerce','https://commerces.cstjean.qc.ca/enseignants')
]

# Creation of the target directory
resultat_dir = 'resultat'
if not os.path.isdir(resultat_dir):
	os.mkdir(resultat_dir)

for departement in departements:
	
	# Find all the li with a class of fiche. Those elements contains information about a teacher in a departement
	reponse = requests.get(departement.lien)
	soup = BeautifulSoup(reponse.text, 'html.parser')
	
	# We itterate trough all the found teachers
	enseignants_html = soup.select('li.fiche')
	for enseignant_html in enseignants_html:
		# Parse the name of the teacher found in the dom tree
		nom_prof = ""
		nom_prof_html = enseignant_html.find('p' , 'title')
		if nom_prof_html:
			# Trim the excess text found in the p tag, could have used a regex but this does the job perfectly
			nom_prof = nom_prof_html.get_text() #Retrieve only the text
			nom_prof = nom_prof[:nom_prof.index("\n")] #Trim the text until we found a return line
		else:
			nom_prof = None
		
		# Parse the image of the teacher found in the dom tree
		image_prof = ""
		image_prof_html = enseignant_html.find('img', 'bg')
		if image_prof_html:
			image_prof = image_prof_html['src']
			image_response = requests.get(image_prof)
			
			# Create the directory to place the photo in
			if not os.path.isdir(os.path.join(resultat_dir, departement.nom)):
				os.mkdir(os.path.join(resultat_dir,departement.nom))
			
			# Create the file name and path to the file to write the image in
			image_file = nom_prof.replace(" ", "") + '.jpg'
			image_path = os.path.join(resultat_dir, departement.nom, image_file)
			
			# Write the content of the image inside the specified file
			with open(image_path , 'wb') as F:
				F.write(image_response.content)
		else:
			image_prof = None
		
		# We create a new teacher object and add it to the teachers array of the current department
		enseignant = Enseignant(nom_prof, image_prof, departement.nom)
		departement.enseignants.append(enseignant)

# Display all the informations gathered inside the console.
compteur = 0
for departement in departements: 
	for enseignant in departement.enseignants:
		compteur = compteur + 1
		print(str(compteur) + "::"+ str(enseignant.nom) + "::" + str(enseignant.departement) + "::" + str(enseignant.image))
print("Total::" + str(compteur))

# Generate the csv file
with open('resultat.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file, delimiter=';', encoding="utf-8-sig")
    for departement in departements:
    	for enseignant in departement.enseignants:
    		writer.writerow([str(enseignant.departement), str(enseignant.nom), str(enseignant.image)])