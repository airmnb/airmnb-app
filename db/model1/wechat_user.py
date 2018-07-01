
from ._std import *

_names = set(locals().keys()) | {'_names'}

##########################################################################

# WechatUser
class WechatUser(Base):
	__table__ = t_wechat_users

class WechatUserSchema(Schema):
	class Meta:
		fields = ('wechatUserId', 'openId', 'wechatNickName', 'avatarUrl', 'createdAt')

##########################################################################

__all__ = list(set(locals().keys()) - _names)
