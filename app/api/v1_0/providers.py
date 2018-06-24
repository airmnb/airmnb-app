
from flask import request, session, jsonify

import db.model as m
from db.db import SS
from app.api import api, caps, MyForm, Field, validators
from app.i18n import get_text as _
from . import api_1_0 as bp, InvalidUsage

from . import _helper as helper

_name = '/' + __file__.split('/')[-1].split('.')[0]


@bp.route(_name, methods=['POST'])
@api
@caps()
def create_new_provider():
	data = MyForm(
		Field('providerId', is_mandatory=True, default=lambda: g.current_user.userId),
		Field('info', is_mandatory=True, validators=[
			validators.is_string,
			]),
		Field('certificates')
		)
	provider = m.Provider(**data)
	SS.add(provider)
	SS.flush()
	return jsonify(message=_('created provider {0} successfully'
		).format(provider.providerId),
		provider=m.Provider.dump(provider),
	)


@bp.route(_name + '/<providerId>', methods=['GET'])
@api
@caps()
def get_provider(providerId):
	provider = m.Provider.query.get(providerId)
	if not provider:
		raise InvalidUsage(_('provider {} not found').format(providerId), 404)
	return jsonify(provider=m.Provider.dump(provider))


@bp.route(_name + '/<providerId>', methods=['PUT'])
@api
@caps()
def update_provider(providerId):
	provider = m.Provider.query.get(providerId)
	data = MyForm(
		Field('info', is_mandatory=True, validators=[
			validators.is_string,
			]),
		Field('certificates')
		)
	if not provider:
		user = m.User.query.get(providerId)
		if not user:
			raise InvalidUsage(_('provider {} not found').format(providerId), 404)
		else:
			provider = m.Provider(providerId=providerId, **data)
			SS.add(provider)
	else:
		for k, v in data:
			setattr(provider, k, v)
	SS.flush()
	return jsonify(
		message=_('updated provider {} successfully').format(providerId),
		provider=m.Provider.dump(provider),
		)

