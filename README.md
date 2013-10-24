# Miscellaneous IPython extensions

You can install each extension individually, or you can just clone the whole repo into your `.ipython/extensions` dir.

## Gist

Add a gist button to the notebook toolbar:

    %install_ext https://rawgithub.com/minrk/ipython_extensions/master/gist.py
    %load_ext gist

This one requires the [gist](https://github.com/defunkt/gist) rubygem.

## Retina Figures

Enable 2x display of matplotlib figures

install the extension:

    %install_ext https://rawgithub.com/minrk/ipython_extensions/master/retina.py

load the extension:

    %load_ext retina

## Table of Contents 

Automatically generates floating table of contents inside your ipnb from the headers.
Autoresize and scroll capabilities.

install the extension:

    %install_ext https://rawgithub.com/minrk/ipython_extensions/master/nbtoc.py

load the extension:

    %load_ext nbtoc
    %nbtoc

run `%nbtoc` once more to refresh the Table-of-contents


    
