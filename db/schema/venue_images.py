
from .. import pg, sa, metadata

t_venue_images = sa.Table('venue_images', metadata,
	sa.Column('venue_id', pg.UUID, nullable=False, key=u'venueId', doc=''),
	sa.Column('image_id', pg.UUID, nullable=False, key=u'imageId', doc=''),
	sa.ForeignKeyConstraint([u'venueId'], [u'venues.venueId']),
	sa.ForeignKeyConstraint([u'imageId'], [u'images.imageId']),
)
