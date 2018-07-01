#!/usr/bin/env python

import os
import glob

from sqlalchemy.ext.declarative import declarative_base

from .. import database, mode
from ..db import SS
from ..db import database as db
from ..schema import metadata

def set_schema(cls, schema_class, schema_key=None):
	if not issubclass(schema_class, Schema):
		raise TypeError('schema must be subclass of Schema')
	registry = cls.__dict__.get('_schema_registry', None)
	if registry is None:
		cls._schema_registry = {}
	cls._schema_registry[schema_key] = schema_class


def dump(cls, obj, use=None, extra=None, only=(), exclude=(),
		prefix=u'', strict=False, context=None, load_only=(), **kwargs):
	try:
		schema_class = cls._schema_registry.get(use, None)
	except:
		schema_class = None
	if schema_class is None:
		raise RuntimeError('schema class not found for {0}: key {1}'\
			.format(cls.__name__, use))
	s = schema_class(extra=extra, only=only, exclude=exclude,
			prefix=prefix, strict=strict, context=context)
	if isinstance(obj, list):
		many = True
	else:
		many = False
	marshal_result = s.dump(obj, many=many, **kwargs)
	return marshal_result.data

if mode == 'app':
	Base = database.Model
else:
	class MyBase(object):
		pass
	Base = declarative_base(cls=MyBase, metadata=metadata)
	Base.query = SS.query_property()

Base.set_schema = classmethod(set_schema)
Base.dump = classmethod(dump)


_package_name = __name__

_names = set(locals().keys()) | {'_names'}

##########################################################################

__all__ = []


for _ in glob.glob(os.path.join(os.path.dirname(__file__), '*.py')):
	_basename = os.path.basename(_)	# e.g. _std.py/activity.py/baby.py/provider.py
	if _basename.startswith('_'):	# e.g. _std.py
		continue
	_mod_name = _basename.split('.')[0]	# activity/baby/
	_mod = _package_name + '.' + _mod_name	# db.model1.activity
	try:
		_temp = __import__(_mod, globals(), locals(), ['*'], 0)
	except:
		print(dict(_baseame=_basename, _mod_name=_mod_name, _mod=_mod))
		raise
	for _name in dir(_temp):
		locals()[_name] = getattr(_temp, _name)
	__all__.append(_name)

del os, glob

##########################################################################

for schema_name in [i for i in __all__ if i.endswith('Schema')]:
	klass_name = schema_name[:-6]
	if klass_name.find('_') >= 0:
		klass_name, schema_key = klass_name.split('_', 1)
		schema_key = schema_key.lower()
	else:
		schema_key = ''
	assert klass_name
	klass = locals()[klass_name]
	schema = locals()[schema_name]
	klass.set_schema(schema, schema_key or None)
