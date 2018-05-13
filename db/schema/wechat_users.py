
from .. import pg, sa, metadata

# Extension table if a user account is signed up from weapp
t_wechat_users = sa.Table('wechat_users', metadata,
	sa.Column('wechat_user_id', pg.UUID, primary_key=True, autoincrement=False, server_default=sa.text('uuid_generate_v4()'), key=u'wechatUserId', doc=''),
	sa.Column('open_id', pg.TEXT, nullable=False, key=u'openId', doc=''),
	sa.Column('avatar_url', pg.TEXT, nullable=True, key=u'avatarUrl', doc=''),
	sa.Column('created_at', pg.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'createdAt', doc=''),
)
