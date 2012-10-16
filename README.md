# Autosave for IPython Notebook

## Extension for managing periodic autosave of IPython notebooks

install the extension:

    %install_ext https://raw.github.com/minrk/autosave_ipython/master/autosave.py

load the extension:

    %load_ext autosave

autosave every 30 seconds:

    %autosave 30

disable autosave:

    %autosave 0

trigger save from Python:

    %savenb

