"""
This is the gist share button,
and a %gist magic, as a Python extension.
You can also get just the gist button without this extension by adding
the contents of gist.js to static/js/custom.js in your profile.

This code requires that you have the jist rubygem installed and properly configured.

"""

gist_js = r"""

/*
Add the contents of this file to your custom.js
for it to always be on.
*/


IPython.ext_update_gist_link = function(gist_id) {
    
    IPython.notebook.metadata.gist_id = gist_id;
    var toolbar = IPython.toolbar.element;
    var link = toolbar.find("a#nbviewer");
    if ( ! link.length ) {
        link = $('<a id="nbviewer" target="_blank"/>');
        toolbar.append(
            $('<span id="nbviewer_span"/>').append(link)
        );
    }
    
    link.attr("href", "http://nbviewer.ipython.org/" + gist_id);
    link.text("http://nbviewer.ipython.org/" + gist_id);
};

IPython.ext_handle_gist_output = function(output_type, content) {
    if (output_type != 'stream' || content['name'] != 'stdout') {
        return;
    }
    var gist_id = jQuery.trim(content['data']);
    if (! gist_id.match(/[A-Za-z0-9]+/g)) {
        alert("Gist seems to have failed: " + gist_id);
        return;
    }
    IPython.ext_update_gist_link(gist_id);
};

IPython.ext_gist_notebook = function () {
    var gist_id = IPython.notebook.metadata.gist_id || null;
    var cmd = '_nbname = "' + IPython.notebook.notebook_name + '.ipynb"';
    cmd = cmd + '\nlines = !jist -p'
    if (gist_id) {
        cmd = cmd + ' -u ' + gist_id;
    }
    cmd = cmd + ' $_nbname';
    cmd = cmd + '\nprint lines[0].replace("https://gist.github.com", "").replace("/","")';
    IPython.notebook.kernel.execute(cmd, {'output' : IPython.ext_handle_gist_output});
};

setTimeout(function() {
    if ($("#gist_notebook").length == 0) {
        IPython.toolbar.add_buttons_group([
            {
                'label'   : 'Share Notebook as gist',
                'icon'    : 'ui-icon-share',
                'callback': IPython.ext_gist_notebook,
                'id'      : 'gist_notebook'
            },
        ])
    }

    if (IPython.notebook.metadata.gist_id) {
        IPython.ext_update_gist_link(IPython.notebook.metadata.gist_id);
    }
}, 1000);

"""


from IPython.display import display, Javascript

def gist(line=''):
    display(Javascript("IPython.ext_gist_notebook()"))

def load_ipython_extension(ip):
    display(Javascript(gist_js))
    ip.magics_manager.register_function(gist)
    
    