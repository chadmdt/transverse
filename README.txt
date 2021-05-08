###############################################################################
Pour main.py
Avoir un dossier qui contient les fichiers pdb, un qui contient les fichiers main.py,
bscoord.R et selectChains.R
Ne changer que les adresses à l'endroit indiqué dans le code, respecter celles qui
ont un '/' à la fin (mettre le '/' après votre adresse.

Le code ne fonctionne que pour les fichiers pdb contenant trois chaines, dont
deux nommées L et H.

###############################################################################
Pour eigenfaces.ipynb:

Il y a un fichier 'total.csv' et un dossier d'images bruitees qu'il faut
charger. Changez le chemin au début du notebook.

Le notebook prepare le csv pour y faire une analyse en composantes principales.
Il affiche en premier lieu les images des eigenfaces.
-> Probleme : il n'affiche qu'une seule image au lieu de 10.

Il fait ensuite le test avec l'image bruitee chargee.
L'image est importee en csv puis en numpy array. On lui applique une ACP.
On calcule la distance euclidienne entre la premiere ACP et la seconde.
-> Probleme : la distance euclidiennene fonctionne pas jusqu'au bout.