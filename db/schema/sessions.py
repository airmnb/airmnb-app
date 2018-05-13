
from .. import pg, sa, metadata

t_sessions = sa.Table('sessions', metadata,
	sa.Column('session_id', pg.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()'), key=u'sessionId', doc=''),
	sa.Column('session_expires_at', pg.TIMESTAMP(timezone=True), nullable=False, key=u'sessionExpiresAt', doc=''),
	sa.Column('user_id', pg.UUID, key=u'userId', doc=''),
	sa.Column('access_token', pg.TEXT, key=u'accessToken', doc=''),
	sa.Column('access_token_expires_at', pg.TIMESTAMP(timezone=True), key=u'accessTokenExpiresAt', doc=''),
	sa.Column('refresh_token', pg.TEXT, key=u'refreshToken', doc=''),
	sa.Column('created_at', pg.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'createdAt', doc=''),
	# TODo: add more fields in session
	sa.ForeignKeyConstraint([u'userId'], [u'users.userId']),
)
