/*
Jupyter notebook extension to enforce cells executed in order

1. cells that have been executed are green
2. cells that have failed are red
3. executing a cell automatically executes all cells above in order
4. an error prevents execution of cells below
5. modifying a cell invalidates state and will restart kernel on next execute

Caveats:

- state is preserved only on the page, so refreshing the page with a running kernel allows inconsistent state
  (restarting the kernel will cause the state to become consistent again).

License: BSD 3-Clause

install and enable with:

    jupyter nbextension install inorder.js [--user]
    jupyter nbextension enable inorder

*/
define([], function () {
  var Jupyter = require('base/js/namespace');
  var events = require('base/js/events');
  
  function handle_cell_above(cell, idx) {
    // a cell below this one has requested execution
    if (cell.cell_type != 'code_cell') return;
    if (cell.element.hasClass('inorder-error')) {
      // return true means we should prevent future execution
      return true;
    }
    cell.execute();
  }

  function handle_cell_below(cell, idx) {
    // a cell above this one has been executed
    // clear its output
    if (cell.cell_type != 'code_cell') return;
    
    unlock_cell(cell);
    cell.element.removeClass('inorder-executed');
    cell.clear_output();
  }
  
  function unlock_cell(cell) {
    // unlock a given cell
    if (cell.cell_type != 'code_cell') return;
    cell.element.removeClass('inorder-locked');
    cell.element.removeClass('inorder-error');
    cell.clear_output();
  }
  
  function lock_cell(cell) {
    // lock a cell.
    if (cell.cell_type != 'code_cell') return;
    // on edit, unlock cell and invalidate cells below
    cell.element.addClass('inorder-locked');
    cell.code_mirror.on("change", function () {
      unlock_cell(cell);
      var nb = Jupyter.notebook;
      var idx = nb.find_cell_index(cell);
      invalidate_below(idx);
    });
  }
  
  function invalidate_below(idx) {
    // invalidate cells after a given cell.
    var cells = Jupyter.notebook.get_cells();
    for (var i = idx + 1; i < cells.length; i++) {
      handle_cell_below(cells[i], i);
    }
  }
  
  function my_execute() {
    // our version of CodeCell.execute
    // check state and maybe restart kernel
    // ... and then do the real execute
    var cell = this;
    var nb = Jupyter.notebook;
    var idx = nb.find_cell_index(cell);
    var cells = nb.get_cells();
    if (cell.element.hasClass('inorder-locked')) {
      // locked means it's valid, don't re-execute
      return;
    }
    
    // check if cell below has been executed
    // if so, restart the kernel and run to here.
    if (cell.element.hasClass('inorder-executed')) {
      cells.map(unlock_cell);
      console.log("Restarting kernel to restore consistent state.");
      nb.kernel.restart(function () {
        for (var i = 0; i <= idx; i++) {
          nb.execute_cells([i]);
        }
      });
      return;
    }
    
    // check cells above for
    // - errors
    // - execution
    for (var i = 0; i < idx; i++) {
      if (handle_cell_above(cells[i], i)) {
        // we noticed an error, so stop before we execute this cell
        return;
      }
    }
    
    // actually lock and run this cell
    cell.element.addClass('inorder-executed');
    lock_cell(cell);
    var f = this.original_execute();
    // invalidate cells after this one, now that we have been execute
    invalidate_below(idx);
    return f; // incase original execute returns a promise
  }
  
  function cell_for_output_area(output_area) {
    // get the cell corresponding to a given output area,
    // since output areas don't have a reference to their parent
    var nb = Jupyter.notebook;
    var cells = nb.get_cells();
    for (var i = 0; i < cells.length; i++) {
      var cell = cells[i];
      if (cell.output_area == output_area) {
        return cell;
      }
    }
  }
  
  function handle_error(evt, data) {
    // called when an error is produced by execution
    // triggers invalidation of cells below and prevents their execution
    var output_area = data.output_area;
    var cell = cell_for_output_area(output_area);
    var nb = Jupyter.notebook;
    var idx = nb.find_cell_index(cell);
    cell.element.addClass('inorder-error');
    invalidate_below(idx);
  }
  
  function monkeypatch() {
    // patch Cell.execute and OutputArea.append_error for missing functionality
    
    // find the first code cell
    console.log("patching execute");
    
    // create and destroy code cell at end
    var nb = Jupyter.notebook;
    var ncells = nb.ncells();
    var cell = nb.insert_cell_at_index('code', ncells);
    
    var CodeCell = Object.getPrototypeOf(cell);
    var OutputArea = Object.getPrototypeOf(cell.output_area);
    Jupyter.notebook.delete_cells([ncells]);
    
    if (CodeCell.original_execute) {
      // already patched
      return;
    }
    CodeCell.original_execute = CodeCell.execute;
    CodeCell.execute = my_execute;
    
    // patch OutputArea.append_error because there is no event for errors
    OutputArea.original_append_error = OutputArea.append_error;
    OutputArea.append_error = function () {
      OutputArea.original_append_error.apply(this, arguments);
      events.trigger('output_error.InOrderExtension', {
        output_area: this,
        data: arguments[0],
      });
    };
  }
  
  function load_extension () {
    console.log("Loading inorder extension");

    // when there's an error, mark it and invalidate below
    events.on('output_error.InOrderExtension', handle_error);

    // when the kernel restarts, reset all state
    events.on('kernel_restarting.Kernel', function () {
      var cells = Jupyter.notebook.get_cells();
      cells.map(function (cell) {
        unlock_cell(cell);
        cell.element.removeClass('inorder-executed');
      });
    });
    
    // add our css (!important due to race with cell.selected)
    var style = document.createElement("style");
    style.type = "text/css";
    style.innerHTML = 
      "div.cell.inorder-locked { background-color: #afa !important}\n" +
      "div.cell.inorder-locked.inorder-error { background-color: #faa !important}\n"
    ;
    document.getElementsByTagName("head")[0].appendChild(style);
  
    // apply patches when the notebook has been loaded
    if (!Jupyter.notebook) {
      events.one('notebook_loaded.Notebook', monkeypatch);
    } else {
      monkeypatch();
    }
  }

  return {
    load_ipython_extension: load_extension,
  };
});
