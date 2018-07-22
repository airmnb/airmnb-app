import os

from flask import request, session, jsonify

import db.model as m
from db.db import SS
from app.api import api, caps, MyForm, Field, validators
from app.i18n import get_text as _
from . import api_1_0 as bp, InvalidUsage

from . import _helper as helper

_name = '/' + __file__.split(os.sep)[-1].split('.')[0]


@bp.route(_name, methods=['GET'])
@api
@caps()
def get_stat():
	userCount = m.User.query.count()
	babyCount = m.Baby.query.count()
	providerCount = m.Provider.query.count()
	activityCount = m.Activity.query.count()
	bookingCount = m.Purchase.query.count()
	transactionCount = m.Purchase.query.filter(m.Purchase.status == 1).count()
	
	return jsonify(stat=dict(
		userCount=userCount, 
		babyCount=babyCount,
		providerCount=providerCount,
		activityCount=activityCount,
		bookingCount=bookingCount,
		transactionCount=transactionCount,
	))
