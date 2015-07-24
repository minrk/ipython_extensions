// This extension adds a button to renumber cells in order,
// letting you pretend you re-ran from the beginning,
// without actually doing so.
// For @oceankidbilly

define(['jquery', 'base/js/namespace'], function ($, IPython) {

    function renumber () {
        // renumber cells in order, so it doesn't look like you made any mistakes
        var i=1;
        IPython.notebook.get_cells().map(function (cell) {
            if (cell.cell_type == 'code') {
                // set the input prompt
                cell.set_input_prompt(i);
                // set the output prompt (in two places)
                cell.output_area.outputs.map(function (output) {
                    if (output.output_type == 'execute_result') {
                        output.execution_count = i;
                        cell.element.find(".output_prompt").text('Out[' + i + ']:');
                    }
                });
                i += 1;
            }
        });
    }
    
    function add_button () {
        if (!IPython.toolbar) {
            $([IPython.events]).on("app_initialized.NotebookApp", add_button);
            return;
        }

        if ($("#renumber-button").length === 0) {
            IPython.toolbar.add_buttons_group([{
              'label'   : 'Renumber cells',
              'icon'    : 'fa-list-ol',
              'callback': renumber,
              'id'      : 'renumber-button'
            }]);
        }
    };

    return {
        load_ipython_extension : add_button,
    };

    IPython.toolbar.add_buttons_group([{
      'label'   : 'Renumber cells',
      'icon'    : 'fa-list-ol',
      'callback': renumber,
      'id'      : 'renumber-button'
    }]);
});