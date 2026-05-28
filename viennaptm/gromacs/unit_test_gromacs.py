import os
import numpy as np
from viennaptm.resources.aa_pdbs import fd_AXA

root_fd = os.path.join(os.getcwd(), 'test_gmx_emin')
os.makedirs(root_fd,  exist_ok=True)

aa1_3 = {"R":"arg","H":"his","K":"lys","D":"asp","E":"glu",
       "S":"ser","T":"thr","N":"asn","Q":"gln","C":"cys",
         "G":"gly","P":"pro","A":"ala","V":"val","I":"ile",
         "L":"leu","M":"met","F":"phe","Y":"tyr","W":"trp"}
aa3_1 = {}
for aa1 in aa1_3:
    aa3_1[aa1_3[aa1].upper()] = aa1
    aa1_3[aa1] = aa1_3[aa1].upper()

from viennaptm.modification.modification_library import ModificationLibrary
ml = ModificationLibrary()
for mod in ml.modifications:
    aa, mod = mod.residue_original_abbreviation, mod.residue_modified_abbreviation
    if len(mod)!=3:continue # this is wrong!
    mod_fd = os.path.join(root_fd, f'{aa}_{mod}')
    os.makedirs(mod_fd,  exist_ok=True)
    os.chdir(mod_fd)
    aa_1 = aa3_1[aa]
    pdb_input = os.path.join(fd_AXA, f'A{aa_1}A.pdb')
    viennaptm_comm = f'viennaptm --input {pdb_input} --modify " :3={mod}" --output testoutput.pdb  --gromacs.minimize True'
    os.system(viennaptm_comm)
    os.chdir('gmx_emin')
    os.system('echo 1 2 3 4 5 6 7 8 9 | gmx energy -f em')
    with open('energy.xvg') as f:
        for l in f:pass
        E = np.array(l.split(), dtype=float)
        assert E[1] < 20 # bond ene
        assert E[2] < 120 # ang ene
        assert E[3] < 120 # dih
        assert E[4] < 50 # imp
        #assert E[6] < 500 # 1-4
        if mod=='TOG':
            assert E[-1] < 50 # total
        else:
            assert E[-1] < -25 # total
    #break

