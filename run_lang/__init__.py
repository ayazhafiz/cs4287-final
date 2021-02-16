from flask import Flask, request, jsonify, Blueprint
from .execute import execute
from .describe import get_ubuntu, get_description, \
    get_packages, get_server_lang


bp = Blueprint("rce", __name__)


@bp.route('/api/run', methods=['POST'])
def playground():
    json_data = request.get_json()
    if not json_data:
        return {"message": "Data must be JSON"}, 400
    try:
        code = json_data["code"]
    except KeyError:
        return {"message": "Key \"code\" is not present"}, 400

    result = execute(code)
    return jsonify(result), 200


@bp.route('/api/describe', methods=['GET'])
def describe():
    return jsonify({
        "ubuntu": get_ubuntu(),
        "description": get_description(),
        "packages": get_packages(),
    })


def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)

    return app
