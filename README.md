# Miscellaneous IPython extensions

These extensions target IPython master, so may not always work on the latest stable release of IPython.

You can install each extension individually, or you can link the extension directories
into your IPython directories (what I do):

    ln -s $(pwd)/extensions/* $(ipython locate)/extensions
    ln -s $(pwd)/nbextensions/* $(ipython locate)/nbextensions

## Gist

Add a gist button to the notebook toolbar:

    $ curl -L https://rawgithub.com/minrk/ipython_extensions/master/nbextensions/gist.js > $(ipython locate)/nbextensions/gist.js

and load it by adding to your custom.js, found in `$(ipython locate profile)/static/custom/custom.js`:

```javascript
IPython.load_extensions('gist');
```


## Retina Figures

Enable 2x display of matplotlib figures (no longer necessary on IPython master)

install the extension:

    %install_ext https://rawgithub.com/minrk/ipython_extensions/master/extensions/retina.py

load the extension:

    %load_ext retina

## Table of Contents 

Generates floating table of contents inside your notebook from the heading cells.
Adds a button to the toolbar to toggle the floating table of contents.

install the extension:

    $ curl -L https://rawgithub.com/minrk/ipython_extensions/master/nbextensions/toc.js > $(ipython locate)/nbextensions/toc.js
    $ curl -L https://rawgithub.com/minrk/ipython_extensions/master/nbextensions/toc.css > $(ipython locate)/nbextensions/toc.css

and load it with this in your custom.js:

```javascript
IPython.load_extensions('toc');
```

## Write and execute

This IPython Notebook magic writes the content of the cell to a specified .py file before executing it.
An identifier can be used when writing to the file, thus making it possible to overwrite previous iterations of the same code block. 
The use case for this extension is to export selected code from a Notebook for reuse through a .py file.

To install the extension use:
    %install_ext https://raw.githubusercontent.com/minrk/ipython_extensions/master/extensions/writeandexecute.py
Then load it with 
    %load_ext writeandexecute
