"""
This adds a 'share-as-gist' button to the IPython notebook toolbar.

It relies on the `gist` ruby gem, which you can install with `gem install gist`

Loading this Python extension will install its javascript counterparts,
and load them into your custom.js.
"""
from __future__ import print_function

import os
import urllib2

from subprocess import check_output

from IPython.display import display_javascript

load_js = """
// load the gist extension

require(["nbextensions/gistcomm"], function (gist_extension) {
    console.log('gist extension loaded');
    gist_extension.load_extension();
});
"""

def install_nbextension(ip):
    """install the gist javascript extension, and load it in custom.js"""
    
    gist_js = os.path.join(ip.ipython_dir, 'nbextensions', 'gistcomm.js')
    url = "http://rawgithub.com/minrk/ipython_extensions/master/nbextensions/gistcomm.js"
    here = os.path.dirname(__file__)
    if not os.path.exists(gist_js):
        local_gist_js = os.path.join(here, 'gistcomm.js')
        if os.path.exists(local_gist_js):
            print ("installing gistcomm.js from %s" % local_gist_js)
            gist_f = open(local_gist_js)
        else:
            print ("installing gistcomm.js from %s" % url)
            gist_f = urllib2.urlopen(url)
        with open(gist_js, 'w') as f:
            f.write(gist_f.read())
        gist_f.close()
    
    custom_js = os.path.join(ip.profile_dir.location, 'static', 'custom', 'custom.js')
    already_required = False
    if os.path.exists(custom_js):
        with open(custom_js, 'r') as f:
            js = f.read()
        already_required = "nbextensions/gist" in js
    
    if not already_required:
        print("loading gist button into custom.js")
        with open(custom_js, 'a') as f:
            f.write(load_js)
        display_javascript(load_js, raw=True);

class GistExtension(object):
    def __init__(self, comm, msg=None):
        self.comm = comm
        self.comm.on_msg(self.handler)
    
    def handler(self, msg):
        data = msg['content']['data']
        name = data['name']
        root = data['root']
        path = data['path']
        cmd = ['gist']
        if data.get('gist_id'):
            cmd.extend(['-u', data['gist_id']])
        cmd.append(os.path.join(root, path, name))
        try:
            output = check_output(cmd).decode('utf8').strip()
        except Exception as e:
            reply = dict(
                status='failed',
                message=str(e)
            )
        else:
            reply = dict(
                status='ok',
                gist_id = output.replace('https://gist.github.com/', '')
            )
        self.comm.send(reply)

def gist(line=''):
    display_javascript("IPython.gist_button.publish_gist()", raw=True)

def load_ipython_extension(ip):
    install_nbextension(ip)
    ip.magics_manager.register_function(gist)
    comms = getattr(ip, 'comm_manager', None)
    if comms:
        comms.register_target('gist', GistExtension)
    