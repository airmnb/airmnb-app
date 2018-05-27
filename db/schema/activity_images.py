
from .. import pg, sa, metadata

t_activity_images = sa.Table('activity_images', metadata,
	sa.Column('activity_image_id', pg.UUID, primary_key=True, autoincrement=False, key=u'imageId', doc=''),
	sa.Column('activity_id', pg.UUID, nullable=False, key=u'activityId', doc=''),
	sa.ForeignKeyConstraint([u'imageId'], [u'images.imageId']),
	sa.ForeignKeyConstraint([u'activityId'], [u'activities.activityId']),
)
