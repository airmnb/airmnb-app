import os

print 'current directory', os.getcwd()
print 'PYTHONPATH', os.environ.get('PYTHONPATH')

import sys
dir=os.path.dirname(__file__)
sys.path.insert(0, dir)
sys.path.insert(0, os.path.join(dir, 'venv/lib/python2.7'))
print 'sys.path:'
print '\n'.join(sys.path) + '\n'

from app import create_app

application = create_app(os.environ.get('RUNTIME_ENVIRONMENT', 'development'))
