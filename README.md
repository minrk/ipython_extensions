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

Enable 2x display of matplotlib figures (no longer necessary on IPython master)

install the extension:

    %install_ext https://rawgithub.com/minrk/ipython_extensions/master/extensions/retina.py

load the extension:

    %load_ext retina

## Table of Contents 

Generates floating table of contents inside your notebook from the heading cells.
Adds a button to the toolbar to toggle the floating table of contents.

install the extension:

    $ curl https://rawgithub.com/minrk/ipython_extensions/master/nbextensions/toc.js > $(ipython locate)/nbextensions/toc.js
    $ curl https://rawgithub.com/minrk/ipython_extensions/master/nbextensions/toc.css > $(ipython locate)/nbextensions/toc.css

and load it with this in your custom.js:

```javascript
require(["nbextensions/toc"], function (toc) {
    console.log('Table of Contents extension loaded');
    toc.load_extension();
});
```
