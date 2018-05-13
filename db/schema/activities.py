
from .. import pg, sa, metadata

t_activities = sa.Table('activities', metadata,
	sa.Column('activity_id', pg.UUID, primary_key=True, autoincrement=False, server_default=sa.text('uuid_generate_v4()'), key=u'activityId', doc=''),
	sa.Column('name', pg.TEXT, nullable=False, key=u'name', doc=''),
	sa.Column('info', pg.TEXT, key=u'info', doc=''),
	sa.Column('capacity', pg.INTEGER, key=u'capacity', doc=''),
	sa.Column('venue_id', pg.UUID, nullable=False, key=u'venueId', doc=''),
	sa.Column('provider_id', pg.UUID, nullable=False, key=u'providerId', doc=''),
	sa.Column('created_at', pg.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'createdAt', doc=''),
	sa.ForeignKeyConstraint([u'venueId'], [u'venues.venueId']),
	sa.ForeignKeyConstraint([u'providerId'], [u'users.userId']),
)
