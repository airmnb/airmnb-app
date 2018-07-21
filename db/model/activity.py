
from ._std import *

from .tag import Tag

_names = set(locals().keys()) | {'_names'}

##########################################################################

# Activity
class Activity(Base):
	__table__ = t_activities
	venue = relationship('Venue')
	provider = relationship('User')
	images = relationship('ActivityImage')
	timeslots = relationship('Timeslot')
	@property
	def isActive(self):
		return self.endDate >= datetime.datetime.now().date()
	
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
	startTime = fields.Method('get_starttime_literal')
	endTime = fields.Method('get_endtime_literal')
	def get_starttime_literal(self, obj):
		return obj.startTime.strftime("%H:%M")
	def get_endtime_literal(self, obj):
		return obj.endTime.strftime("%H:%M")
	class Meta:
		fields = ('activityId', 'name', 'info', 'category', 'minAge', 'maxAge',
			'daysOfWeek', 'capacity', 'gender', 'daysOfWeek',
			'startDate', 'startTime', 'endDate', 'endTime',
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


# # ActivityReview
# class ActivityReview(Base):
# 	__table__ = t_activity_reviews


# class ActivityReviewSchema(Schema):
# 	class Meta:
# 		fields = ('reviewId', 'activityId', 'reviewerId', 'stars', 'content', 'createdAt')
	

# # ActivityResponse
# class ActivityResponse(Base):
# 	__table__ = t_activity_responses


# class ActivityResponseSchema(Schema):
# 	class Meta:
# 		fields = ('responseId', 'reviewId', 'activityId', 'providerId', 'content', 'createdAt')


##########################################################################

__all__ = list(set(locals().keys()) - _names)
