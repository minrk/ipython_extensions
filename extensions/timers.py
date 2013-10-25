# coding: utf-8
"""Extension for simple stack-based tic/toc timers

Each %tic starts a timer,
each %toc prints the time since the last tic

`%tic label` results in 'label: ' being printed at the corresponding %toc.

Usage:

In [6]: %tic outer
   ...: for i in range(4):
   ...:     %tic
   ...:     time.sleep(2 * random.random())
   ...:     %toc
   ...: %toc
  459 ms
  250 ms
  509 ms
  1.79 s
outer:   3.01 s
"""

import sys
import time

from IPython.core.magic import magics_class, line_magic, cell_magic, Magics
from IPython.core.magics.execution import _format_time

@magics_class
class TimerMagics(Magics):
    
    timers = None
    tics = None
    
    def __init__(self, *args, **kwargs):
        super(TimerMagics, self).__init__(*args, **kwargs)
        self.timers = {}
        self.tics = []
        self.labels = []
    
    @line_magic
    def tic(self, line):
        """Start a timer
        
        Usage:
        
            %tic [label]
        
        """
        label = line.strip() or None
        now = self.time()
        if label in self.timers:
            # %tic on an existing name prints the time,
            # but does not affect the stack
            self.print_time(now - self.timers[label], label)
            return
        
        if label:
            self.timers[label] = now
        self.tics.insert(0, self.time())
        self.labels.insert(0, label)
    
    @line_magic
    def toc(self, line):
        """Stop and print the timer started by the last call to %tic
        
        Usage:
        
            %toc
        
        """
        now = self.time()
        tic = self.tics.pop(0)
        label = self.labels.pop(0)
        self.timers.pop(label, None)
        
        self.print_time(now - tic, label)
    
    def print_time(self, dt, label):
        ts = _format_time(dt)
        msg = "%8s" % ts
        if label:
            msg = "%s: %s" % (label, msg)
        print ('%s%s' % ('  ' * len(self.tics), msg))
    
    @staticmethod
    def time():
        """time.clock seems preferable on Windows"""
        if sys.platform.startswith('win'):
            return time.clock()
        else:
            return time.time()
    
def load_ipython_extension(ip):
    """Load the extension in IPython."""
    ip.register_magics(TimerMagics)

