
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

_name = '/' + __file__.split('/')[-1].split('.')[0]


@bp.route(_name + '/<reviewId>', methods=['POST'])
@api
@caps()
def create_review_response(reviewId):
	review = m.ActivityReview.query.get(reviewId)
	if not review:
		raise InvalidUsage(_('review {} not found').format(reviewId))
	data = MyForm(
		Field('reviewId', is_mandatory=True, default=reviewId),
		Field('activityId', is_mandatory=True, default=review.activityId),
		Field('providerId', is_mandatory=True, default=review.providerId),
		Field('content', is_mandatory=True, validators=[
			validators.is_string,
			validators.non_blank,
			]),
		)
	resp = m.ActivityResponse(**data)
	SS.add(resp)
	SS.flush()
	return jsonify(
		message=_('successfully created response {}').format(resp.responseId),
		response=m.ActivityResponse.dump(),
	)
