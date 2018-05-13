
from .. import pg, sa, metadata

# Amb user account, it's also a customer account. We assume every account can be a consumer.
t_users = sa.Table('users', metadata,
	sa.Column('user_id', pg.UUID, primary_key=True, autoincrement=False, server_default=sa.text('uuid_generate_v4()'), key=u'userId', doc=''),
	sa.Column('account_name', pg.TEXT, nullable=True, unique=True, key=u'accountName', doc=''),
	sa.Column('source', pg.SMALLINT, nullable=False, key=u'source', doc='local 1, Facebook: 4, WeChat: 6, WeApp: 8, Google: 9'),
	sa.Column('password', pg.BYTEA, nullable=True, key=u'password', doc='encrypted password, md5 hash of real password + salt'),
	sa.Column('salt', pg.TEXT, nullable=False, key=u'salt', doc='randomly generated text'),
	sa.Column('email', pg.TEXT, nullable=True, key=u'email', doc=''),
	sa.Column('phone', pg.TEXT, nullable=True, key=u'phone', doc=''),
	sa.Column('family_name', pg.TEXT, nullable=True, key=u'familyName', doc=''),
	sa.Column('given_name', pg.TEXT, nullable=True, key=u'givenName', doc=''),
	sa.Column('full_name', pg.TEXT, nullable=True, key=u'fullName', doc=''),
	sa.Column('gender', pg.BOOLEAN, nullable=True, key=u'gender', doc=''),
	sa.Column('dob', pg.DATE, nullable=True, key=u'dob', doc=''),
	# sa.Column('avatar_image_id', pg.UUID, nullable=True, key=u'avatarImageId', doc=''),
	sa.Column('last_access_at', pg.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'lastAccessAt', doc=''),
	sa.Column('created_at', pg.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'createdAt', doc=''),
	# sa.ForeignKeyConstraint([u'avatarImageId'], [u'images.imageId']),
)
