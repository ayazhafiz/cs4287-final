from flask import redirect, render_template, request, Blueprint, url_for
from flask_login import UserMixin, login_user

# Is this sacrilege? Yes. Maybe later on we will make something "proper", but
# that's not the point of this exercise.
SECRET_KEY = "GCOQ73GBBOLW0WC1U6K8T7KN"
USERS = {
    "ayazhafiz": "ayazayaz",
    "kevjin": "kevinkevin",
}


class User(UserMixin):
    def __init__(self, id):
        self.id = id

    @staticmethod
    def get(username, password):
        if USERS.get(username) == password:
            return User(username)
        return None


auth = Blueprint("auth", __name__)


@auth.route('/login', methods=['GET'])
def login_view():
    return render_template("login.html")


@auth.route('/login', methods=['POST'])
def login_auth():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.get(username, password)
    if user is None:
        return render_template("login.html", tried_invalid=True)

    login_user(user)
    return redirect(url_for('rce.playground'))
