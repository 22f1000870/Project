
from flask import Flask,render_template,request, url_for,redirect
from model11 import*

app=Flask(__name__)

app.config['SQL_ALCHEMY_DATABASE_URI']="sqlite:///project_database.sqlite3"
db.init_app(app)

app.app_context().push()
db.create_all()

@app.route("/",methods=["POST","GET"])
def home():
    if request.method=="GET":
        return render_template("login.html")
    else:
        return redirect(url_for("login"))

@app.route("/registration/<usertype>",methods=["GET","POST"])
def registration(usertype):
    if request.method=="GET":
        if usertype=="influencer":
            return render_template("registration1.html",user=usertype)
        else:
            return render_template("registration1.html",user=usertype)
    else:
        pass
if __name__=="__main__":
    app.run(debug=True)



