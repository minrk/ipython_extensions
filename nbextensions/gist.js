/*
Add this file to $(ipython locate)/nbextensions/gist.js
And load it with:

require(["nbextensions/gist"], function (gist_extension) {
    console.log('gist extension loaded');
    gist_extension.load_ipython_extension();
});

*/
define( function () {
    
    var token_name = "gist_github_token";
    
    // dialog to request GitHub OAuth token
    // I'm not sure it's possible to step through OAuth purely client side,
    // so just ask the user to go create a token manually.
    
    var token_dialog = function () {
        var dialog = $('<div/>').append(
            $("<p/>")
                .html('Enter a <a href="https://github.com/settings/applications" target="_blank">GitHub OAuth token</a>:')
        ).append(
            $("<br/>")
        ).append(
            $('<input/>').attr('type','text').attr('size','40')
        );
        IPython.dialog.modal({
            title: "GitHub OAuth",
            body: dialog,
            buttons : {
                "Cancel": {},
                "OK": {
                    class: "btn-primary",
                    click: function () {
                        var token = $(this).find('input').val();
                        localStorage[token_name] = token;
                        gist_notebook();
                    }
                }
            },
            open : function (event, ui) {
                var that = $(this);
                // Upon ENTER, click the OK button.
                that.find('input[type="text"]').keydown(function (event, ui) {
                    if (event.which === 13) {
                        that.find('.btn-primary').first().click();
                        return false;
                    }
                });
                that.find('input[type="text"]').focus().select();
            }
        });
    };
    // get the GitHub token, via cookie or 
    var get_github_token = function () {
        var token = localStorage[token_name];
        if (!token) {
            token_dialog();
            return null;
        }
        return token;
    };

    var gist_notebook = function () {
        if (!IPython.notebook) return;
        var gist_id = IPython.notebook.metadata.gist_id;
        console.log(gist_id);
        var token = get_github_token();
        if (!token) {
            // dialog's are async, so we can't do anything yet.
            // the dialog OK callback will continue the process.
            console.log("waiting for auth dialog");
            return;
        }
        var method = "POST";
        var url = "https://api.github.com/gists";
        if (gist_id) {
            url = url + "/" + gist_id;
            method = "PATCH";
        }
        var filedata = {};
        var nbj = IPython.notebook.toJSON();
        filedata[IPython.notebook.notebook_name] = {content : JSON.stringify(nbj, undefined, 1)};
        var settings = {
            type : method,
            headers : { Authorization: "token " + token },
            data : JSON.stringify({
                public : true,
                files : filedata,
            }),
            success : function (data, status) {
                console.log("gist succeeded: " + data.id);
                IPython.notebook.metadata.gist_id = data.id;
                update_gist_link(data.id);
                IPython.notification_area.get_widget("notebook").set_message("gist succeeded: " + data.id, 1500);
            },
            error : function (jqXHR, status, err) {
                if (true || jqXHR.status == 403) {
                    // authentication failed,
                    // delete the token so that we prompt again next time
                    delete localStorage[token_name];
                }
                alert("Uploading gist failed: " + err);
            }
        };
        $.ajax(url, settings);
    };
    
    var update_gist_link = function(gist_id) {
        if (!IPython.notebook) return;
        
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

    var gist_button = function () {
        if (!IPython.toolbar) {
            $([IPython.events]).on("app_initialized.NotebookApp", gist_button);
            return;
        }
        if ($("#gist_notebook").length === 0) {
            IPython.toolbar.add_buttons_group([
                {
                    'label'   : 'Share Notebook as gist',
                    'icon'    : 'fa-share',
                    'callback': gist_notebook,
                    'id'      : 'gist_notebook'
                },
            ]);
        }
        update_gist_link();
    };
    
    var load_ipython_extension = function () {
        gist_button();
        update_gist_link();
        $([IPython.events]).on("notebook_loaded.Notebook", function () {update_gist_link();});
    };
    
    return {
        load_ipython_extension : load_ipython_extension,
    };
    
});