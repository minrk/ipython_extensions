/*
Install this with

    jupyter nbextension install editor-tabs.js

Enable it with:

    jupyter nbextension enable --section edit editor-tabs

*/
define( function () {
  var $ = require('jquery');
  var Jupyter = require('base/js/namespace');

  function toggle_tabs() {
    $("#indent-with-tabs").find('.fa-check').toggle();
    var current = Jupyter.editor.codemirror.getOption('indentWithTabs');
    Jupyter.editor.update_codemirror_options({indentWithTabs: !current});
  };

  function add_button() {
    var current = Jupyter.editor.codemirror.getOption('indentWithTabs');
    var entry = $("<li>").attr('id', 'indent-with-tabs');
    entry.append(
      $("<a>")
      .attr('href', '#')
      .text("Indent with Tabs")
      .click(toggle_tabs)
      .append(
        $("<i>").addClass('fa fa-check')
      )
    )
    if (!current) {
      entry.find(".fa-check").hide();
    }
    $("#edit-menu").append($("<li>").addClass('divider'));
    $("#edit-menu").append(entry);
  }

  function load_ipython_extension () {
    console.log("Loading editor-tabs extension");
    add_button();
  };

  return {
    load_ipython_extension : load_ipython_extension,
  };

});