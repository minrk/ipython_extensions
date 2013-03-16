"""

Simple getpass / raw_input workarounds for the IPython notebook using jQueryUI dialogs.
Not awesome, because they don't *return* the response, they store them in a variable,
but it should suffice in a few situations while we implement the real thing.

"""

from IPython import display, Javascript

def nbgetpass(prompt="Enter Password", name='passwd'):
    display(Javascript("""
var dialog = $('<div/>').append(
    $('<input/>')
    .attr('id', 'password')
    .attr('name', 'password')
    .attr('type', 'password')
    .attr('value', '')
);
$(document).append(dialog);
dialog.dialog({
    resizable: false,
    modal: true,
    title: "%s",
    closeText: '',
    buttons : {
        "Okay": function () {
            IPython.notebook.kernel.execute(
                "%s = '" + $("input#password").attr('value') + "'"
            );
            $(this).dialog('close');
            dialog.remove();
        },
        "Cancel": function () {
            $(this).dialog('close');
            dialog.remove();
        }
    }
});
""" % (prompt, name)), include=['application/javascript'])
                                  
def nb_raw_input(prompt, name="raw_input_reply"):
    display(Javascript("""
var dialog = $('<div/>').append(
    $('<input/>')
    .attr('id', 'theinput')
    .attr('value', '')
);
$(document).append(dialog);
dialog.dialog({
    resizable: false,
    modal: true,
    title: "%s",
    closeText: '',
    buttons : {
        "Okay": function () {
            IPython.notebook.kernel.execute(
                "%s = '" + $("input#theinput").attr('value') + "'"
            );
            $(this).dialog('close');
            dialog.remove();
        },
        "Cancel": function () {
            $(this).dialog('close');
            dialog.remove();
        }
    }
});
""" % (prompt, name)), include=['application/javascript'])

def load_ipython_extension(ip):
    ip.user_ns['nb_raw_input'] = nb_raw_input
    ip.user_ns['nbgetpass'] = nbgetpass
