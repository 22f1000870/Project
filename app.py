
from flask import Flask,render_template,request, url_for,redirect,flash
from model11 import*
import os
import jinja2

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///project_database.sqlite3"
app.config['SECRET_KEY']='mirzajunaid'
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
            
            if a['fname'] and a['username'] and a['pswd']:
                if a['fname'].isalpha():
                    u=Roles(username=a['username'],password=a['pswd'],type=usertype)
                    db.session.add(u)
                    db.session.flush()
                    r=int(a['instagram'])+int(a['facebook'])+int(a['youtube'])
                    f=(request.files['image']).read()
                    i=Influencer(influencer_id=u.user_id,fname=a['fname'],lname=a['lname'],image=f,reach=r)
                    db.session.add(i)
                    db.session.commit()
                    return redirect(url_for('home'))
                else:
                    flash("First name should not be numeric or alphanumeric",'danger')
                    return redirect(url_for('registration',usertype=usertype))
            else:
                flash("Fill-up the empty fields",'warning')
                return redirect(url_for('registration',usertype=usertype))
            
        else:
            a=request.form
            if a['cname'] and a['username'] and a['pswd'] and a['budget']  and a['industry']:
                if a['cname'].isalpha():
                    u=Roles(username=a['username'],password=a['pswd'],type=usertype)
                    db.session.add(u)
                    db.session.flush()
                    f=(request.files['image']).read()
                    s=Sponsor(sponsor_id=u.user_id,company_name=a['cname'],industry=a['industry'],image=f,budget=float(a['budget']))
                    db.session.add(s)
                    db.session.commit()
                    return redirect(url_for('home'))
                else:
                    flash("Company name should not be numeric or alphanumeric",'danger')
                    return redirect(url_for('registration',usertype=usertype))
            else:
                flash("Fill-up the empty fields",'warning')
                return redirect(url_for('registration',usertype=usertype))

@app.route('/login',methods=['GET','POST'])
def login():
    a=request.form
    u=db.session.query(Roles).filter(Roles.username==a['username'],Roles.password==a['pswd'])
    print(u)
    if u:
        if u.type=='influencer':
            return render_template('idashboard.html')
        elif u.type=='sponsor':
            return render_template('sdashboard.html')
        elif u.type=='admin':
            return render_template('adashboard.html')
        
    else:
        flash('Incorrect Username or Password')
        return redirect(url_for(home))



if __name__=="__main__":
    app.run(debug=True)



