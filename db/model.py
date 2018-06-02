#!/usr/bin/env python

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import relationship, backref, synonym, deferred, column_property, object_session
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql import case, text, func
from sqlalchemy.types import Integer, String
from marshmallow import Schema, fields

from . import database, mode
from .db import SS
from .db import database as db
from .schema import *


def set_schema(cls, schema_class, schema_key=None):
	if not issubclass(schema_class, Schema):
		raise TypeError('schema must be subclass of Schema')
	registry = cls.__dict__.get('_schema_registry', None)
	if registry is None:
		cls._schema_registry = {}
	cls._schema_registry[schema_key] = schema_class


def dump(cls, obj, use=None, extra=None, only=(), exclude=(),
		prefix=u'', strict=False, context=None, load_only=(), **kwargs):
	try:
		schema_class = cls._schema_registry.get(use, None)
	except:
		schema_class = None
	if schema_class is None:
		raise RuntimeError('schema class not found for {0}: key {1}'\
			.format(cls.__name__, use))
	s = schema_class(extra=extra, only=only, exclude=exclude,
			prefix=prefix, strict=strict, context=context)
	if isinstance(obj, list):
		many = True
	else:
		many = False
	marshal_result = s.dump(obj, many=many, **kwargs)
	return marshal_result.data

if mode == 'app':
	Base = database.Model
else:
	class MyBase(object):
		pass
	Base = declarative_base(cls=MyBase, metadata=metadata)
	Base.query = SS.query_property()

Base.set_schema = classmethod(set_schema)
Base.dump = classmethod(dump)


_names = set(locals().keys()) | {'_names'}


#
# Define model class and its schema (if needed) below
#
##########################################################################

# User
class User(Base):
	__table__ = t_users


class UserSchema(Schema):
	class Meta:
		# password (encryption) and salt must never be dumped
		fields = ('userId','accountName', 'source',
			'email', 'phone', 'familyName', 'givenName', 'fullName', 'language',
			'gender', 'dob', 'lastAccessAt', 'createdAt')
		exclude = ('password', 'salt')

# WechatUser
class WechatUser(Base):
	__table__ = t_wechat_users

class WechatUserSchema(Schema):
	class Meta:
		fields = ('wechatUserId', 'openId', 'avatarUrl', 'createdAt')

# Provider
class Provider(Base): 
	__table__ = t_providers

class ProviderSchema(Schema):
	class Meta:
		fields = ('providerId', 'certificates', 'info', 'createdAt')

# Baby
class Baby(Base):
	__table__ = t_babies


class BabySchema(Schema):
	class Meta:
		fields = ('babyId', 'nickName', 'familyName', 'givenName', 'fullName',
		 'gender', 'dob', 'creatorId', 'info', 'avatarImageId', 'createdAt')

# Venue
class Venue(Base):
	__table__ = t_venues

class VenueSchema(Schema):
	class Meta:
		fields = ('venueId', 'name', 'longitude', 'latitude', 'addr1', 'addr2', 
		'addr3', 'city', 'state', 'country', 'postcode', 'info', 'providerId', 'createdAt')


# Activity
class Activity(Base):
	__table__ = t_activities
	venue = relationship('Venue')
	provider = relationship('User')
	images = relationship('ActivityImage')
	timeslots = relationship('Timeslot')
	@property
	def tags(self):
		return SS.query(Tag).filter(
			Tag.tagId.in_(SS.query(ActivityTag.tagId
				).filter(ActivityTag.activityId==self.acvitityId))
			).order_by(Tag.tagId).all()

class ActivitySchema(Schema):
	venue = fields.Nested('VenueSchema')
	# provider = fields.Nested('UserSchema')
	tags = fields.Nested('TagSchema')
	imageIds = fields.Method('get_image_ids')
	def get_image_ids(self, obj):
		return [i.imageId for i in obj.images]
	class Meta:
		fields = ('activityId', 'name', 'info', 'category', 'minAge', 'maxAge',
			'daysOfWeek', 'capacity', 'gender', 'daysOfWeek',
			'venue', 'price', 'tags', 'imageIds', 'status')


# ActivityImage
class ActivityImage(Base):
	__table__ = t_activity_images

class ActivityImageSchema(Schema):
	class Meta:
		fields = ('imageId', 'activityId')


# ActivityTag
class ActivityTag(Base):
	__table__ = t_activity_tags


# Timeslot
class Timeslot(Base):
	__table__ = t_timeslots
	vacancies = relationship('Vacancy')


class TimeslotSchema(Schema):
	activity = fields.Nested('Activity')
	timeslot = fields.Nested('Timeslot')
	bookedBy = fields.Nested('User')
	class Meta:
		fields = ('vacancyId', 'activity', 'timeslot', 'bookedBy', 'bookedAt')

# Vacancy
class Vacancy(Base):
	__table__ = t_vacancies


# Session
class Session(Base):
	__table__ = t_sessions
	user = relationship(User)


class SessionSchema(Schema):
	class Meta:
		fields = ('sessionId', 'userId', 'accessToken', 'refreshToken')


# Image
class Image(Base):
	__table__ = t_images

class ImageSchema(Schema):
	class Meta:
		fields = ('imageId', 'mimeType')

# Tag
class Tag(Base):
	__table__ = t_tags

class TagSchema(Schema):
	class Meta:
		fields = ('tagId', 'name', 'description')



##########################################################################
#
# Define model class and its schema (if needed) above
#

__all__ = list(set(locals().keys()) - _names)

for schema_name in [i for i in __all__ if i.endswith('Schema')]:
	klass_name = schema_name[:-6]
	if klass_name.find('_') >= 0:
		klass_name, schema_key = klass_name.split('_', 1)
		schema_key = schema_key.lower()
	else:
		schema_key = ''
	assert klass_name
	klass = locals()[klass_name]
	schema = locals()[schema_name]
	klass.set_schema(schema, schema_key or None)
