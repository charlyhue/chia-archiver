import glob

def get_plots(dirs):
    plots = []
    for d in dirs:
        plots = plots + glob.glob(d + "*.plot")
    return plots
