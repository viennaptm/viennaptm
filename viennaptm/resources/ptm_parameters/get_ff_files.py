import os
this_dir = os.path.split(__file__)[0]

def get_gmx_ff(ff='gromos54a8', destination_dir=None):
    fd_gmx = os.path.join(this_dir, 'ptm_parameters', 'GROMACS')
    fd_gmx = os.path.abspath(fd_gmx)
    if ff == 'gromos54a8':
        ff_dir_name = 'gromos54a8.ff'
        residuetypes_fname = "residuetypes.dat"
        if destination_dir is None:
            full_ff_dir_name = ff_dir_name
            full_residuetypes_fname = residuetypes_fname
        else:
            full_ff_dir_name = os.path.join(destination_dir, ff_dir_name)
            full_residuetypes_fname = os.path.join(destination_dir, residuetypes_fname)
        if not os.path.exists(full_ff_dir_name):
            os.symlink(os.path.join(fd_gmx, ff_dir_name), full_ff_dir_name)
        if not os.path.exists(full_residuetypes_fname):
            os.symlink(os.path.join(fd_gmx, residuetypes_fname), full_residuetypes_fname)
        return
    raise ValueError(f"Force field {ff} in file format {file_format} not supported.")

