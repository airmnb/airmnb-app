
from .. import pg, sa, metadata

t_activity_tags = sa.Table('activity_tags', metadata,
	sa.Column('activity_id', pg.UUID, nullable=False, key=u'activityId', doc=''),
	sa.Column('tag_id', pg.INTEGER, nullable=False, key=u'tagId', doc=''),
	sa.PrimaryKeyConstraint(u'activityId', u'tagId'),
	sa.ForeignKeyConstraint([u'activityId'], [u'activities.activityId']),
	sa.ForeignKeyConstraint([u'tagId'], [u'tags.tagId']),
)
