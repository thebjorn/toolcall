# -*- coding: utf-8 -*-
import inspect


class pset(dict):
    def __init__(self):
        self.__dict__ = self


class C2PMetaclass(type):
    """Convert a class to a pset.
    """
    @staticmethod
    def _classdict(cls):
        return {k: getattr(cls, k) for k in dir(cls)}

    @staticmethod
    def cls2pset(dct):
        "Convert class `cls` to a pset."
        res = pset()

        for attr in [a for a in dct if not a.startswith('_')]:
            value = dct[attr]
            if inspect.isclass(value):
                value = C2PMetaclass.cls2pset(C2PMetaclass._classdict(value))
            res[attr] = value

        if '__doc__' in dct and dct['__doc__'] and 'description' not in res:
            res.description = u' '.join(dct['__doc__'].split())

        return res

    def __new__(cls, name, bases, dct):
        # print name, bases, dct
        if 'PluginBase' in [b.__name__ for b in bases]:  # XXX: hack
            # print "BASE\n\n\n"
            return cls.cls2pset(dct)
        return type.__new__(cls, name, bases, dct)


class PluginBase(object):
    __metaclass__ = C2PMetaclass
