import os

import mimetypes
from base64 import b64decode
import re

from flask import request, session, jsonify, g
import psycopg2

import db.model as m
from db.db import SS
from app.api import api, caps, MyForm, Field, validators
from app.i18n import get_text as _
from . import api_1_0 as bp, InvalidUsage

from . import _helper as helper

_name = '/' + __file__.split(os.sep)[-1].split('.')[0]

@bp.route(_name + '/<imageId>', methods=['GET','POST'])
@api
@caps()
def create_new_image(imageId):
	if not imageId:
		raise InvalidUsage(_('imageId not found'))

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
	image = m.Image(imageId=imageId, blob=blob, mimeType=mimeType)
	SS.add(image)
	SS.flush()
	return jsonify(image=m.Image.dump(image))

def normalize_b64_str(data, key, literal):
	m = re.match('data:[^/]*/[^/]*;base64,', literal)
	if m:
		literal = literal[m.end():]
	decoded = b64decode(bytearray(literal, 'utf-8'))
	return decoded

@bp.route(_name + '_base64', methods=['POST'])
@api
@caps()
def create_new_image_as_base64():
	data = MyForm(
		Field('data', is_mandatory=True,
			normalizer=normalize_b64_str,
		)
	).get_data()
	image = m.Image(blob=data['data'], mimeType=None)
	SS.add(image)
	SS.flush()
	return jsonify(image=m.Image.dump(image))

