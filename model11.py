from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class roles(db.Model):
    __tablename__='roles'
    user_id=db.Column(db.Integer,autoincrement=True,unique=True)
    username=db.Column(db.String,primary_key=True)
    password=db.Column(db.String,nullable=False)
    type=db.Column(db.String,nullable=False)
    

class Sponsor(db.Model):
    __tablename__='sponsor'
    sponsor_id=db.Column(db.Integer,db.ForiegnKey('roles.user_id'))
    company_name=db.Column(db.String,nullable=False,unique=True)
    industry=db.Column(db.String,nullable=False)
    image=db.Column(db.LargeBinary,nullable=False)
    budget=db.Column(db.Double,nullable=False)
    role=db.relationship('Role',uselist=False,backref=db.backref('sponsor',uselist=False,lazy='dynamic'),lazy='dynamic')
    campaign=db.relationship('Campaign',backref=db.backref('sponsor',lazy='dynamic'),lazy='dynamic')

class Campaign(db.Model):
    __tablename__='campaign'
    campaign_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    niche=db.Column(db.String,nullable=False)
    requirement=db.Column(db.String)
    visibility=db.Column(db.Integer,nullable=False)
    amount=db.Column(db.Double,nullable=False)
    time=db.relationship('Time',uselist=False,backref=db.backref('campaign',uselist=False,lazy='dynamic'),lazy='dynamic')
    
    
class Influencer(db.Model):
    __tablename__='influencer'
    influencer_id=db.Column(db.Integer,db.ForeignKey('roles.user_id'))
    fname=db.Column(db.String,nullable=False)
    lname=db.Column(db.String)
    image=db.Column(db.LargeBinary,nullable=False)
    reach=db.Column(db.Integer,nullable=False)
    role=db.relationship('Role',uselist=False,backref=db.backref('influencer',uselist=False,lazy='dynamic'),lazy='dynamic')



class Time(db.Model):
    campaign_id=db.Column(db.Integer,db.ForeignKey('campaign.campaign_id'))
    start=db.Column(db.DateTime,nullable=False)
    end=db.Column(db.DateTime,nullable=False)
    status=db.Column(db.Integer,nullable=False)
    
class CI(db.Model):
    campaign_id=db.Column(db.Integer,db.ForeignKey('campaign.campaign_id'))
    influencer_id=db.Column(db.Integer,db.ForeignKey('influencer.influencer_id'))
    
