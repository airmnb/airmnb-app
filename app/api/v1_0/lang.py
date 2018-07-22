import os

from flask import request, session, jsonify, json

import db.model as m
from db.db import SS
from app.api import api, caps, MyForm, Field, validators
from app.i18n import get_text as _
from . import api_1_0 as bp, InvalidUsage

from . import _helper as helper

_name = '/' + __file__.split(os.sep)[-1].split('.')[0]


def load_json_i18n_file(lang):
	site_root = os.path.realpath(os.path.dirname(__file__))
	json_url = os.path.join(site_root, 'i18n', lang + '.json')
	data = json.load(open(json_url, encoding='utf-8'))
	return data

supported_langs = {
	'en': load_json_i18n_file('en'), 
	'zh': load_json_i18n_file('zh'), 
}

@bp.route(_name, methods=['GET'])
@bp.route(_name + '/<lang>', methods=['GET'])
@api
@caps()
def get_lang_i18n(lang):
	if lang is None:
		lang = "en"
	if lang not in supported_langs:
		raise InvalidUsage(_('Language code {0} is not supported').format(lang), 404)
	data = supported_langs[lang]
	print('>>>>> ', lang, supported_langs)
	return jsonify(i18n=data)
