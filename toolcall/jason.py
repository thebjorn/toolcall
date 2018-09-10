# -*- coding: utf-8 -*-

"""Helper module to send json encoded data from Python.
   (the misspelling is intentional ;-)
"""

# pylint:disable=E0202

import decimal
import datetime
import json
import collections
import re

DJANGO = TTCAL = False
try:
    from django import http
    from django.db.models.query import QuerySet
    DJANGO = True
except ImportError:  # pragma: nocover
    pass

try:
    from dk import ttcal
    TTCAL = True
except ImportError:  # pragma: nocover
    pass

# Call JSON.parse() if dk.jason.parse() is not available
# (the re.sub() call removes all spaces, which is currently safe).
_clientparsefn = re.sub(r'\s+', "", """
    function (val) {
        return (dk && dk.jason && dk.jason.parse) ?
            dk.jason.parse(val) : JSON.parse(val)
    }
""")


# Are we sending a simple value, i.e. values that don't need the double parse
# required when sending '@type:__' encoded values?
# Currently this only checks the top level of the value.
def _is_simpleval(v):
    if isinstance(v, (int, long, decimal.Decimal)):
        return True
    if isinstance(v, basestring) and not v.startswith('@'):
        return True
    return False


class DkJSONEncoder(json.JSONEncoder):
    """Handle special cases, like Decimal...
    """

    def default(self, obj):  # pylint:disable=R0911
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if hasattr(obj, '__json__'):
            return obj.__json__()
        if isinstance(obj, set):
            return list(obj)

        if TTCAL:
            if isinstance(obj, ttcal.Year):
                return dict(year=obj.year, kind='YEAR')
            if isinstance(obj, ttcal.Duration):
                return '@duration:%d' % obj.toint()

        if isinstance(obj, datetime.datetime):
            return '@datetime:%s' % obj.isoformat()
        if isinstance(obj, datetime.date):
            return '@date:%s' % obj.isoformat()
        if isinstance(obj, datetime.time):
            return dict(hour=obj.hour,
                        minute=obj.minute,
                        second=obj.second,
                        microsecond=obj.microsecond,
                        kind="TIME")

        if DJANGO:
            if isinstance(obj, QuerySet):
                return list(obj)

        if hasattr(obj, '__dict__'):
            return dict((k, v) for k, v in obj.__dict__.items()
                        if not k.startswith('_'))

        return json.JSONEncoder.default(self, obj)


def dumps(val, indent=4, sort_keys=True, cls=DkJSONEncoder):
    """Dump json value, using our special encoder class.
    """
    return json.dumps(val, indent=indent, sort_keys=sort_keys, cls=cls)


def dump2(val, **kw):
    kw['indent'] = kw.get('indent', None)
    kw['cls'] = kw.get('cls', DkJSONEncoder)
    kw['separators'] = kw.get('separators', (',',':'))
    return json.dumps(val, **kw)


datetime_re = re.compile(r'''
    @datetime:
        (?P<year>\d{4})
        -(?P<mnth>\d\d?)
        -(?P<day>\d\d?)
        T(?P<hr>\d\d?)
        :(?P<min>\d\d?)
        :(?P<sec>\d\d?)
        (?:\.(?P<ms>\d+)Z?)?
''', re.VERBOSE)


def obj_decoder(pairs):
    def _get_tag(v):
        if isinstance(v, unicode) and v.startswith('@'):
            try:
                v = str(v)
            except UnicodeEncodeError:
                return None
            else:
                if ':' not in v:
                    return None
                tag, val = v.split(':', 1)
                return tag + ':'
        else:
            return None

    res = collections.OrderedDict()
    for key, val in pairs:
        tag = _get_tag(val)
        if tag and tag == '@datetime:':
            val = str(val)
            m = datetime_re.match(val)
            g = m.groupdict()
            val = datetime.datetime(
                int(g['year']),
                int(g['mnth']),
                int(g['day']),
                int(g['hr']),
                int(g['min']),
                int(g['sec']),
                int(g.get('ms', '0') or 0)
            )
            # val = datetime.datetime.strptime(val[len('@datetime:'):],
            #                                  '%Y-%m-%dT%H:%M:%S.%f')
        elif tag and tag == '@date:':
            val = datetime.date(
                *[int(part, 10)
                      for part in val[len('@date:'):].split('-')])
        res[key] = val
    return res


def loads(txt, **kw):
    if 'cls' not in kw:
        kw['object_pairs_hook'] = kw.get('object_pairs_hook', obj_decoder)
    return json.loads(txt, **kw)


def json_eval(txt):
    """Un-serialize json value.
    """
    return loads(txt)


def jsonname(val):
    """Convert the string in val to a valid json field name.
    """
    return val.replace('.', '_')


if DJANGO:
    def response(request, val, **kw):
        """Return a json or jsonp response.
        """
        if request.GET.get('callback'):
            return jsonp(request.GET['callback'], val, **kw)
        else:
            return jsonval(val, **kw)

    def jsonval(val, **kw):
        """Serialize val to a json HTTP response.
        """
        data = dumps(val, **kw)
        resp = http.HttpResponse(data, content_type='application/json')
        resp['Content-Type'] = 'application/json; charset=UTF-8'
        return resp

    def jsonp(callback, val, **kw):
        """Serialization with json callback.
        """
        if _is_simpleval(val):
            data = callback + '(%s)' % dump2(val, **kw)
        else:
            data = callback + '(%s(%s))' % (
                _clientparsefn,
                dump2(dump2(val, **kw)))

        return http.HttpResponse(
            data,
            content_type='application/javascript; charset=utf-8'
        )
