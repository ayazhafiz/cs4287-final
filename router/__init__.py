from flask import Flask, render_template, request, Blueprint
from .schemas import SchemaCodeExec
from .routing_table import RUN_LANG_TABLE
from marshmallow import ValidationError
import requests

bp = Blueprint("rce", __name__)


def do_code_exec(run_lang_ip, lang, code):
    addr = "http://%s/api/run/%s" % (run_lang_ip, lang)
    response = requests.post(addr, json={"code": code})
    return response.json(), response.status_code


def do_lang_describe(run_lang_ip, lang):
    addr = "http://%s/api/describe/%s" % (run_lang_ip, lang)
    response = requests.get(addr)
    return response.json(), response.status_code


@bp.route('/')
def playground():
    return render_template("playground.html")


@bp.route('/api/rce', methods=['POST'])
def rce():
    json_data = request.get_json()
    if not json_data:
        return {"message": "Data must be JSON"}, 400
    try:
        data = SchemaCodeExec().load(json_data)
    except ValidationError as err:
        return err.messages, 400

    lang = data["lang"]
    code = data["code"]
    try:
        run_lang_ip = RUN_LANG_TABLE[data["lang"]]
    except KeyError:
        return {"message": "Language \"%s\" is not valid" % lang}, 400

    return do_code_exec(run_lang_ip, lang, code)


@bp.route('/api/describe/<lang>', methods=['GET'])
def describe(lang=None):
    try:
        run_lang_ip = RUN_LANG_TABLE[lang]
    except KeyError:
        return {"message": "Language \"%s\" is not valid" % lang}, 400

    return do_lang_describe(run_lang_ip, lang)


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)

    return app
