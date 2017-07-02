from flask import Flask, render_template, redirect, request, jsonify, session
import os
import sql
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import json

app = Flask(__name__)


@app.route("/planet/vote", methods=['POST'])
def vote_up():
    planet = request.form["planet"]
    planet_id = request.form["planetId"]
    user = get_current_user()
    time = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())
    add_vote = request.form["addVote"]

    if int(add_vote):
        try:
            parameters = (planet_id, planet, get_user_id(user), time)
            save_vote(parameters)
        except:
            pass
    else:
        parameters = (planet_id, planet, get_user_id(user))
        delete_vote(parameters)

    return ""


def delete_vote(parameters):
    query = """DELETE FROM planet_votes WHERE planet_id=%s AND planet_name=%s AND account_id=%s;"""
    fetch = ""
    sql.query(query, parameters, fetch)


def get_user_id(user):
    query = """ SELECT id FROM accounts WHERE user_name=%s"""
    parameters = (user,)
    fetch = 'one'
    return sql.query(query, parameters, fetch)


def save_vote(parameters):
    query = """ INSERT INTO planet_votes (planet_id, planet_name, account_id,sub_time) VALUES (%s, %s, %s, %s)"""
    fetch = ""
    sql.query(query, parameters, fetch)


def votes(user_id):
    query = """ SELECT planet_name FROM planet_votes WHERE account_id=%s """
    parameters = (user_id)
    fetch = "col"
    return sql.query(query, parameters, fetch)


@app.route("/get_current_user_votes")
def get_votes():
    if session:
        user = get_current_user()
        user_id = get_user_id(user)
        try:
            votes_of_user = votes(user_id)
        except:
            return json.dumps("")
        return json.dumps(votes_of_user)
    return ""


def get_current_user():
    return session["username"]


@app.route("/login")
def try_log_in():
    return render_template("login.html")


@app.route("/login", methods=['POST'])
def login():
    usernames = get_usernames()
    username = request.form["username"]
    password = request.form["password"]

    if username in usernames:
        check = check_password_hash(get_password(username), password + "4" + username)
        if check:
            session["username"] = username
            return redirect("/")

    return render_template("login.html", invalid_username_or_password=True)


def get_password(username):
    query = """SELECT password FROM accounts WHERE user_name=%s;"""
    parameters = (username,)
    fetch = 'cell'
    return sql.query(query, parameters, fetch)


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        usernames = get_usernames()
        username = request.form["username"]
        password = request.form["password"]
        password_hash = generate_password_hash(password + "4" + username, method='pbkdf2:sha512:80000', salt_length=8)
        time = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())

        if username in usernames:
            return render_template("register.html", not_available=True)
        else:
            create_new_account(username, password_hash, time)
            return render_template("login.html", created_account=True)
    return render_template("register.html")


@app.route("/")
def first_page():
    if "username" in session:
        username = session["username"]
        return render_template("main.html", username=username)
    else:
        return render_template("main.html")


def create_new_account(username, password_hash, time):
    query = """INSERT INTO accounts (user_name, password, reg_date) VALUES (%s, %s, %s) """
    parameter = (username, password_hash, time)

    sql.query(query, parameter, "")


def get_usernames():
    query = """SELECT user_name FROM accounts"""
    parameter = ""
    fetch = "col"
    return sql.query(query, parameter, fetch)


@app.route('/vote_statistic', methods=['POST'])
def vote_statistic():
    query = """SELECT planet_name, COUNT(account_id)
                FROM planet_votes
                GROUP BY planet_name
                ORDER BY COUNT(account_id) DESC """
    parameters = ("")
    fetch = "all"
    try:
        result = sql.query(query, parameters, fetch)
    except:
        result = ""
    return json.dumps(result)


def main():
    app.secret_key = os.urandom(12)
    app.run(debug=True)


if __name__ == '__main__':
    main()
