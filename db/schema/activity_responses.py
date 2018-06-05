
from .. import pg, sa, metadata

t_activity_responses = sa.Table('activity_responses', metadata,
	sa.Column('response_id', pg.UUID, nullable=False, server_default=sa.text('uuid_generate_v4()'), key=u'responseId', doc=''),
	sa.Column('review_id', pg.UUID, nullable=False, key=u'reviewId', doc=''),
	sa.Column('activity_id', pg.UUID, nullable=False, key=u'activityId', doc=''),
	sa.Column('provider_id', pg.UUID, nullable=False, key=u'providerId', doc=''),
	sa.Column('content', pg.TEXT, nullable=False, key=u'content', doc=''),
	sa.Column('created_at', pg.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'createdAt', doc=''),
	sa.PrimaryKeyConstraint(u'responseId'),
	sa.ForeignKeyConstraint([u'reviewId'], [u'activity_reviews.reviewId']),
	sa.ForeignKeyConstraint([u'activityId'], [u'activities.activityId']),
	sa.ForeignKeyConstraint([u'providerId'], [u'users.userId']),
)
