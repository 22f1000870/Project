import os
from flask import Flask,render_template, url_for,redirect,flash,session,request
from sqlalchemy import or_
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
                        i=Influencer(influencer_id=u.user_id,fname=a['fname'],lname=a['lname'],image=f.filename,reach=r,niche=a['niche'])
                        db.session.add(i)
                        db.session.commit()
                        return redirect(url_for('home'))
                    else:
                        i=Influencer(influencer_id=u.user_id,fname=a['fname'],lname=a['lname'],reach=r,niche=a['niche'])
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
            return redirect(url_for('dashboard'))
        else:
            flash("Wrong user credentials")
            return redirect(url_for('home'))


@app.route('/dashboard',methods=['GET'])
def dashboard():
    if current_user.type=='influencer':
        
        j=db.session.query(Influencer).filter(Influencer.influencer_id==current_user.user_id).first()
        c=db.session.query(Campaign,Time).filter(Campaign.influencer_id==current_user.user_id,Time.status==1).all()
        print(c)
        r=db.session.query(Request).filter(Request.influencer_id==current_user.user_id).all()
        print(r)
        pending=[]
        for i in r:
            z={'request_id':i.request_id,'campaign':i.campaign}
            print(z['campaign'].image)
            pending.append(z)
        print(pending)
        return render_template('idashboard.html',influencer=j,campaign=c,request=pending)
    elif current_user.type=='sponsor':
        return redirect(url_for('campaign'))


    


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
        campaign=[{},{}]
        return render_template('addcampaign.html',user=current_user.sponsor,campaign=campaign,url=url_for('addcampaign'))
    elif request.method=='POST':
        a=request.form
        if a['title'] and a['requirement'] and a['start'] and a['end'] and a['niche'] :
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
                    c=Campaign(sponsor_id=current_user.user_id,title=a['title'],niche=a['niche'],requirement=a['requirement'],amount=a['amount'])
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
        r=db.session.query(Request).filter(Request.campaign_id==c.campaign_id).first()
        return render_template('details.html',campaign=c,user=current_user.sponsor,time=t,amount=r.amount,u=current_user)#
    

@app.route('/campaign/<int:id>',methods=['GET','POST'])
@login_required
def updatecampaign(id):
    if request.method=='GET':
        c=db.session.query(Campaign,Time).filter(Campaign.campaign_id==id,Time.campaign_id==id).first()
        r=db.session.query(Request).filter(Request.campaign_id==c[0].campaign_id).first()
        return render_template('addcampaign.html',user=current_user.sponsor,campaign=c,url=url_for('updatecampaign',id=c[0].campaign_id),amount=r.amount)
    else:
        c=db.session.query(Campaign,Time,Request).filter(Campaign.campaign_id==id,Time.campaign_id==id,Request.campaign_id==id).first()
        a=request.form
        i=request.files['image']
        img=c[0].image
        c[0].title=a['title']; c[0].niche=a['niche']; c[0].requirement=a['requirement'];c[2].amount=float(a['amount'])
        file=os.path.join(app.config['UPLOAD_FOLDER'], i.filename)
        i.save(file)
        c[0].image=i.filename
        c[1].start=datetime.strptime(a['start'],"%Y-%m-%dT%H:%M")
        c[1].end=datetime.strptime(a['end'],"%Y-%m-%dT%H:%M")
        c[1].visibility=int(a['visibility'])
        db.session.commit()#
        filepath=os.path.join(app.config['UPLOAD_FOLDER'],img)
        os.remove(filepath)
        return redirect(url_for('details',id=c[0].campaign_id))
        

        
@app.route('/search/<usertype>/<int:id>',methods=['GET','POST'])
@login_required
def search(usertype,id):
    if usertype=='sponsor':
        

        if request.method=='POST':
            a=request.form
            search_query=a['search']
            if search_query !="":
                results = db.session.query(Influencer).filter(or_(
                    Influencer.fname.like(f"%{search_query}%"),Influencer.lname.like(f"%{search_query}%"))).all()
                return render_template('find.html', results=results, user=current_user.sponsor,cid=id)
            else:
                results = db.session.query(Influencer).filter(Influencer.niche==a['niche']).all()
                return render_template('find.html',results=results,user=current_user.sponsor,cid=id)

        
        else:
            results=Influencer.query.all()
            print(results)
            return render_template('find.html',results=results, user=current_user.sponsor,cid=id)


@app.route('/request/<status>/<int:request_id>')
def requeststatus(status,request_id):
    if status=='accept':
        cd=db.session.query(Request).filter(Request.request_id==request_id).first()
        print(cd.campaign)


@app.route('/request/<int:cid>/<int:id>')
def crequest(cid,id):
    r=db.session.query(Request).filter(Request.campaign_id==cid,Request.influencer_id.is_(None)).first()
    if r:
        r.influencer_id=id
        db.session.commit()
        print(r.influencer_id)
        flash('Request send successfully')
        return redirect(url_for('details',id=cid))
    else:
        flash('You have already request influencer please wait till they accept or reject!')
        return redirect(url_for('details',id=cid))

if __name__=='__main__':
    db.create_all()
    app.run(host='0.0.0.0',port=5000,debug=True)










