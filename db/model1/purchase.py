
from ._std import *

_names = set(locals().keys()) | {'_names'}

##########################################################################

# Purchase
class Purchase(Base):
	__table__ = t_purchases
	activity = relationship('Activity')
	vacancies = relationship('Vacancy')
	baby = relationship('Baby')


class PurchaseSchema(Schema):
	activity = fields.Nested('ActivitySchema')
	vacancies = fields.Nested('VacancySchema', many=True)
	baby = fields.Nested('BabySchema')
	class Meta:
		fields = ('purchaseId', 'providerId', 'startDate', 'endDate', 'bookedBy', 'activity', 'vacancies', 'baby')


##########################################################################

__all__ = list(set(locals().keys()) - _names)
