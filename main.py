import os
import numpy as np
from matplotlib import image

"""
    To get the name of the file, without extension
"""
def get_protname(prot_file):
    protname_with_ext = prot_file
    protname = '.'.join(protname_with_ext.split('.')[:-1])
    return protname

"""
    To get the name of the antigene chain (in the pdb file)
"""
def get_antiname(protein_folder_path, protname):
    labelId = 0
    chain_arg = []
    prot_path = protein_folder_path + protname + '.pdb'
    with open(prot_path, 'r') as file:
        for line in file:
            if 'LABEL' in line:
                labelId = line.find('LABEL')
            elif labelId != 0 and 'CHAIN' in line and len(chain_arg) < 3:
                chain_arg.append(line[labelId])
    antiname = ''
    for letter in chain_arg:
        if 'L' != letter and 'H' != letter:
            antiname = letter
    return antiname

"""
    Creates a file protname.csv that contains only the two 
    chains of the antibody, oriented in the correct way
"""
def orientor(protein_folder_path, r_path, bscoord_path, protname):
    antiname = get_antiname(protein_folder_path,protname)
    args = protein_folder_path + protname + '.pdb' + ' L,H ' + antiname + ' 10 10 100 100 ' + protname + '.csv'
    os.system(r_path + ' ' + bscoord_path + ' ' + args)

"""
    Creates a PDB file that only contains the chains LH and H
"""
def selector(protein_folder_path, r_path, selectChains_path, protname):
    args = protein_folder_path + protname + '.pdb' + ' --chain L,H --outfile ' + protname + '.pdb'
    os.system(r_path + ' ' + selectChains_path + ' ' + args)

"""
    Creates a csv files that contains the values of the potentials
"""
def apbs(csv_folder_path, apbs_path, apbs_multivalue_path, protname):
    #creates protname.in
    os.system('pdb2pqr30 --ff=AMBER --apbs-input ' + protname + '.in ' + protname + '.pdb ' + protname + '.pqr')
    #creates protname.pqr.dx
    os.system(apbs_path + ' ' + protname + '.in')
    #creates protname_pot.csv, saves it in the dedicated folder
    os.system(apbs_multivalue_path + ' ' + protname + '.csv ' + protname + '.pqr.dx ' + csv_folder_path + protname + '_pot.csv')

"""
    Creates and image from the csv data
"""
def save_img(csv_folder_path,img_folder_path,protname):
    my_data = np.genfromtxt(csv_folder_path + protname + '_pot.csv', delimiter=',')
    my_data_new = np.reshape(my_data[:,3],(100,100))
    image.imsave(img_folder_path+protname+'.png', my_data_new, cmap='gray')

"""
    Clears the main folder of the files created during the data preparation
"""
def trash(protname):
    os.remove(protname+'.csv')
    os.remove(protname+'.in')
    os.remove(protname+'.log')
    os.remove(protname+'.pdb')
    os.remove(protname+'.pqr')
    os.remove(protname+'.pqr.dx')
    os.remove('io.mc')

"""
    The place where you can change the paths
"""
protein_folder_path = 'C:/Users/chadm/Desktop/PT/proteins/'
csv_folder_path = 'C:/Users/chadm/Desktop/PT/2prog/csv/'
img_folder_path = 'C:/Users/chadm/Desktop/PT/2prog/images/'
apbs_path = 'C:/Users/chadm/Downloads/APBS-3.0.0_Windows/APBS-3.0.0_Windows/bin/apbs.exe'
apbs_multivalue_path = 'C:/Users/chadm/Downloads/APBS-3.0.0_Windows/APBS-3.0.0_Windows/share/apbs/tools/bin/Release/multivalue.exe'
r_path = '"C:/Program Files/R/R-3.6.1/bin/Rscript.exe"'
bscoord_path = 'C:/Users/chadm/Desktop/PT/2prog/bscoord.R'
selectChains_path = 'C:/Users/chadm/Desktop/PT/2prog/selectChains.R'

"""
    The main part of the code
"""
for prot_file in os.listdir(protein_folder_path) :
    protname = get_protname(prot_file)
    orientor(protein_folder_path, r_path, bscoord_path , protname)
    selector(protein_folder_path, r_path, selectChains_path, protname)
    apbs(csv_folder_path, apbs_path, apbs_multivalue_path, protname)
    save_img(csv_folder_path,img_folder_path,protname)
    trash(protname)
