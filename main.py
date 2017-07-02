from flask import Flask, render_template, redirect, request, jsonify, session
import os
import sql
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
import json
import account

app = Flask(__name__)
app.secret_key = os.urandom(12)


@app.route("/planet/vote", methods=['POST'])
def vote_up():
    planet = request.form["planet"]
    planet_id = request.form["planetId"]
    user = account.get_current_user()
    time = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())
    add_vote = request.form["addVote"]

    if int(add_vote):

        parameters = (planet_id, planet, account.get_user_id(user), time)
        account.save_vote(parameters)

    else:
        parameters = (planet_id, planet, account.get_user_id(user))
        account.delete_vote(parameters)

    return ""


@app.route("/get_current_user_votes")
def get_votes():
    if session:
        user = account.get_current_user()
        user_id = account.get_user_id(user)
        try:
            votes_of_user = account.votes(user_id)
        except:
            return json.dumps("")
        return json.dumps(votes_of_user)
    return ""


@app.route("/login")
def try_log_in():
    return render_template("login.html")


@app.route("/login", methods=['POST'])
def login():
    usernames = account.get_usernames()
    username = request.form["username"]
    password = request.form["password"]

    if username in usernames:
        check = check_password_hash(account.get_password(username), password + "4" + username)
        if check:
            session["username"] = username
            return redirect("/")

    return render_template("login.html", invalid_username_or_password=True)


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        usernames = account.get_usernames()
        username = request.form["username"]
        password = request.form["password"]
        password_hash = generate_password_hash(password + "4" + username, method='pbkdf2:sha512:80000', salt_length=8)
        time = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())
        if usernames is None:
            account.create_new_account(username, password_hash, time)
            return render_template("login.html", created_account=True)

        if username in usernames:
            return render_template("register.html", not_available=True)
        else:
            account.create_new_account(username, password_hash, time)
            return render_template("login.html", created_account=True)
    return render_template("register.html")


@app.route("/")
def first_page():
    if "username" in session:
        username = session["username"]
        return render_template("main.html", username=username)
    else:
        return render_template("main.html")


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
