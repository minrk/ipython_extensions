// Remove outputs from saved data.
// Saves bandwidth on slow connections, etc.
// THIS IS DESTRUCTIVE in that opening a notebook and saving it will delete your output data.
//
// install me with
//     jupyter nbextension install [url-to-this-file]
// and enable me with
//     jupyter nbextension enable dontsaveoutput


define(["notebook/js/notebook"], function (notebook) {
  "use strict";
  function load () {
    var origToJSON = notebook.Notebook.prototype.toJSON;
    notebook.Notebook.prototype.toJSON = function () {
      var data = origToJSON.apply(this);
      console.log("Deleting outputs prior to save.");
      data.cells.map(function (cell) {
        if (cell.cell_type == 'code') {
          // clear outputs so we don't save them
          cell.outputs = [];
        }
      });
      return data;
    };
  }

  return {
    load_ipython_extension: load
  };
});
