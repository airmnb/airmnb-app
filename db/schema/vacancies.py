
from .. import pg, sa, metadata

t_vacancies = sa.Table('vacancies', metadata,
	sa.Column('vacancy_id', pg.UUID, primary_key=True, autoincrement=False, server_default=sa.text('uuid_generate_v4()'), key=u'vacancyId', doc=''),
	sa.Column('activity_id', pg.UUID, nullable=False, key=u'activityId', doc=''),
	sa.Column('timeslot_id', pg.UUID, nullable=False, key=u'timeslotId', doc=''),
	sa.Column('purchase_id', pg.UUID, nullable=True, key=u'purchaseId', doc=''),
	sa.Column('booked_at', pg.TIMESTAMP(timezone=True), nullable=True, key=u'bookedAt', doc=''),
	sa.ForeignKeyConstraint([u'activityId'], [u'activities.activityId']),
	sa.ForeignKeyConstraint([u'timeslotId'], [u'timeslots.timeslotId']),
	sa.ForeignKeyConstraint([u'purchaseId'], [u'purchases.purchaseId']),
)
