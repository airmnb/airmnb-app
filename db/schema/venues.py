
from .. import pg, sa, metadata

t_venues = sa.Table('venues', metadata,
	sa.Column('venue_id', pg.UUID, primary_key=True, autoincrement=False, server_default=sa.text('uuid_generate_v4()'), key=u'venueId', doc=''),
	sa.Column('name', pg.TEXT, nullable=False, key=u'name', doc=''),
	sa.Column('longitude', pg.DOUBLE_PRECISION, nullable=False, key=u'longitude', doc=''),
	sa.Column('latitude', pg.DOUBLE_PRECISION, nullable=False, key=u'latitude', doc=''),
	sa.Column('map_service', pg.TEXT, nullable=True, key=u'mapService', doc=''),
	sa.Column('addr1', pg.TEXT, nullable=False, key=u'addr1', doc=''),
	sa.Column('addr2', pg.TEXT, key=u'addr2', doc=''),
	sa.Column('addr3', pg.TEXT, key=u'addr3', doc=''),
	sa.Column('city', pg.TEXT, nullable=False, key=u'city', doc=''),
	sa.Column('state', pg.TEXT, nullable=False, key=u'state', doc=''),
	sa.Column('country', pg.TEXT, nullable=False, key=u'country', doc=''),
	sa.Column('postcode', pg.TEXT, key=u'postcode', doc=''),
	sa.Column('info', pg.TEXT, key=u'info', doc=''),
	sa.Column('provider_id', pg.UUID, nullable=False, key=u'providerId', doc=''),
	sa.Column('created_at', pg.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'createdAt', doc=''),
	sa.ForeignKeyConstraint([u'providerId'], [u'users.userId']),
)
