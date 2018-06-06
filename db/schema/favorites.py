
from .. import pg, sa, metadata

t_favorites = sa.Table('favorites', metadata,
	sa.Column('favorate_id', pg.UUID, nullable=False, server_default=sa.text('uuid_generate_v4()'), key=u'favorateId', doc=''),
	sa.Column('activity_id', pg.UUID, nullable=False, key=u'activityId', doc=''),
	sa.Column('provider_id', pg.UUID, nullable=False, key=u'providerId', doc=''),
	sa.Column('consumer_id', pg.UUID, nullable=False, key=u'consumerId', doc=''),
	sa.Column('created_at', pg.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'createdAt', doc=''),
	sa.PrimaryKeyConstraint(u'favorateId'),
	sa.ForeignKeyConstraint([u'activityId'], [u'activities.activityId']),
	sa.ForeignKeyConstraint([u'providerId'], [u'users.userId']),
	sa.ForeignKeyConstraint([u'consumerId'], [u'users.userId']),
)
