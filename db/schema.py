
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

metadata = sa.MetaData()


##########################################################################
# Amb user account, it's also a customer account. We assume every account can be a consumer.
t_users = sa.Table('users', metadata,
	sa.Column('user_id', pg.UUID, primary_key=True, autoincrement=False, server_default=sa.text('uuid_generate_v4()'), key=u'userId', doc=''),
	sa.Column('account_name', pg.TEXT, nullable=True, unique=True, key=u'accountName', doc=''),
	sa.Column('password', pg.TEXT, nullable=True, key=u'password', doc=''),
	sa.Column('source', pg.SMALLINT, nullable=False, key=u'source', doc='local 1, Facebook: 4, WeChat: 6, WeApp: 8, Google: 9'),
	sa.Column('email', pg.TEXT, nullable=True, key=u'email', doc=''),
	sa.Column('phone', pg.TEXT, nullable=True, key=u'phone', doc=''),
	sa.Column('family_name', pg.TEXT, nullable=True, key=u'familyName', doc=''),
	sa.Column('given_name', pg.TEXT, nullable=True, key=u'givenName', doc=''),
	sa.Column('full_name', pg.TEXT, nullable=True, key=u'fullName', doc=''),
	sa.Column('gender', pg.BOOLEAN, nullable=True, key=u'gender', doc=''),
	sa.Column('dob', pg.DATE, nullable=True, key=u'dob', doc=''),
	sa.Column('avatar_image_id', pg.UUID, nullable=True, key=u'avatarImageId', doc=''),
	sa.Column('last_access_at', pg.TIMESTAMP(timezone=True), nullable=False, key=u'lastAccessAt', doc=''),
	sa.Column('created_at', pg.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'createdAt', doc=''),
	sa.ForeignKeyConstraint([u'avatarImageId'], [u'images.imageId']),
)

# Extension table if a user account is signed up from weapp
t_wechat_users = sa.Table('wechat_users', metadata,
	sa.Column('wechat_user_id', pg.UUID, primary_key=True, autoincrement=False, server_default=sa.text('uuid_generate_v4()'), key=u'wechatUserId', doc=''),
	sa.Column('open_id', pg.TEXT, nullable=False, key=u'openId', doc=''),
	sa.Column('avatar_url', pg.TEXT, nullable=True, key=u'avatarUrl', doc=''),
	sa.Column('created_at', pg.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'createdAt', doc=''),
)

# Extension table if a user is a provider
t_providers = sa.Table('providers', metadata,
	sa.Column('provider_id', pg.UUID, primary_key=True, key=u'providerId', doc=''),
	sa.Column('certificates', pg.TEXT, nullable=True, key=u'certificates', doc=''),
	sa.Column('info', pg.TEXT, nullable=False, key=u'info', doc=''),
	sa.Column('created_at', pg.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'createdAt', doc=''),
	sa.ForeignKeyConstraint([u'providerId'], [u'users.userId']),
)

t_babies = sa.Table('babies', metadata,
	sa.Column('baby_id', pg.UUID, primary_key=True, autoincrement=False, server_default=sa.text('uuid_generate_v4()'), key=u'babyId', doc=''),
	sa.Column('family_name', pg.TEXT, nullable=True, key=u'familyName', doc=''),
	sa.Column('given_name', pg.TEXT, nullable=True, key=u'givenName', doc=''),
	sa.Column('nick_name', pg.TEXT, nullable=True, key=u'nickName', doc=''),
	sa.Column('full_name', pg.TEXT, nullable=True, key=u'fullName', doc=''),
	sa.Column('gender', pg.TEXT, key=u'gender', doc=''),
	sa.Column('dob', pg.DATE, nullable=True, key=u'dob', doc=''),
	sa.Column('creator_id', pg.UUID, nullable=False, key=u'creatorId', doc=''),
	sa.Column('info', pg.TEXT, nullable=True, key=u'info', doc=''),
	sa.Column('avatar_image_id', pg.UUID, nullable=True, key=u'avatarImageId', doc=''),
	sa.Column('created_at', pg.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'createdAt', doc=''),
	sa.ForeignKeyConstraint([u'creatorId'], [u'users.userId']),
	sa.ForeignKeyConstraint([u'avatarImageId'], [u'images.imageId']),
)

t_venues = sa.Table('venues', metadata,
	sa.Column('venue_id', pg.UUID, primary_key=True, autoincrement=False, server_default=sa.text('uuid_generate_v4()'), key=u'venueId', doc=''),
	sa.Column('name', pg.TEXT, nullable=False, key=u'name', doc=''),
	sa.Column('longitude', pg.DOUBLE_PRECISION, nullable=True, key=u'longitude', doc=''),
	sa.Column('latitude', pg.DOUBLE_PRECISION, nullable=True, key=u'latitude', doc=''),
	sa.Column('addr1', pg.TEXT, nullable=False, key=u'addr1', doc=''),
	sa.Column('addr2', pg.TEXT, key=u'addr2', doc=''),
	sa.Column('addr3', pg.TEXT, key=u'addr3', doc=''),
	sa.Column('city', pg.TEXT, nullable=False, key=u'city', doc=''),
	sa.Column('state', pg.TEXT, nullable=False, key=u'state', doc=''),
	sa.Column('country', pg.TEXT, nullable=False, key=u'country', doc=''),
	sa.Column('postcode', pg.TEXT, key=u'postcode', doc=''),
	sa.Column('info', pg.TEXT, key=u'info', doc=''),
	sa.Column('provider_id', pg.UUID, nullable=False, key=u'providerId', doc=''),
	sa.Column('created_at', pg.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'createdAt', doc=''),
	sa.ForeignKeyConstraint([u'providerId'], [u'users.userId']),
)

# t_venues_images = sa.Table('venues_images', metadata,
# 	sa.Column('venue_id', pg.UUID, nullable=False, key=u'venueId', doc=''),
# 	sa.Column('image_id', pg.UUID, nullable=False, key=u'imageId', doc=''),
# 	sa.ForeignKeyConstraint([u'venueId'], [u'venues.venueId']),
# 	sa.ForeignKeyConstraint([u'imageId'], [u'images.imageId']),
# )

t_activities = sa.Table('activities', metadata,
	sa.Column('activity_id', pg.UUID, primary_key=True, autoincrement=False, server_default=sa.text('uuid_generate_v4()'), key=u'activityId', doc=''),
	sa.Column('name', pg.TEXT, nullable=False, key=u'name', doc=''),
	sa.Column('description', pg.TEXT, key=u'description', doc=''),
	sa.Column('venue_id', pg.UUID, nullable=False, key=u'venueId', doc=''),
	sa.ForeignKeyConstraint([u'venueId'], [u'venues.venueId']),
)

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

t_images = sa.Table('images', metadata,
	sa.Column('image_id', pg.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()'), key=u'imageId', doc=''),
	sa.Column('blob', pg.BYTEA, nullable=False, key=u'blob', doc=''),
	sa.Column('mime', pg.TEXT, nullable=True, key=u'mimeType', doc=''),
	sa.Column('linked', pg.BOOLEAN, nullable=False, server_default=sa.text('False'), key=u'linked', doc=''),
	sa.Column('created_at', pg.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'createdAt', doc=''),
)

##########################################################################


__all__ = [name for name in locals().keys()
		if name.startswith('t_') or name.startswith('j_')]
__all__.insert(0, 'metadata')
