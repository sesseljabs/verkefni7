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
        
def logins(values):
    values1 = values
    if "loggedin" in session:
        return f"""
            <h2>Þú ert skráð/ur inn, {session["loggedin"]}</h2>
        """
    else:
        return f"""
            <a href="/login">Skrá inn</a>
            <a href="/signup">Nýskráning</a>
        """

app.jinja_env.filters['logins'] = logins

@app.route("/")
def index():
    # user_id = request.cookies.get("uid")
    return render_template("index.html",session=session)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/submit", methods=["POST"])
def submit():
    if "loggedin" in session:
        return redirect("/")
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
            return render_template("pagenotfound.html")

    login = user["boolval"]
    if login == 0:
        return render_template("custom.html", content="Notendanafn eða lykilorð rangt")
    elif login == 1:
        session["loggedin"] = values['username']
        return redirect("/")
    else:
        return render_template("pagenotfound.html")


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
            if i["user_name"] == sup["username"]:
                return render_template("signup.html", error="Þetta notendanafn er nú þegar í notkun")
            elif i["user_email"] == sup["email"]:
                return render_template("signup.html", error="Þetta netfang er nú þegar í notkun")
        else:
            skrainn = f"insert into users values ('{sup['username']}', '{sup['email']}', '{sup['password']}')"
            cursor.execute(skrainn)
            connection.commit()

    return render_template("custom.html", content=f"Skráður, {sup['username']}!")
            
@app.route("/utskra")
def utskra():
    if "loggedin" in session:
        session.pop("loggedin")
        return render_template("custom.html", content="Skráð/ur út")
    else:
        return redirect("/")

@app.route("/users")
def users():
    if "loggedin" in session:
        if session["loggedin"] in ["admin", "sesseljabs"]:
            with connection.cursor() as cursor:
                getusers = "select user_name,user_email from users"
                cursor.execute(getusers)
                users = cursor.fetchall()

            return render_template("users.html", users=users)
        else:
            return render_template("custom.html", content="Þú hefur ekki leyfi til að skoða þessa síðu")
    else:
        return render_template("custom.html", content="Þú hefur ekki leyfi til að skoða þessa síðu")

@app.errorhandler(404)
def pagenotfound(error):
    return render_template('pagenotfound.html')


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
    #app.run(host="192.168.43.126")