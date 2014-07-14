/*

Add this file to $(ipython locate)/nbextensions/celltags.js
And load it with:

IPython.load_extensions("celltags");
*/
define([
    "jquery",
    "base/js/namespace",
    "notebook/js/celltoolbar"
    ], function ($, IPython, ctb) {
        
    var tags_from_input = function (input_element) {
        var tag_str = input_element.val();
        var tags;
        if (tag_str.trim().length === 0) {
            tags = [];
        } else {
            tags = tag_str.split(",").map(
                function (s) { return s.trim(); }
            );
        }
        return tags;
    };
    
    var filter_tagged_cells = function () {
        var active_tags = IPython.notebook.metadata.active_cell_tags;
        var cells = IPython.notebook.get_cells();
        var tags;
        for (var i = 0; i < cells.length; i++) {
            var cell = cells[i];
            tags = cell.metadata.tags;
            if (!active_tags || active_tags.length === 0 || !tags || tags.length === 0) {
                cell.element.show();
            } else {
                var tag_match = false;
                for (var j = 0; j < tags.length; j++) {
                    var tag = tags[j];
                    if (active_tags.indexOf(tag) > -1) {
                        tag_match = true;
                        break;
                    }
                }
                if (tag_match) {
                    cell.element.show();
                } else {
                    cell.element.hide();
                }
            }
        }
    };
    
    var add_tags_input = function (div, cell) {
        var container = $(div);
        container.append($("<span/>").text("tags").css("padding", "5px"));
        var input = $('<input/>')
            .attr("size", 100)
            .val(
                (cell.metadata.tags || []).join(", ")
            )
            .on("focusout", function () {
                cell.metadata.tags = tags_from_input(input);
                filter_tagged_cells();
            });
        if (cell.keyboard_manager) {
            cell.keyboard_manager.register_events(input);
        }
        container.append(input);
    };
    
    var add_tag_toolbar = function () {
        var tag_toolbar = $("#tag_toolbar");
        if (tag_toolbar.length === 0) {
            tag_toolbar = $("<div/>").attr("id", "tag_toolbar");
            $("#menubar-container").append(tag_toolbar);
        }
        var active_tags_input = $("<input/>")
        active_tags_input
            .attr("id", "active_tag_input")
            .attr("size", 100)
            .val(
                (IPython.notebook.metadata.active_cell_tags || []).join(", ")
            ).on("focusout", function () {
                IPython.notebook.metadata.active_cell_tags = tags_from_input(active_tags_input);
                filter_tagged_cells();
            });
        IPython.notebook.keyboard_manager.register_events(active_tags_input);
        tag_toolbar.html("")
            .append($("<span/>")
                .css("padding", "5px")
                .text("filter tags"))
            .append(active_tags_input);
        filter_tagged_cells();
    };
    
    var register_celltoolbar = function () {
        ctb.CellToolbar.register_callback('tags.input', add_tags_input);

        var preset = ["tags.input"];

        ctb.CellToolbar.register_preset('Cell Tags', preset, IPython.notebook, IPython.events);
        console.log('Cell tags loaded.');
    };
    
    var load_ipython_extension = function () {
        
        if (IPython.notebook) {
            add_tag_toolbar();
            register_celltoolbar();
        }
        $([IPython.events]).on("notebook_loaded.Notebook", register_celltoolbar);
        $([IPython.events]).on("notebook_loaded.Notebook", add_tag_toolbar);
    };
    
    return {
        load_ipython_extension : load_ipython_extension,
    };
    
});