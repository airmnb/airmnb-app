
from flask import request, session, jsonify, g
from sqlalchemy.sql import func

import datetime
from dateutil.tz import tzoffset
import db.model as m
from db import database as db
from db.db import SS
from app.api import api, caps, MyForm, Field, validators
from app.i18n import get_text as _
from . import api_1_0 as bp, InvalidUsage

from . import _helper as helper

_name = '/' + __file__.split('/')[-1].split('.')[0]


@bp.route(_name, methods=['GET'])
@api
@caps()
def get_all_purchased_activities():
	user = g.current_user
	is_closed = request.args.get('closed', 0)
	status = 0
	if is_closed:
		status = 1
	purchases = m.Purchase.query.filter(m.Purchase.bookedBy == user.userId).order_by(m.Purchase.createdAt.desc()).all()
	# activities = [p.activity for p in purchases]
	return jsonify(purchases=m.Purchase.dump(purchases))


@bp.route(_name + '/<purchaseId>', methods=['GET'])
@api
@caps()
def get_purchase(purchaseId):
	purchase = m.Purchase.query.get(purchaseId)
	if not purchase:
		raise InvalidUsage(_('purchase {0} not found').format(purchaseId), 404)
	return jsonify(purchase=m.Purchase.dump(purchase))


def check_timeslot_ids(data, key, timeslotIds):
	activityId = data['activityId']
	vacancies = []
	for timeslotId in timeslotIds:
		timeslot = m.Timeslot.query.get(timeslotId)
		if not timeslot:
			raise ValueError(_('timeslot {} not found'.format(timeslotId)))
		if timeslot.activityId != activityId:
			raise ValueError(_('timeslot {} does not belong to activity {}').format(timeslotId, activityId))
		vacancy = m.Vacancy.query.filter(
			m.Vacancy.timeslotId==timeslotId).filter(
			m.Vacancy.activityId==activityId).filter(
			m.Vacancy.purchaseId.is_(None)).first()
		if not vacancy:
			raise ValueError(_('timeslot {} has no more vacancies').format(timeslotId))
		vacancy.bookedBy = g.current_user.userId
		vacancies.append(vacancy)
	data['vacancies'] = vacancies


@bp.route(_name, methods=['POST'])
@api
@caps()
def create_purchase():
	data = MyForm(
		Field('activityId', is_mandatory=True, validators=[helper.check_uuid_is_valid]),
		Field('babyId', is_mandatory=True, validators=[helper.check_uuid_is_valid]),
		Field('timeslotIds', is_mandatory=True,
			validators=[
				(check_timeslot_ids,),
			]),
	).get_data()

	activityId = data['activityId']
	activity = m.Activity.query.get(activityId)
	if not activity:
		raise InvalidUsage(_('activity {} not found').format(activityId))
	if not activity.isActive:
		raise InvalidUsage(_('activity {} is not active').format(activityId))

	babyId = data['babyId']
	baby = m.Baby.query.get(babyId)
	if not baby:
		raise InvalidUsage(_('baby {} not found').format(babyId))

	time_scope = db.session \
		.query(func.min(m.Timeslot.start), func.max(m.Timeslot.end)) \
		.filter(m.Timeslot.timeslotId.in_(data['timeslotIds'])) \
		.one()
	purchase = m.Purchase(
		activityId=activityId,
		providerId=activity.providerId,
		babyId=babyId,
		bookedBy=g.current_user.userId,
		startDate=time_scope[0].strftime("%Y-%m-%d"),
		endDate=time_scope[1].strftime("%Y-%m-%d"),
	)
	vacancies = data['vacancies']
	for v in vacancies:
		purchase.vacancies.append(v)
	SS.add(purchase)
	SS.flush()
	return jsonify(
			purchase=m.Purchase.dump(purchase),
		)
