
from ._std import *

_names = set(locals().keys()) | {'_names'}

##########################################################################

# Provider
class Provider(Base): 
	__table__ = t_providers

class ProviderSchema(Schema):
	class Meta:
		fields = ('providerId', 'certificates', 'info', 'createdAt')

##########################################################################

__all__ = list(set(locals().keys()) - _names)
