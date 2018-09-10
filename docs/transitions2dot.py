# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import textwrap
from dkfileutils.path import Path

FILE = Path(__file__)
DIRNAME = FILE.dirname


def transitions_to_dot(transitions, states):
    def fillcolor(c, fc=None):
        return {'style': 'filled',
                'fillcolor': c,
                'fontcolor': fc or 'white'}

    sdata = {s[0]: s[2] for s in states}
    rules = []
    for cur, nexts in transitions.iteritems():
        for nxt in nexts:
            rule = '        "%s" -> "%s"' % (cur, nxt)
            if 'comm' in sdata[nxt]:
                rule += ' [label="step-%d"]' % sdata[nxt]['comm']
                del sdata[nxt]['comm']
                sdata[nxt].update(fillcolor('blue'))
            rules.append(rule + ';')

    nodes = []

    for node, attrs in sdata.iteritems():
        if node.endswith('-err'):
            attrs.update(fillcolor('red'))
        if node.endswith('-ok'):
            attrs.update(fillcolor('green'))
        if attrs:
            if 'comm' in attrs:
                attrs.update(fillcolor('blue'))

            nodeattrs = '        "%s" [%s];' % (
                node,
                ';'.join('%s=%s' % kv for kv in attrs.iteritems())
            )
            nodes.append(nodeattrs)

    return textwrap.dedent("""\
    digraph G {
        node [shape=box];
        rankdir = "LR";
    \n    %s
    \n    %s
    }
    """ % (
        '\n    '.join(rules),
        '\n    '.join(nodes)
    ))


if __name__ == '__main__':
    from toolcall.models.legal_transitions import states, transitions
    default_output = 'diagrams/transitions.dot'
    output_fname = sys.argv[1] if len(sys.argv) > 1 else default_output
    dotsrc = transitions_to_dot(transitions, states)
    print(dotsrc)
    Path(output_fname).write(dotsrc)
