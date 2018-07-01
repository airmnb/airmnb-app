
from ._std import *

_names = set(locals().keys()) | {'_names'}

##########################################################################

# Vacancy
class Vacancy(Base):
	__table__ = t_vacancies
	@property
	def isBooked(self):
		return self.purchaseId is not None

class VacancySchema(Schema):
	class Meta:
		fields = ('vacancyId', 'isBooked', 'activityId', 'timeslotId', 'bookedAt', 'purchaseId')

##########################################################################

__all__ = list(set(locals().keys()) - _names)
