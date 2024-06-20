from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class roles(db.Model):
    __tablename__='roles'
    user_id=db.Column(db.Integer,autoincrement=True,unique=True)
    username=db.Column(db.String,primary_key=True)
    password=db.Column(db.String,nullable=False)
    sponsor=db.relationship('Sponsor',uselist=False)
    influencer=db.relationship('Influencer',uselist=False)

class Sponsor(db.Model):
    __tablename__='sponsor'
    sponsor_id=db.Column(db.Integer,db.ForiegnKey('roles.user_id'))
    company_name=db.Column(db.String,nullable=False,unique=True)
    category=db.Column(db.String,nullable=False)
    industry=db.Column(db.String,nullable=False)
    image=db.Column(db.LargeBinary,nullable=False)
    budget=db.Column(db.Double,nullable=False)
    #campaigns=db.relationship('Campaign',backref=db.backref('sponsors',lazy='joined'),lazy='dynamic')

class Campaign(db.Model):
    __tablename__='campaign'
    campaign_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    niche=db.Column(db.String,nullable=False)
    requirement=db.Column(db.String)
    visibility=db.Column(db.Integer,nullable=False)
    amount=db.Column(db.Double,nullable=False)
    time=db.relationship('Time',uselist=False)
    
class Influencer(db.Model):
    __tablename__='influencer'
    influencer_id=db.Column(db.Integer,db.ForeignKey('roles.user_id'))
    fname=db.Column(db.String,nullable=False)
    lname=db.Column(db.String)
    image=db.Column(db.LargeBinary,nullable=False)
    niche=db.Column(db.String,nullable=False)
    reach=db.Column(db.Integer,nullable=False)

class Time(db.Model):
    campaign_id=db.Column(db.Integer,db.ForeignKey('campaign.campaign_id'))
    start=db.Column(db.DateTime,nullable=False)
    end=db.Column(db.DateTime,nullable=False)
    status=db.Column(db.Integer,nullable=False)
    
class CI(db.Model):
    campaign_id=db.Column(db.Integer,db.ForeignKey('campaign.campaign_id'))
    influencer_id=db.Column(db.Integer,db.ForeignKey('influencer.influencer_id'))

    campaign=db.relationship('Camipaign',backref='CI',lazy='dynamic')
    


'''class Request:
    __tablename__='request'
    request_id=db.Column(db.String,primary_key=True)
    campaign_id=db.Column(db.Integer,db.ForeignKey('campaign.campaign_id'))
    status=db.Column(db.Integer,db.ForeignKey('campaign.status'))
    niche=db.Column(db.Integer,db.ForeignKey('campaign.niche'))'''