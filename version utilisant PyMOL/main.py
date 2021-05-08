"""Ne changer les adresses que dans la fonction prog
Le dossier proteines ne doit contenir que les proteines, et il sera vidé à la fin
Le dossier photos doit être vide au début
"""
import os

def photo(photo_folder_path,protein_folder_path):
    photo_list = os.listdir(photo_folder_path)
    protname = get_protname(protein_folder_path)
    #if no protein
    if (protname == 0):
        return 0
    #if first photo
    if(photo_list is None or not(photo_list)):
        cmd.save(photo_folder_path+'/'+protname+'.png')
        return 0
    #if not first photo = photo we really want to keep
    os.remove(protein_folder_path+'/'+protname+'.pdb')
    cmd.save(photo_folder_path+'/'+protname+'.png')

def get_protname(protein_folder_path):
    prot_list = os.listdir(protein_folder_path)
    if(prot_list is not None and not(prot_list)):
        return 0
    else:
        protname_with_ext = prot_list[0]
        protname = '.'.join(protname_with_ext.split('.')[:-1])
        return protname

def selector(protein_folder_path,prog_folder_path,protname):
    cmd.delete('all')
    cmd.load(protein_folder_path+'/'+protname+'.pdb')
    cmd.select('antibody_chains', 'chain L, chain H')
    cmd.save(prog_folder_path+'/'+protname+'.pdb', 'antibody_chains')
    cmd.delete('all')

def apbs(apbs_path,prog_folder_path,protname):
    os.system('cd ' + prog_folder_path)
    os.system('pdb2pqr30 --ff=AMBER --apbs-input result.in '+protname+'.pdb result.pqr')
    os.system(apbs_path+' result.in')

def slicer(prog_folder_path,protname):
    cmd.load('result.pqr.dx')
    cmd.run('slice.pml')

def trash(prog_folder_path,protname):
    os.remove('result.in')
    os.remove('result.log')
    os.remove(prog_folder_path + '/' + protname+'.pdb')
    os.remove('result.pqr')
    os.remove('result.pqr.dx')
    os.remove('io.mc')

def prog():
    prog_folder_path = 'C:/Users/chadm/Desktop/PT/prog'
    protein_folder_path = 'C:/Users/chadm/Desktop/PT/proteins'
    photo_folder_path = 'C:/Users/chadm/Desktop/PT/photos'
    apbs_path = 'C:/Users/chadm/Downloads/APBS-3.0.0_Windows/APBS-3.0.0_Windows/bin/apbs.exe'
    photo(photo_folder_path,protein_folder_path)
    protname = get_protname(protein_folder_path)
    if(protname == 0):
        print('ERROR : The folder is empty')
        return 1
    selector(protein_folder_path,prog_folder_path,protname)
    apbs(apbs_path,prog_folder_path,protname)
    slicer(prog_folder_path,protname)
    trash(prog_folder_path,protname)

cmd.extend('prog', prog)
