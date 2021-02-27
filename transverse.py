@author Aidan Bonnefond
@author Charlotte des Mares de Trebons
@author Damien Monseur
@author Romain Labrosse

from Bio.PDB import PDBParser
parser = PDBParser()
prot_id = "1A2Y"
prot_file = "1A2Y.pdb"
structure = parser.get_structure(prot_id, prot_file)
