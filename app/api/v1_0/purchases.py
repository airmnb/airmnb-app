
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
	activities = [p.activity for p in purchases]
	return jsonify(activities=m.Activity.dump(activities))



@bp.route(_name + '/<purchaseId>', methods=['GET'])
@api
@caps()
def get_purchase(purchaseId):
	purchase = m.Purchase.query.get(purchaseId)
	if not purchase:
		raise InvalidUsage(_('purchase {0} not found').format(purchaseId), 404)
	return jsonify(activity=m.Purchase.dump(purchase))

