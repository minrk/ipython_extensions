/*
Add a gist button to the IPython notebook toolbar

You can load it by putting:

require(["nbextensions/gist"], function (gist_extension) {
    console.log('gist extension loaded');
    gist_extension.load_extension();
});

in your custom.js

It also requires adding `gist` to your IPython extensions.

*/

define( function () {
    "use strict";
    
    var GistButton = function () {
        var that = this;
        $([IPython.events]).on("status_started.Kernel", $.proxy(this.setup_comm, this));
    };
    
    GistButton.prototype.setup_comm = function () {
        IPython.notebook.kernel.execute("%load_ext gist", IPython.notebook.get_cell(0).get_callbacks());
        this.comm = IPython.notebook.kernel.comm_manager.new_comm('gist');
        this.comm.on_msg($.proxy(this.handle_reply, this));
        this.update_gist_link();
    };
    
    GistButton.prototype.update_gist_link = function(gist_id) {
        if (!gist_id) {
            gist_id = IPython.notebook.metadata.gist_id;
        } else {
            IPython.notebook.metadata.gist_id = gist_id;
        }
        if (!gist_id) {
            return;
        }
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

    GistButton.prototype.handle_reply = function(msg) {
        var data = msg.content.data;
        if (data.status == 'ok') {
            console.log("gist succeeded: ", data.gist_id);
        } else {
            alert("Gist seems to have failed: " + data.message);
            console.log(msg);
        } 
        
        this.update_gist_link(data.gist_id);
    };

    GistButton.prototype.publish_gist = function () {
        var nb = IPython.notebook;
        var data = {
            gist_id: nb.metadata.gist_id || null,
            name: nb.notebook_name,
            path: nb.notebook_path,
            root: $("body").data("project")
        };
        this.comm.send(data);
    };
    
    GistButton.prototype.setup_gist_button = function () {
        if ($("#gist_notebook").length === 0) {
            IPython.toolbar.add_buttons_group([
                {
                    'label'   : 'Share Notebook as gist',
                    'icon'    : 'icon-share',
                    'callback': $.proxy(this.publish_gist, this),
                    'id'      : 'gist_notebook'
                },
            ])
        }
        this.update_gist_link();
    };
    
    var load_extension = function () {
        IPython.gist_button = new GistButton();
    
        $([IPython.events]).on('notebook_loaded.Notebook', function() {
            IPython.gist_button.update_gist_link();
        });
    
        IPython.gist_button.setup_gist_button();
    }
    return {
        GistButton : GistButton,
        load_extension : load_extension,
    };
});