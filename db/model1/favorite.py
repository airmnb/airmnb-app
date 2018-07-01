
from ._std import *

_names = set(locals().keys()) | {'_names'}

##########################################################################

# Favorite
class Favorite(Base):
	__table__ = t_favorites


class FavoriteSchema(Schema):
	class Meta:
		fields = ('favoriteId', 'activityId', 'providerId', 'consumerId')


##########################################################################

__all__ = list(set(locals().keys()) - _names)
