"""
Extension for disabling autoscrolling long output, which is super annoying sometimes

Usage:

    %load_ext disable_autoscroll

You can also put the js snippet below in profile_dir/static/js/custom.js
"""

from IPython.display import display, Javascript

disable_js = """
IPython.OutputArea.prototype._should_scroll = function(lines) {
    return false;
}
"""

def load_ipython_extension(ip):
    display(Javascript(disable_js))
    print ("autoscrolling long output is disabled")
