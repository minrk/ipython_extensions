/*

Add QtConsole button to notebook toolbar

Only works with IPython kernel

install:

jupyter nbextension install --user https://rawgithub.com/minrk/ipython_extensions/master/nbextensions/qtconsole-button.js
jupyter nbextension enable qtconsole-button

Copyright (c) Min RK.
Distributed under the terms of the Modified BSD License.

*/

define(function (require, exports, module) {
  "use strict";
  var $ = require('jquery');
  var Jupyter = require('base/js/namespace');
  var events = require('base/js/events');
  
  function launch_qtconsole() {
    var kernel = Jupyter.notebook.kernel;
    kernel.execute("%qtconsole --style monokai"); // monokai for @ianozsvald
  }
  
  function qtconsole_button () {
      if (!Jupyter.toolbar) {
          events.on("app_initialized.NotebookApp", qtconsole_button);
          return;
      }
      if ($("#qtconsole-button").length === 0) {
          Jupyter.toolbar.add_buttons_group([
              {
                  'label'   : 'Launch QtConsole attached to this kernel',
                  'icon'    : 'fa-terminal',
                  'callback': launch_qtconsole,
                  'id'      : 'qtconsole-button'
              },
          ]);
      }
  }
  
  function load_ipython_extension () {
      qtconsole_button();
  }
  
  return {
      load_ipython_extension : load_ipython_extension,
  };
  
});