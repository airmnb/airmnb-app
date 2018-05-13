
from .. import pg, sa, metadata

t_timeslots = sa.Table('timeslots', metadata,
	sa.Column('timeslot_id', pg.UUID, primary_key=True, autoincrement=False, server_default=sa.text('uuid_generate_v4()'), key=u'timeslotId', doc=''),
	sa.Column('activity_id', pg.UUID, nullable=False, key=u'activityId', doc=''),
	sa.Column('start', pg.TIMESTAMP(timezone=True), nullable=False, key=u'start', doc=''),
	sa.Column('end', pg.TIMESTAMP(timezone=True), nullable=False, key=u'end', doc=''),
	sa.ForeignKeyConstraint([u'activityId'], [u'activities.activityId']),
)
