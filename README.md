# Miscellaneous IPython extensions

You can install each extension individually, or you can just clone the whole repo into your `.ipython/extensions` dir.

## Autosave

An Extension for managing periodic autosave of IPython notebooks

install the extension:

    %install_ext https://raw.github.com/minrk/ipython_extensions/master/autosave.py

load the extension:

    %load_ext autosave

autosave every 30 seconds:

    %autosave 30

disable autosave:

    %autosave 0

trigger single save from Python (just like clicking the save button):

    %savenb

## Retina Figures

Enable 2x display of matplotlib figures

install the extension:

    %install_ext https://raw.github.com/minrk/ipython_extensions/master/retina.py

load the extension:

    %load_ext retina

## Table of Contents 

Automatically generates floating table of contents inside your ipnb from the headers.
Autoresize and scroll capabilities.

install the extension:

    %install_ext https://raw.github.com/minrk/ipython_extensions/master/nbtoc.py

load the extension:

    %load_ext nbtoc
    %nbtoc

run `%nbtoc` once more to refresh the Table-of-contents


    
