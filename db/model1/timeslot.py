
from ._std import *

_names = set(locals().keys()) | {'_names'}

##########################################################################

# Timeslot
class Timeslot(Base):
	__table__ = t_timeslots
	vacancies = relationship('Vacancy')
	TIME_ADVANCE = timedelta(hours=1)
	@property
	def is_bookable(self):
		return (self.start - self.TIME_ADVANCE) >= now
	@property
	def is_available(self):
		return any([not v.isBooked for v in self.vacancies])


class TimeslotSchema(Schema):
	vacancyIds = fields.Method('get_vacancy_ids')
	def get_vacancy_ids(self, obj):
		return [v.vacancyId for v in obj.vacancies]
	date = fields.Method('get_date')
	def get_date(self, obj):
		return obj.start.strftime("%Y-%m-%d")
	class Meta:
		fields = ('timeslotId', 'date', 'vacancyIds')


##########################################################################

__all__ = list(set(locals().keys()) - _names)
