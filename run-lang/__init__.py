from flask import Flask, request, jsonify
from .execute import execute, LanguageNotFound

app = Flask(__name__)


@app.route('/api/run/<lang>', methods=['POST'])
def playground(lang=None):
    json_data = request.get_json()
    if not json_data:
        return {"message": "Data must be JSON"}, 400
    try:
        code = json_data.get("code")
    except KeyError:
        return {"message": "Key \"code\" is not present"}, 400

    try:
        result = execute(lang, code)
    except LanguageNotFound:
        return {"message": "Language \"%s\" is not valid" % lang}, 400

    return jsonify(result), 200
