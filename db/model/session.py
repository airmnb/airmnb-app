
from ._std import *

_names = set(locals().keys()) | {'_names'}

##########################################################################

# Session
class Session(Base):
	__table__ = t_sessions
	user = relationship('User')


class SessionSchema(Schema):
	class Meta:
		fields = ('sessionId', 'userId', 'accessToken', 'refreshToken')

##########################################################################

__all__ = list(set(locals().keys()) - _names)
