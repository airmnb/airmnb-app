
from .. import pg, sa, metadata

t_purchases = sa.Table('purchases', metadata,
	sa.Column('purchase_id', pg.UUID, primary_key=True, autoincrement=False, server_default=sa.text('uuid_generate_v4()'), key=u'purchaseId', doc=''),
	sa.Column('activity_id', pg.UUID, nullable=False, key=u'activityId', doc=''),
	sa.Column('provider_id', pg.UUID, nullable=False, key=u'providerId', doc=''),
	sa.Column('booked_by', pg.UUID, nullable=False, key=u'bookedBy', doc=''),
	sa.Column('status', pg.SMALLINT, nullable=False, server_default=sa.text('0'), key=u'status', doc=''),
	sa.Column('created_at', pg.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'createdAt', doc=''),
	sa.ForeignKeyConstraint([u'activityId'], [u'activities.activityId']),
	sa.ForeignKeyConstraint([u'providerId'], [u'providers.providerId']),
	sa.ForeignKeyConstraint([u'bookedBy'], [u'users.userId']),
)