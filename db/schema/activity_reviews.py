
from .. import pg, sa, metadata

t_activity_reviews = sa.Table('activity_reviews', metadata,
	sa.Column('review_id', pg.UUID, nullable=False, key=u'reviewId', doc=''),
	sa.Column('activity_id', pg.UUID, nullable=False, key=u'activityId', doc=''),
	sa.Column('reviewer_id', pg.UUID, nullable=False, key=u'reviewerId', doc=''),
	sa.Column('stars', pg.SMALLINT, nullable=False, key=u'stars', doc=''),
	sa.Column('content', pg.TEXT, nullable=False, key=u'content', doc=''),
	sa.Column('created_at', pg.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'createdAt', doc=''),
	sa.PrimaryKeyConstraint(u'reviewId'),
	sa.ForeignKeyConstraint([u'activityId'], [u'activities.activityId']),
	sa.ForeignKeyConstraint([u'reviewerId'], [u'users.userId']),
)
