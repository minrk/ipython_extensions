/*
Add this file to $(ipython locate)/nbextensions/gist.js
And load it with:

require(["nbextensions/gist"], function (gist_extension) {
    console.log('gist extension loaded');
    gist_extension.load_extension();
});

*/
define( function () {
    
    var token_cookie_name = "gist_github_token";
    
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
                        set_cookie(token_cookie_name, token);
                        gist_notebook();
                    }
                }
            },
            open : function (event, ui) {
                var that = $(this);
                // Upon ENTER, click the OK button.
                that.find('input[type="text"]').keydown(function (event, ui) {
                    if (event.which === utils.keycodes.ENTER) {
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
        var token = get_cookie(token_cookie_name);
        if (!token) {
            token_dialog();
            return null;
        }
        return token;
    };

    // cookie utils from http://www.elated.com/articles/javascript-and-cookies/

    var set_cookie = function (name, value) {
        document.cookie = name + "=" + escape(value);
    };

    var get_cookie = function (name) {
        var results = document.cookie.match( '(^|;) ?' + name + '=([^;]*)(;|$)' );

        if (results) {
            return unescape(results[2]);
        } else {
            return null;
        }
    };

    var delete_cookie = function (name) {
        document.cookie = name += "=; expires=" + new Date(0).toGMTString();
    };

    var gist_notebook = function () {
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
        nbj.nbformat = 3;
        filedata[IPython.notebook.notebook_name] = {content : JSON.stringify(nbj, undefined, 1)};
        console.log(token);
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
                IPython.notification_area.get_notification_widget("notebook").set_message("gist succeeded: " + data.id, 500);
            },
            error : function (jqXHR, status, err) {
                console.log(jqXHR);
                if (jqXHR.status == 403) {
                    // authentication failed,
                    // delete the cookie so that we prompt again next time
                    delete_cookie(token_cookie_name);
                }
                alert("Uploading gist failed: " + err);
            }
        };
        $.ajax(url, settings);
    };
    
    var update_gist_link = function(gist_id) {
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
                    'icon'    : 'icon-share',
                    'callback': gist_notebook,
                    'id'      : 'gist_notebook'
                },
            ]);
        }
        update_gist_link();
    };
    
    var load_extension = function () {
        gist_button();
        update_gist_link();
        $([IPython.events]).on("notebook_loaded.Notebook", function () {update_gist_link();});
    };
    
    return {
        load_extension : load_extension,
    };
    
});