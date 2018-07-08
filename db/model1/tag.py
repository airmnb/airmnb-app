
from ._std import *

_names = set(locals().keys()) | {'_names'}

##########################################################################

# Tag
class Tag(Base):
	__table__ = t_tags


class TagSchema(Schema):
	class Meta:
		fields = ('tagId', 'name', 'description')


##########################################################################

__all__ = list(set(locals().keys()) - _names)
