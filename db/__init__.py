
import sys

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from flask_sqlalchemy import SQLAlchemy

mode = 'app' if 'app' in sys.modules else 'shell'

metadata = sa.MetaData()

database = SQLAlchemy(metadata=metadata)
