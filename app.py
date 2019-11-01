from flask import Flask, render_template, session, url_for, request, redirect, escape
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
        sql = "select * from users where user_name='%s'" % values['username']
        cursor.execute(sql)
        user = cursor.fetchone()
        print(user)
        connection.close()

    if user == None:
        return "user is none"
    else:
        if values["password"] == user["user_password"]:
            return "worked lol ur now logged in, %s" % user["user_name"]
        else:
            return "wrong pass lol"
            

@app.errorhandler(404)
def pagenotfound(error):
    return render_template('pagenotfound.html')


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
    #app.run()