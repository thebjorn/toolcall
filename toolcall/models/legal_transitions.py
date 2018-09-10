# -*- coding: utf-8 -*-
import os

DIRNAME = os.path.dirname(__file__)

states = [
    ('initial',
        'Not Started', {'shape': 'point'}),
    ('started',
        'User has started tool call', {}),
    ('tool-validated',
        "Tool and Client exist and are active", {}),
    ('authenticated',
        "User is authenticated (we know who they are)", {}),
    ('authorized',
        "User is authorized to use this tool", {}),
    ('start-tk-sent',
        "Token sent to Client's receive_start_token_url", {'comm': 1}),
    ('start-tk-sent-ok',
        "Client returned success after receiving the token", {}),
    ('start-tk-sent-err',
        "Client returned an error after receiving the token", {}),
    ('start-tk-received',
        "Server received start-tk", {'comm': 2}),
    ('start-tk-ok',
        "Start token is valid", {}),
    ('start-tk-err',
        "Start token is not valid", {}),
    ('start-data-sent',
        "Start data sent to Client's receive_start_data_url", {'comm': 3}),
    ('start-data-sent-ok',
        'Client returned success after receiving start data', {}),
    ('start-data-sent-err',
        'Client returned an error after receiving start data', {}),
    ('tool-timeout-err',
        "Tool has exceeded its time limit", {}),
    ('result-tk-received',
        "Result token received from client.", {'comm': 4}),
    ('result-tk-sent',
        "Result token sent to Client's receive_result_token_url.", {'comm': 5}),
    ('result-received-ok',
        "Client returned result data.", {'comm': 6}),
    ('result-received-err',
        "Client did not return result data.", {}),
    ('result-saved',
        "Client result has been sucessfully saved on server", {}),
    ('finished-ok',
        "Tool call has finished without error", {'shape': 'doublecircle'}),
    ('finished-err',
            "Tool call has finished with error", {'shape': 'doublecircle'}),
    ('err',
        'Error', {'style':'filled', 'fillcolor':'red', 'fontcolor':'white'}),
]

choices = [s[:2] for s in states]

# print "MAXLEN:", max(len(choice[0]) for choice in choices)

transitions = {
    'initial':                  ['started'],
    # 'started':                  ['tool-validated'],
    # 'tool-validated':           ['authenticated', 'err'],
    'authenticated':            ['authorized', 'err'],
    'authorized':               ['start-tk-sent', 'err'],

    # communication 1: server sends a start token to the client
    # 'start-tk-sent':            ['start-tk-sent-ok', 'start-tk-sent-err'],
    # 'start-tk-sent-ok':         ['start-tk-received'],

    'start-tk-sent':            ['start-tk-received'],

    # communication 2: client returns start token
    'start-tk-received':        ['start-tk-ok', 'start-tk-err'],
    'start-tk-ok':              ['start-data-sent'],

    # communication 3: server sends start data to client
    'start-data-sent':          ['start-data-sent-ok', 'start-data-sent-err'],
    'start-data-sent-ok':       ['tool-timeout-err', 'result-tk-received'],

    # communication 4: client sends result token to server
    'result-tk-received':       ['result-tk-sent'],

    # communication 5: server returns result token to client
    'result-tk-sent':           ['result-received-ok', 'result-received-err'],

    # communication 6: client returns result data to server
    'result-received-ok':       ['result-saved'],
    'result-saved':             ['finished-ok'],
    'start-tk-sent-err':        ['finished-err'],
    'start-tk-err':             ['finished-err'],
    'start-data-sent-err':      ['finished-err'],
    'result-received-err':      ['finished-err'],


    'err':                      [],
}


if True:  # settings.DEBUG:
    def _validate_state_transitions(transitions, states):
        allstates = set()
        lhs = set()
        rhs = set()

        for k, v in transitions.iteritems():
            allstates.add(k)
            lhs.add(k)
            for s in v:
                allstates.add(s)
                rhs.add(s)

        known_states = {s[0] for s in states}
        if known_states ^ allstates:
            print "states vs tr.states:", known_states ^ allstates
            assert {s[0] for s in states} == allstates
        print "lhs - rhs:", lhs - rhs
        assert lhs - rhs == {'initial'}
        print "rhs - lhs:", rhs - lhs
        print allstates

    # _validate_state_transitions(transitions, states)

