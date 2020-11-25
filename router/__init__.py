from flask import Flask, render_template, request
from .schemas import SchemaCodeExec
from .routing_table import RUN_LANG_TABLE
from marshmallow import ValidationError
import requests

app = Flask(__name__)


def do_code_exec(run_lang_ip, lang, code):
    addr = "http://%s/api/run/%s" % (run_lang_ip, lang)
    response = requests.post(addr, json={"code": code})
    return response.json(), response.status_code


@app.route('/')
def playground():
    return render_template("playground.html")


@app.route('/api/rce', methods=['POST'])
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
