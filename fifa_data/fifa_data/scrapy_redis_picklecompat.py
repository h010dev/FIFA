"""A pickle wrapper module with protocol=-1 by default."""

try:
    import cPickle as pickle  # PY2
    import json
except ImportError:
    import pickle
    import json


def loads(s):
    return json.loads(s)


def dumps(obj):
    return json.dumps(obj, protocol=-1)
