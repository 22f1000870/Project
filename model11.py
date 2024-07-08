from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Roles(db.Model):
    __tablename__='roles'
    user_id=db.Column(db.Integer,primary_key=True,autoincrement=True,unique=True)
    username=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    type=db.Column(db.String,nullable=False)
    
    sponsor=db.relationship('Sponsor',uselist=False,backref=db.backref('role',uselist=False),cascade='all,delete-orphan')
    influencer=db.relationship('Influencer',uselist=False,backref=db.backref('role',uselist=False),cascade='all,delete-orphan')


class Sponsor(db.Model):
    __tablename__='sponsor'
    sponsor_id=db.Column(db.Integer,db.ForeignKey('roles.user_id'),primary_key=True)
    company_name=db.Column(db.String,nullable=False,unique=True)
    industry=db.Column(db.String,nullable=False)
    image=db.Column(db.LargeBinary)
    budget=db.Column(db.Double,nullable=False)
    
    campaign=db.relationship('Campaign',backref=db.backref('sponsor'))
    

class Campaign(db.Model):
    __tablename__='campaign'
    sponsor_id=db.Column(db.Integer,db.ForeignKey('sponsor.sponsor_id'))
    campaign_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    niche=db.Column(db.String,nullable=False)
    requirement=db.Column(db.String)
    visibility=db.Column(db.Integer,nullable=False)
    amount=db.Column(db.Double,nullable=False)
    time=db.relationship('Time',uselist=False,backref=db.backref('campaign',uselist=False))
    
    
class Influencer(db.Model):
    __tablename__='influencer'
    influencer_id=db.Column(db.Integer,db.ForeignKey('roles.user_id'),primary_key=True)
    fname=db.Column(db.String,nullable=False)
    lname=db.Column(db.String)
    image=db.Column(db.LargeBinary)
    reach=db.Column(db.Integer)
    


class Time(db.Model):
    campaign_id=db.Column(db.Integer,db.ForeignKey('campaign.campaign_id'),primary_key=True)
    start=db.Column(db.DateTime,nullable=False)
    end=db.Column(db.DateTime,nullable=False)
    status=db.Column(db.Integer,nullable=False)
    
class CI(db.Model):
    campaign_id=db.Column(db.Integer,db.ForeignKey('campaign.campaign_id'),primary_key=True)
    influencer_id=db.Column(db.Integer,db.ForeignKey('influencer.influencer_id'))
    
