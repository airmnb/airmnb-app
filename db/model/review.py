
from ._std import *

from .tag import Tag

_names = set(locals().keys()) | {'_names'}

##########################################################################

# Review
class ActivityReview(Base):
	__table__ = t_activity_reviews


class ActivityReviewSchema(Schema):
	reviewer = fields.Nested('UserSchema')
	class Meta:
		fields = ('reviewId', 'activityId', 'reviewer', 'stars', 'content', 'createdAt')
	

# ActivityResponse
class ActivityResponse(Base):
	__table__ = t_activity_responses


class ActivityResponseSchema(Schema):
	class Meta:
		fields = ('responseId', 'reviewId', 'activityId', 'providerId', 'content', 'createdAt')


##########################################################################

__all__ = list(set(locals().keys()) - _names)
