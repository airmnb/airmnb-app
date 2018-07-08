
from ._std import *

_names = set(locals().keys()) | {'_names'}

##########################################################################

# Venue
class Venue(Base):
	__table__ = t_venues

class VenueSchema(Schema):
	class Meta:
		fields = ('venueId', 'name', 'longitude', 'latitude', 'addr1', 'addr2', 
		'addr3', 'city', 'state', 'country', 'postcode', 'info', 'providerId', 'createdAt')


##########################################################################

__all__ = list(set(locals().keys()) - _names)
