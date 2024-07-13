import os
from flask import Flask,render_template, url_for,redirect,flash,session,request
from model11 import*
from datetime import datetime

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///project_database.sqlite3"

app.config['SECRET_KEY']='mirzajunaid'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER']=os.path.join(basedir,'static')

db.init_app(app)

login.init_app(app)

app.app_context().push()

db.create_all()

def checkext(filename):
    if '.' in filename and filename.rsplit('.',1)[1].lower():
        return True
    else:
        return False
    

@login.user_loader
def loader(user_id):
    return db.session.get(Roles,int(user_id))

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
                    f=request.files['image']

                    if f and checkext(f.filename):
                        filepath=os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
                        f.save(filepath)
                        i=Influencer(influencer_id=u.user_id,fname=a['fname'],lname=a['lname'],image=f.filename,reach=r)
                        db.session.add(i)
                        db.session.commit()
                        return redirect(url_for('home'))
                    else:
                        i=Influencer(influencer_id=u.user_id,fname=a['fname'],lname=a['lname'],reach=r)
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
                    f=request.files['image']
                    if f and checkext(f.filename):
                        filepath=os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
                        f.save(filepath)
                        #relative_filepath = os.path.join('static', f.filename)
                        print(filepath)
                        #print(relative_filepath)
                        s=Sponsor(sponsor_id=u.user_id,company_name=a['cname'],industry=a['industry'],image=f.filename,budget=float(a['budget']))
                        db.session.add(s)
                        db.session.commit()
                        return redirect(url_for('home'))
                    else:
                        s=Sponsor(sponsor_id=u.user_id,company_name=a['cname'],industry=a['industry'],budget=float(a['budget']))
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
def log():
    if request.method=='POST':
       
        u=db.session.query(Roles).filter(Roles.username==request.form.get('username'),Roles.password==request.form.get('pswd')).first()
        if u:
            login_user(u)
            return redirect(url_for('campaign'))
        else:
            flash("Wrong user credentials")
            return redirect(url_for('home'))



@app.route('/campaign')
@login_required
def campaign():
   if request.method=='GET':
    c=db.session.query(Campaign).filter(Campaign.sponsor_id==current_user.user_id).all()
    return render_template('campaign.html',user=current_user.sponsor,campaign=c)#user=current_user.sponsor,campaign=c)

@app.route('/campaign/add',methods=['GET','POST'])
@login_required
def addcampaign():
    if request.method=='GET':
        return render_template('addcampaign.html',user=current_user.sponsor)
    elif request.method=='POST':
        a=request.form
        if a['title'] and a['requirement'] and a['start'] and a['end'] and a['niche'] and a['amount'] :
            start= datetime.strptime(a['start'],"%Y-%m-%dT%H:%M")
            end= datetime.strptime(a['end'],"%Y-%m-%dT%H:%M")
            f=request.files['image']
            if end>start:
                if f and checkext(f.filename):
                    filepath=os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
                    f.save(filepath)
                    #relative_filepath = os.path.join('static', f.filename)
                    print(filepath)
                    #print(relative_filepath)
                    c=Campaign(sponsor_id=current_user.user_id,title=a['title'],niche=a['niche'],requirement=a['requirement'],image=f.filename,amount=a['amount'])
                    
                else:
                    c=Campaign(sponsor_id=current_user.user_id,title=a['title'],niche=a['niche'],requirement=a['requirement'])
                db.session.add(c)
                db.session.flush()   
                t=Time(campaign_id=c.campaign_id,start=start,end=end,status=0,visibility=int(a['visibility']))
                r=Request(campaign_id=c.campaign_id,amount=float(a['amount']))
                db.session.add_all([t,r])
                db.session.commit()
                
                return redirect(url_for('campaign'))
            else:
                flash("Incorrect Date Time")
        
                return redirect(url_for('addcampaign'))
        else:
            flash("empty field, please fill up!")
            return redirect(url_for('addcampaign'))
            
@app.route('/details/<int:id>',methods=['GET','POST'])
@login_required
def details(id):
    if request.method=='GET':
        c=db.session.query(Campaign).filter(Campaign.campaign_id==id).first()
        t=db.session.query(Time).filter(Time.campaign_id==c.campaign_id).first()
        return render_template('details.html',campaign=c,user=current_user.sponsor,time=t)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)










