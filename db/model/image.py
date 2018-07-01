
from ._std import *

_names = set(locals().keys()) | {'_names'}

##########################################################################


# Image
class Image(Base):
	__table__ = t_images

class ImageSchema(Schema):
	class Meta:
		fields = ('imageId', 'mimeType')

##########################################################################

__all__ = list(set(locals().keys()) - _names)
