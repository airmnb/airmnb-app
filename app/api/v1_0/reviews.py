import os

from flask import request, session, jsonify, g

import datetime
from dateutil.tz import tzoffset
import db.model as m
from db import database as db
from db.db import SS
from app.api import api, caps, MyForm, Field, validators
from app.i18n import get_text as _
from . import api_1_0 as bp, InvalidUsage

from . import _helper as helper

_name = '/' + __file__.split(os.sep)[-1].split('.')[0]


@bp.route(_name + '/activity/<activityId>', methods=['GET'])
def get_activity_reviews(activityId):
	activity = m.Activity.query.get(activityId)
	if not activity:
		raise InvalidUsage(_('activity {} not found').format(activityId))
	reviews = m.ActivityReview.query.filter(
		m.ActivityReview.activityId==activityId).order_by(
		m.ActivityReview.reviewId).all()
	return jsonify(
		reviews=m.ActivityReview.dump(reviews))


@bp.route(_name, methods=['POST'])
@api
@caps()
def create_review():
	data = MyForm(
		Field('activityId', is_mandatory=True, default=None),
		Field('reviewerId', is_mandatory=True, default=lambda: g.current_user.userId),
		Field('stars', is_mandatory=True, validators=[
			(validators.is_number, (), dict(min_value=0, max_value=5)),
			]),
		Field('content'),
		).get_data()

	activityId = data['activityId']
	activity = m.Activity.query.get(activityId)
	if not activity:
		raise InvalidUsage(_('activity {} not found').format(activityId))
	#
	# TODO: check if user (userId) is a consumer of activity (activityId)
	#
	review = m.ActivityReview(**data)
	SS.add(review)
	SS.flush()
	return jsonify(message=_('successfully created review {}').format(review.reviewId),
		review=m.ActivityReview.dump(review),
		)


@bp.route(_name + '/<reviewId>/responses/', methods=['POST'])
@api
@caps()
def create_review_response(reviewId):
	review = m.ActivityReview.query.get(reviewId)
	if not review:
		raise InvalidUsage(_('review {} not found').format(reviewId))
	activity = m.Activity.query.get(review.activityId)
	data = MyForm(
		Field('reviewId', is_mandatory=True, default=reviewId),
		Field('activityId', is_mandatory=True, default=review.activityId),
		Field('providerId', is_mandatory=True, default=activity.providerId),
		Field('content', is_mandatory=True, validators=[
			validators.is_string,
			validators.non_blank,
			]),
		).get_data()
	resp = m.ActivityResponse(**data)
	SS.add(resp)
	SS.flush()
	return jsonify(
		message=_('successfully created response {}').format(resp.responseId),
		response=m.ActivityResponse.dump(resp),
	)

