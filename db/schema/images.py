
from .. import pg, sa, metadata

t_images = sa.Table('images', metadata,
	sa.Column('image_id', pg.UUID, primary_key=True, server_default=sa.text('uuid_generate_v4()'), key=u'imageId', doc=''),
	sa.Column('blob', pg.BYTEA, nullable=False, key=u'blob', doc=''),
	sa.Column('mime', pg.TEXT, nullable=True, key=u'mimeType', doc=''),
)
