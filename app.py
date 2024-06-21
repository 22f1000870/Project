
from flask import Flask,render_template,request, url_for,redirect
from model11 import*
import os

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///project_database.sqlite3"
db.init_app(app)

app.app_context().push()
db.create_all()

@app.route("/",methods=["GET"])
def home():
    if request.method=="GET":
        return render_template("login.html")

@app.route("/registration/<usertype>",methods=["GET","POST"])
def registration(usertype):
    if request.method=="GET":
        if usertype=="influencer":
            return render_template("registration1.html")
        else:
            return render_template("registration.html")
    else:
        if usertype=='influencer':

            a=request.form
            u=Roles(username=a['username'],password=a['pswd'],type=usertype)
            db.session.add(u)
            db.session.flush()
            r=int(a['instagram'])+int(a['facebook'])+int(a['youtube'])
            f=(request.files['image']).read()
            i=Influencer(influencer_id=u.user_id,fname=a['fname'],lname=a['lname'],image=f,reach=r)
            db.session.add(i)
            db.session.commit()
            return redirect(url_for('home'))
            


if __name__=="__main__":
    app.run(debug=True)



