import sql
from flask import session


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


def get_current_user():
    return session["username"]


def get_password(username):
    query = """SELECT password FROM accounts WHERE user_name=%s;"""
    parameters = (username,)
    fetch = 'cell'
    return sql.query(query, parameters, fetch)


def create_new_account(username, password_hash, time):
    query = """INSERT INTO accounts (user_name, password, reg_date) VALUES (%s, %s, %s) """
    parameter = (username, password_hash, time)

    sql.query(query, parameter, "")


def get_usernames():
    query = """SELECT user_name FROM accounts"""
    parameter = ""
    fetch = "col"
    return sql.query(query, parameter, fetch)
