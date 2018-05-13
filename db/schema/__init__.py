
import os
import glob

__all__ = []

for _ in glob.glob(os.path.join(os.path.dirname(__file__), '*.py')):
	_basename = os.path.basename(_)
	if _basename.startswith('_'):
		continue
	_mod_name = _basename.split('.')[0]
	_mod = __name__ + '.' + _mod_name
	_t_name = 't_' + _mod_name
	_temp = __import__(_mod, globals(), locals(), [_t_name], 0)
	locals()[_t_name] = getattr(_temp, _t_name)
	__all__.append(_t_name)

del os, glob

##########################################################################
