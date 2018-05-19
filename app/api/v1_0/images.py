
import mimetypes

from flask import request, session, jsonify, g
import psycopg2

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
def create_new_image():
	data = MyForm(
		Field('dataFile', is_mandatory=True,
			validators=[
				validators.is_file,
			]),
	).get_data(is_json=False)
	dataFile = data['dataFile']
	blob = dataFile.read()
	filename = dataFile.filename
	mimeType, encoding = mimetypes.guess_type(filename)
	image = m.Image(blob=blob, mimeType=mimeType)
	SS.add(image)
	SS.flush()
	return jsonify(image=m.Image.dump(image))
