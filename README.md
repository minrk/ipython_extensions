# Miscellaneous IPython extensions

You can install each extension individually, or you can just clone the whole repo into your `.ipython/extensions` dir.

## Gist

Add a gist button to the notebook toolbar:

    $ curl https://rawgithub.com/minrk/ipython_extensions/master/nbextensions/gist.js > $(ipython locate)/nbextensions/gist.js

and load it by adding to your custom.js, found in `$(ipython locate profile)/static/custom/custom.js`:

```javascript
require(["nbextensions/gist"], function (gist_extension) {
    console.log('gist extension loaded');
    gist_extension.load_extension();
});
```


## Retina Figures

Enable 2x display of matplotlib figures

install the extension:

    %install_ext https://rawgithub.com/minrk/ipython_extensions/master/extensions/retina.py

load the extension:

    %load_ext retina

## Table of Contents 

Automatically generates floating table of contents inside your ipnb from the headers.
Autoresize and scroll capabilities.

install the extension:

    %install_ext https://rawgithub.com/minrk/ipython_extensions/master/extensions/nbtoc.py

load the extension:

    %load_ext nbtoc
    %nbtoc

run `%nbtoc` once more to refresh the Table-of-contents


    
