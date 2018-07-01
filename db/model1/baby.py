
from ._std import *

_names = set(locals().keys()) | {'_names'}

##########################################################################

# Baby
class Baby(Base):
	__table__ = t_babies


class BabySchema(Schema):
	class Meta:
		fields = ('babyId', 'nickName', 'familyName', 'givenName', 'fullName',
		 'gender', 'dob', 'creatorId', 'info', 'avatarImageId', 'createdAt')


##########################################################################

__all__ = list(set(locals().keys()) - _names)
