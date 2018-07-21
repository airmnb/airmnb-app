
from ._std import *

from .tag import Tag

_names = set(locals().keys()) | {'_names'}

##########################################################################

# Review
class ActivityReview(Base):
	__table__ = t_activity_reviews
	reviewer = relationship('User')


class ActivityReviewSchema(Schema):
	reviewer = fields.Nested('UserSchema')
	reviewerName = fields.Method('get_reviewer_name')
	def get_reviewer_name(self, obj):
		return obj.fullName
	class Meta:
		fields = ('reviewId', 'activityId', 'reviewerName', 'stars', 'content', 'createdAt')


# ActivityResponse
class ActivityResponse(Base):
	__table__ = t_activity_responses


class ActivityResponseSchema(Schema):
	class Meta:
		fields = ('responseId', 'reviewId', 'activityId', 'providerId', 'content', 'createdAt')


##########################################################################

__all__ = list(set(locals().keys()) - _names)
