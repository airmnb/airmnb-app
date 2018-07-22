import os

from app import create_app

runtime_env = os.environ.get('AMB_RUNTIME_ENVIRONMENT', 'production')
application = create_app(runtime_env)
