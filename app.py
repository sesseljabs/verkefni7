from flask import Flask, render_template, session, url_for, request, redirect, escape, flash
from flask import *
from datetime import datetime
import pymysql.cursors
import os

app = Flask(__name__)

app.secret_key = os.urandom(16)
#app.config['SECRET KEY'] = "leyndo"

connection = pymysql.connect(host="tsuts.tskoli.is", user="1609022560", password="mypassword", db="1609022560_verk7", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
with connection.cursor() as cursor:
    cursor.execute("select * from users where user_name='uwu'")
    result = cursor.fetchall()
    connection.commit()
    #connection.close()
        

@app.route("/")
def index():
    # user_id = request.cookies.get("uid")
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        values = {
            "username":request.form["username"],
            "password":request.form["password"]
        }
    
    with connection.cursor() as cursor:
        asql = "select count(*) from users where (user_name='%s' and user_password='%s')" % (values['username'], values["password"])
        sql = "select (%s) as boolval" % asql
        print(sql)
        try:
            cursor.execute(sql)
            user = cursor.fetchone()
        except Exception as e:
            print(e)
            return f"login error i guess, {e}"

    login = user["boolval"]
    if login == 0:
        return "passwd eða lykilorð rangt"
    elif login == 1:
        return f"logged in, {values['username']}"
    else:
        return "sql error"


@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/subsignup", methods=["POST"])
def subsignup():
    if request.method == "POST":
        sup = {
            "username":request.form["username"],
            "email":request.form["email"],
            "password":request.form["password"]
        }

    with connection.cursor() as cursor:
        sql = "select * from users"
        cursor.execute(sql)
        userlist = cursor.fetchall()
        for i in userlist:
            pass

    return "lol meme gif"
            

@app.errorhandler(404)
def pagenotfound(error):
    return render_template('pagenotfound.html')


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
    #app.run()