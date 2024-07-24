import os
from flask import Flask,render_template, url_for,redirect,flash,session,request
from sqlalchemy import and_, or_
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
        c=db.session.query(Campaign).filter(Campaign.influencer_id==current_user.user_id,Campaign.influencer_id==j.influencer_id).all()
        print(c)
        r=db.session.query(Request).filter(Request.influencer_id==current_user.user_id).all()
        print(r)
        pending=[]
        for i in r:
            t=i.campaign
            z={'request_id':i.request_id,'campaign':t,'time':t.time,'amount':t.amount}
            print(z['campaign'].image)
            pending.append(z)
        print(pending)
        return render_template('idashboard.html',influencer=j,campaign=c,request=pending)
    elif current_user.type=='sponsor':

        t=db.session.query(Campaign).filter(Campaign.sponsor_id==current_user.user_id,Campaign.influencer_id.isnot(None)).all()
        r=db.session.query(Irequest).filter(Irequest.sponsor_id==current_user.user_id).all()
        
        pending=[]
        
        for i in r:
            c=i.campaign
            z={'request_id':i.request_id,'campaign':c,'time':c.time,'amount':c.amount,'influencer':i.influencer}
            pending.append(z)
        return render_template('sdashboard.html',user=current_user.sponsor,campaign=t,request=pending)


    


@app.route('/campaign')
@login_required
def campaign():
   if request.method=='GET':
    c=db.session.query(Campaign).filter(Campaign.sponsor_id==current_user.user_id).all()
    campaign=[]
    for i in c:
        r={'campaign':i,'request':i.time}
        print(i.time)
        campaign.append(r)
    return render_template('campaign.html',user=current_user.sponsor,campaign=campaign)#user=current_user.sponsor,campaign=c)

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
                t=Time(campaign_id=c.campaign_id,start=start,end=end,status=0)
                r=Request(campaign_id=c.campaign_id)
                db.session.add_all([t,r])
                db.session.commit()
                
                return redirect(url_for('campaign'))
            else:
                flash("Incorrect Date Time")
        
                return redirect(url_for('addcampaign'))
        else:
            flash("empty field, please fill up!")
            return redirect(url_for('addcampaign'))
            

@app.route('/campaign/<int:id>',methods=['GET','POST'])
@login_required
def updatecampaign(id):
    if request.method=='GET':
        c=db.session.query(Campaign,Time).filter(Campaign.campaign_id==id,Time.campaign_id==id).first()
        r=db.session.query(Request).filter(Request.campaign_id==c[0].campaign_id).first()
        return render_template('addcampaign.html',user=current_user.sponsor,campaign=c,url=url_for('updatecampaign',id=c[0].campaign_id),amount=c[0].amount)
    else:
        c=db.session.query(Campaign,Time,Request).filter(Campaign.campaign_id==id,Time.campaign_id==id,Request.campaign_id==id).first()
        a=request.form
        i=request.files['image']
        img=c[0].image
        c[0].title=a['title']; c[0].niche=a['niche']; c[0].requirement=a['requirement'];c[0].amount=float(a['amount'])
        file=os.path.join(app.config['UPLOAD_FOLDER'], i.filename)
        i.save(file)
        c[0].image=i.filename
        c[1].start=datetime.strptime(a['start'],"%Y-%m-%dT%H:%M")
        c[1].end=datetime.strptime(a['end'],"%Y-%m-%dT%H:%M")
        
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
            
            return render_template('find.html',results=results, user=current_user.sponsor,cid=id)
        
@app.route('/search/influencer',methods=['GET',"POST"])
def searchinfluencer():
    if request.method=="POST":
            a=request.form
            search_query=a['search']
            if search_query!="":
                results=db.session.query(Campaign).filter(or_(Campaign.title.like(f"%{search_query}%"),Campaign.requirement.like(f"%{search_query}%"))).all()
                z=[]
                if results:
                    for i in results:
                        r=i.request
                        for j in r:
                            if not j.influencer_id:
                                result={'campaign':i,'time':i.time}
                                z.append(result)
                    return render_template('sfind.html',results=z,user=current_user.influencer)
                else:
                    return render_template('sfind.html',results=z,user=current_user.influencer)
            else:
                results = db.session.query(Campaign).filter(Campaign.niche==a['niche']).all()
                z=[]
                print(results)#
                if results:
                    for i in results:
                        r=i.request
                        print(r)
                        for j in r:
                            if not j.influencer_id:
                                result={'campaign':i,'time':i.time}
                                z.append(result)
                    return render_template('sfind.html',results=z,user=current_user.influencer)
                else:
                    return render_template('sfind.html',results=z,user=current_user.influencer)
    else:
        results=Campaign.query.all()
        z=[]
        if results:
            print(results)
            for i in results:
                result={'campaign':i,'time':i.time}
                z.append(result)
            return render_template('sfind.html',results=z,user=current_user.influencer)
        else:
            return render_template('sfind.html',results=z,user=current_user.influencer)


@app.route('/request/<status>/<int:request_id>',methods=['GET','POST'])
@login_required
def requeststatus(status,request_id):
    if current_user.type=='influencer':
        if request.method=='POST' and status=='accept':
            cd=db.session.query(Request).filter(Request.request_id==request_id).first()
            cd.campaign.influencer_id=current_user.user_id
            c=db.session.query(Campaign).filter(Campaign.campaign_id==cd.campaign_id).first()
            c.time.status=1
            d = db.session.query(Request).filter_by(campaign_id=cd.campaign_id).all()
            ir=db.session.query(Irequest).filter_by(campaign_id=c.campaign_id).all()
            for j in ir:
                db.session.delete(j)
            for req in d:
                db.session.delete(req)
            
            # Commit the changes
            db.session.commit()
            return redirect(url_for('dashboard'))
    
        else:
            cd=db.session.query(Request).filter(Request.request_id==request_id).first()
            cd.campaign.influencer_id=None
            cd.influencer_id=None
            db.session.commit()
            return redirect(url_for('dashboard'))
    elif current_user.type=='sponsor':
        if request.method=='POST' and status=='accept':
            cd=db.session.query(Irequest).filter(Irequest.request_id==request_id).first()
            cd.campaign.influencer_id=current_user.user_id
            c=db.session.query(Campaign).filter(Campaign.campaign_id==cd.campaign_id).first()
            c.time.status=1
            d = db.session.query(Irequest).filter_by(campaign_id=cd.campaign_id).all()
            r=db.session.query(Request).filter_by(campaign_id=c.campaign_id).all()
            for j in r:
                db.session.delete(j)
            for req in d:
                db.session.delete(req)
            db.session.commit()
            return redirect(url_for('dashboard'))
        else:
            cd=db.session.query(Irequest).filter(Irequest.request_id==request_id).first()
            cd.campaign.influencer_id=None
            db.session.delete(cd)
            db.session.commit()
            return redirect(url_for('dashboard'))





@app.route('/request/<int:cid>/<int:id>')
@login_required
def crequest(cid,id):
    if current_user.type=='sponsor':
        r=db.session.query(Request).filter(Request.campaign_id==cid,Request.influencer_id.is_(None)).first()
        if r:
            r.influencer_id=id
            db.session.commit()
            print(r.influencer_id)
            flash('Request send successfully')
            return redirect(url_for('campaign'))
        else:
            flash('You have already requested a influencer please wait till they accept or reject!')
            return redirect(url_for('campaign'))
    else:
        ir=db.session.query(Irequest).filter(Irequest.campaign_id==cid,Irequest.influencer_id==id).first()
       
        if ir:
           
            flash('You have already requested this Campaign please wait till Sponsor accept or reject it !')
            return redirect(url_for('searchinfluencer'))
        else:
            c=db.session.query(Campaign).filter(Campaign.campaign_id==cid).first()
            r=Irequest(campaign_id=cid,influencer_id=id,sponsor_id=c.sponsor_id)
            db.session.add(r)
            db.session.commit()
            flash('Request Send successfully !')
            return redirect(url_for('searchinfluencer'))
    


@app.route("/end/<int:id>",methods=['GET'])
def endcampaign(id):
    if current_user.type=='influencer':
        c=db.session.query(Campaign).filter(Campaign.campaign_id==id).first()
        c.influencer_id=None
        c.time.status=0
        r=Request(campaign_id=id)
        db.session.add(r)
        db.session.commit()
        return redirect(url_for('dashboard'))
    elif current_user.type=='sponsor':
        c=db.session.query(Campaign).filter(Campaign.campaign_id==id).first()
        c.influencer_id=None
        c.time.status=0
        r=Request(campaign_id=id)
        db.session.add(r)
        db.session.commit()
        return redirect(url_for('dashboard'))


@app.route("/delete/<int:id>",methods=['GET','POST'])
def deletecampaign(id):
    c=db.session.query(Campaign).filter(Campaign.campaign_id==id).first()
    db.session.delete(c)
    db.session.commit()
    return redirect('/campaign')


if __name__=='__main__':
    db.create_all()
    app.run(host='0.0.0.0',port=5000,debug=True)










