
from .. import pg, sa, metadata

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
