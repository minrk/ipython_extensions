/*
Add this file and neighboring toc.css to $(ipython locate)/nbextensions/

And load it with:

require(["nbextensions/toc"], function (toc) {
console.log('Table of Contents extension loaded');
toc.load_extension();
// If you want to load the toc by default, add:
// $([IPython.events]).on("notebook_loaded.Notebook", toc.table_of_contents);
});

*/

// adapted from https://gist.github.com/magican/5574556

define(["require"], function (require) {
  "use strict";

  var clone_anchor = function (element) {
    // clone link
    var h = element.find("div.text_cell_render").find(':header').first();
    var a = h.find('a').clone();
    var new_a = $("<a>");
    new_a.attr("href", a.attr("href"));
    // get the text *excluding* the link text, whatever it may be
    var hclone = h.clone();
    hclone.children().remove();
    new_a.text(hclone.text());
    return new_a;
  };

  var ol_depth = function (element) {
    // get depth of nested ol
    var d = 0;
    while (element.prop("tagName").toLowerCase() == 'ol') {
      d += 1;
      element = element.parent();
    }
    return d;
  };
  
  var create_toc_div = function () {
    var toc_wrapper = $('<div id="toc-wrapper"/>')
    .append(
      $("<div/>")
      .addClass("header")
      .text("Contents ")
      .click( function(){
        console.log(this);
        $('#toc').slideToggle();
        $('#toc-wrapper').toggleClass('closed');
        if ($('#toc-wrapper').hasClass('closed')){
          $('#toc-wrapper .hide-btn').text('[+]');
        } else {
          $('#toc-wrapper .hide-btn').text('[-]');
        }
        return false;
      }).append(
        $("<a/>")
        .attr("href", "#")
        .addClass("hide-btn")
        .text("[-]")
      )
    ).append(
        $("<div/>").attr("id", "toc")
    );
    $("body").append(toc_wrapper);
  };

  var table_of_contents = function (threshold) {
    if (threshold === undefined) {
      threshold = 4;
    }
    var cells = IPython.notebook.get_cells();
      
    var toc_wrapper = $("#toc-wrapper");
    if (toc_wrapper.length === 0) {
      create_toc_div();
    }
  
    var ol = $("<ol/>");
    $("#toc").empty().append(ol);
  
    for (var i=0; i < cells.length; i++) {
      var cell = cells[i];
    
      if (cell.cell_type !== 'heading') continue;
    
      var level = cell.level;
      if (level > threshold) continue;
    
      var depth = ol_depth(ol);

      // walk down levels
      for (; depth < level; depth++) {
        var new_ol = $("<ol/>");
        ol.append(new_ol);
        ol = new_ol;
      }
      // walk up levels
      for (; depth > level; depth--) {
        ol = ol.parent();
      }
      //
      ol.append(
        $("<li/>").append(clone_anchor(cell.element))
      );
    }

    $(window).resize(function(){
      $('#toc').css({maxHeight: $(window).height() - 200});
    });

    $(window).trigger('resize');
  };
    
  var toggle_toc = function () {
    // toggle draw (first because of first-click behavior)
    $("#toc-wrapper").toggle();
    // recompute:
    table_of_contents();
  };
  
  var toc_button = function () {
    if (!IPython.toolbar) {
      $([IPython.events]).on("app_initialized.NotebookApp", toc_button);
      return;
    }
    if ($("#toc_button").length === 0) {
      IPython.toolbar.add_buttons_group([
        {
          'label'   : 'Table of Contents',
          'icon'    : 'icon-list',
          'callback': toggle_toc,
          'id'      : 'toc_button'
        },
      ]);
    }
  };
  
  var load_css = function () {
    var link = document.createElement("link");
    link.type = "text/css";
    link.rel = "stylesheet";
    link.href = require.toUrl("./toc.css");
    console.log(link);
    document.getElementsByTagName("head")[0].appendChild(link);
  };
  
  var load_extension = function () {
    load_css();
    toc_button();
    // $([IPython.events]).on("notebook_loaded.Notebook", table_of_contents);
  };

  return {
    load_extension : load_extension,
    toggle_toc : toggle_toc,
    table_of_contents : table_of_contents,
    
  };

});
