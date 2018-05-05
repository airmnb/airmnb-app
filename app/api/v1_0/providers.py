
from flask import request, session, jsonify

import db.model as m
from db.db import SS
from app.api import api, caps, MyForm, Field, validators
from app.i18n import get_text as _
from . import api_1_0 as bp, InvalidUsage

from . import _helper as helper

_name = '/' + __file__.split('/')[-1].split('.')[0]


@bp.route(_name + '/', methods=['POST'])
@api
@caps()
def create_new_provider():
	return jsonify(message=_('created provider {0} successfully'
		).format('newprovider'),
		provider=dict(name='stub'),
	)


@bp.route(_name + '/<providerId>', methods=['GET'])
@api
@caps()
def get_provider(providerId):
	return jsonify(provider=dict(name='tbd', providerId=providerId))


@bp.route(_name + '/<providerId>', methods=['PUT'])
@api
@caps()
def update_provider():
	return jsonify(provider=dict(name='tbd', providerId=providerId))

