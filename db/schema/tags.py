
from .. import pg, sa, metadata

t_tags = sa.Table('tags', metadata,
	sa.Column('tag_id', pg.INTEGER, primary_key=True, autoincrement=True, key=u'tagId', doc=''),
	sa.Column('name', pg.TEXT, nullable=False, key=u'name', doc=''),
	sa.Column('description', pg.TEXT, key=u'description', doc=''),
	sa.UniqueConstraint(u'name'),
)
