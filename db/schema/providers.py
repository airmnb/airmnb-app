
from .. import pg, sa, metadata

# Extension table if a user is a provider
t_providers = sa.Table('providers', metadata,
	sa.Column('provider_id', pg.UUID, primary_key=True, key=u'providerId', doc=''),
	sa.Column('certificates', pg.TEXT, nullable=True, key=u'certificates', doc=''),
	sa.Column('info', pg.TEXT, nullable=False, key=u'info', doc=''),
	sa.Column('created_at', pg.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'createdAt', doc=''),
	sa.ForeignKeyConstraint([u'providerId'], [u'users.userId']),
)
