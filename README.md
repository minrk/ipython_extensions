# Miscellaneous IPython and Jupyter extensions

These extensions typically target master of IPython and/or Jupyter,
so may not always work on the latest stable releases.

You can install each extension individually, via copy, download, or symlink (below):

    ln -s $(pwd)/extensions/* $(ipython locate)/extensions
    ln -s $(pwd)/nbextensions/* $(ipython locate)/nbextensions

or you can link the extension directories into your IPython directories (what I do):

    ln -s $(pwd)/extensions $(ipython locate)/extensions
    ln -s $(pwd)/nbextensions $(ipython locate)/nbextensions

## Gist

Add a gist button to the notebook toolbar:

    $ jupyter nbextension install https://rawgithub.com/minrk/ipython_extensions/master/nbextensions/gist.js
    $ jupyter nbextension enable gist



## Table of Contents 

Generates floating table of contents inside your notebook from the heading cells.
Adds a button to the toolbar to toggle the floating table of contents.

install the extension:

    $ jupyter nbextension install --user https://rawgithub.com/minrk/ipython_extensions/master/nbextensions/toc.js
    $ curl -L https://rawgithub.com/minrk/ipython_extensions/master/nbextensions/toc.css > $(jupyter --data-dir)/nbextensions/toc.css
    $ jupyter nbextension enable toc


## Write and execute

This IPython Notebook magic writes the content of the cell to a specified .py file before executing it.
An identifier can be used when writing to the file, thus making it possible to overwrite previous iterations of the same code block. 
The use case for this extension is to export selected code from a Notebook for reuse through a .py file.

To install the extension use:

    %install_ext https://raw.githubusercontent.com/minrk/ipython_extensions/master/extensions/writeandexecute.py
Then load it with 

    %load_ext writeandexecute
