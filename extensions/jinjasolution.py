"""A simple extension that renders cells as jinja templates.

For demonstration purposes, this renders in a simple environment with `solution=True`,
so that a solution notebook *template* will be executable.

Input with:

    {% if solution %}
    solution_code
    {% else %}
    student_code
    {% endif %}

will be executable as the solution version.
"""

from __future__ import print_function
import sys

import jinja2

from IPython.core.inputtransformer import InputTransformer


class SolutionInputTransformer(InputTransformer):
    """Renders IPython input cells as jinja templates with solution=True"""
    def __init__(self, *args, **kwargs):
        super(SolutionInputTransformer, self).__init__(*args, **kwargs)
        
        self.env = jinja2.Environment()
        self._lines = []
    
    def push(self, line):
        self._lines.append(line)
        return None
    
    def reset(self):
        text = u'\n'.join(self._lines)
        self._lines = []
        template = self.env.from_string(text)
        try:
            return template.render(solution=True)
        except Exception as e:
            print("Failed to render jinja template: %s" % e, file=sys.stderr)
            return text


def load_ipython_extension(ip):
    """register the transformer as the first physical line transform."""
    ip.input_transformer_manager.python_line_transforms.append(
        SolutionInputTransformer()
    )
