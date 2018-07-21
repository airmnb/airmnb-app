
from ._std import *

_names = set(locals().keys()) | {'_names'}

##########################################################################

# User
class User(Base):
	__table__ = t_users


class UserSchema(Schema):
	class Meta:
		# password (encryption) and salt must never be dumped
		fields = ('userId','accountName', 'source',
			'email', 'phone', 'familyName', 'givenName', 'fullName', 'language',
			'gender', 'dob', 'lastAccessAt', 'createdAt')
		exclude = ('password', 'salt')

class User_SimpleSchema(Schema):
	class Meta:
		fields = ('userId', 'fullName')

##########################################################################

__all__ = list(set(locals().keys()) - _names)
