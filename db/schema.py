
import uuid

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

metadata = sa.MetaData()


##########################################################################

t_wechat_users = sa.Table('wechat_users', metadata,
	sa.Column('id', pg.UUID, primary_key=True, autoincrement=False, key=u'id', doc=''),
	sa.Column('openid', pg.TEXT, nullable=False, key=u'openId', doc=''),
	sa.Column('avartar_url', pg.TEXT, nullable=True, key=u'avartarUrl', doc=''),
	sa.Column('created_at', pg.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'createdAt', doc=''),
)

t_users = sa.Table('users', metadata,
	sa.Column('id', pg.UUID, primary_key=True, autoincrement=False,
			default=lambda: str(uuid.uuid4()), key=u'id', doc=''),
	sa.Column('email', pg.TEXT, nullable=True, key=u'email', doc=''),
	sa.Column('nick_name', pg.TEXT, nullable=True, key=u'nickName', doc=''),
	sa.Column('family_name', pg.TEXT, nullable=True, key=u'familyName', doc=''),
	sa.Column('given_name', pg.TEXT, nullable=True, key=u'givenName', doc=''),
	sa.Column('full_name', pg.TEXT, nullable=True, key=u'fullName', doc=''),
	sa.Column('gender', pg.TEXT, nullable=True, key=u'gender', doc=''),
	sa.Column('dob', pg.DATE, nullable=True, key=u'dob', doc=''),
	sa.Column('created_at', pg.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'), key=u'createdAt', doc=''),
)

t_babies = sa.Table('babies', metadata,
	sa.Column('id', pg.UUID, primary_key=True, autoincrement=False, key=u'babyId', doc=''),
	sa.Column('family_name', pg.TEXT, nullable=True, key=u'familyName', doc=''),
	sa.Column('given_name', pg.TEXT, nullable=True, key=u'givenName', doc=''),
	sa.Column('full_name', pg.TEXT, nullable=True, key=u'fullName', doc=''),
	sa.Column('gender', pg.TEXT, key=u'gender', doc=''),
	sa.Column('dob', pg.DATE, nullable=False, key=u'dob', doc=''),
	sa.Column('parent_id', pg.UUID, nullable=False, key=u'parentId', doc=''),
	sa.Column('created_at', pg.TIMESTAMP(timezone=True), nullable=False, key=u'createdAt', doc=''),
	sa.ForeignKeyConstraint([u'parentId'], [u'users.id']),
)


t_locations = sa.Table('locations', metadata,
	sa.Column('id', pg.UUID, primary_key=True, autoincrement=False, key=u'locationId', doc=''),
	sa.Column('langitude', pg.DOUBLE_PRECISION, nullable=False, key=u'langitude', doc=''),
	sa.Column('latitude', pg.DOUBLE_PRECISION, nullable=False, key=u'latitude', doc=''),
	sa.Column('addr1', pg.TEXT, nullable=False, key=u'addr1', doc=''),
	sa.Column('addr2', pg.TEXT, key=u'addr2', doc=''),
	sa.Column('addr3', pg.TEXT, key=u'addr3', doc=''),
	sa.Column('city', pg.TEXT, nullable=False, key=u'city', doc=''),
	sa.Column('state', pg.TEXT, nullable=False, key=u'state', doc=''),
	sa.Column('country', pg.TEXT, nullable=False, key=u'country', doc=''),
	sa.Column('postcode', pg.TEXT, key=u'postcode', doc=''),
)


t_activities = sa.Table('activities', metadata,
	sa.Column('id', pg.UUID, primary_key=True, autoincrement=False, key=u'activityId', doc=''),
	sa.Column('name', pg.TEXT, nullable=False, key=u'name', doc=''),
	sa.Column('description', pg.TEXT, key=u'description', doc=''),
	sa.Column('location_id', pg.UUID, nullable=False, key=u'locationId', doc=''),
	sa.ForeignKeyConstraint([u'locationId'], [u'locations.locationId']),
)


##########################################################################


__all__ = [name for name in locals().keys()
		if name.startswith('t_') or name.startswith('j_')]
__all__.insert(0, 'metadata')
