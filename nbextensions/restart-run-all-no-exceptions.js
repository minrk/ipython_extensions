// Add Restart & Run All (no exceptions) item to Kernel menu
// Same as Restart & Run All, but continue execution on exception

define(function (require, exports, module) {
  "use strict";
  var $ = require('jquery');
  var Jupyter = require('base/js/namespace');

  function restart_run_all_no_exceptions() {
    var nb = Jupyter.notebook;
    return nb.restart_kernel().then(function () {
      nb.get_cells().map(function (cell) {
        cell.execute(false);
      });
    });
  }

  function load_extension () {
    // add menu entry
    $('li#restart_run_all').before(
      $('<li>')
      .attr('id', 'restart_run_all_no_exceptions')
      .attr('title', "Restart the kernel and run all cells, not stopping at exceptions.")
        .append(
          $('<a>')
            .attr('href', '#')
            .text('Restart & Run All (no exceptions)')
            .click(restart_run_all_no_exceptions)
        )
    )
  }

  return {
    load_ipython_extension: load_extension,
  };
});