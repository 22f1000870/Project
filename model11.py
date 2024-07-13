from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,current_user,login_user,logout_user,login_required


db=SQLAlchemy()
login=LoginManager()



class Roles(db.Model,UserMixin):
    __tablename__='roles'
    user_id=db.Column(db.Integer,primary_key=True,autoincrement=True,unique=True)
    username=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    type=db.Column(db.String,nullable=False)
    
    sponsor=db.relationship('Sponsor',uselist=False,backref=db.backref('role',uselist=False),cascade='all,delete-orphan')
    influencer=db.relationship('Influencer',uselist=False,backref=db.backref('role',uselist=False),cascade='all,delete-orphan')

    def get_id(self):
        return self.user_id
class Sponsor(db.Model,UserMixin):
    __tablename__='sponsor'
    sponsor_id=db.Column(db.Integer,db.ForeignKey('roles.user_id'),primary_key=True)
    company_name=db.Column(db.String,nullable=False,unique=True)
    industry=db.Column(db.String,nullable=False)
    image=db.Column(db.String)
    budget=db.Column(db.Double,nullable=False)
    
    campaign=db.relationship('Campaign',backref=db.backref('sponsor'))
    

class Campaign(db.Model,UserMixin):
    __tablename__='campaign'
    sponsor_id=db.Column(db.Integer,db.ForeignKey('sponsor.sponsor_id'))
    campaign_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String,nullable=False)
    image=db.Column(db.String)
    niche=db.Column(db.String,nullable=False)
    requirement=db.Column(db.String)
    amount=db.Column(db.Double,nullable=False)
    influencer_id=(db.Column(db.Integer,db.ForeignKey('influencer.influencer_id')))
    time=db.relationship('Time',uselist=False,backref=db.backref('campaign',uselist=False))
    request=db.relationship('Request',backref=db.backref('campaign'))
    
    
class Influencer(db.Model,UserMixin):
    __tablename__='influencer'
    influencer_id=db.Column(db.Integer,db.ForeignKey('roles.user_id'),primary_key=True)
    fname=db.Column(db.String,nullable=False)
    lname=db.Column(db.String)
    image=db.Column(db.String)
    reach=db.Column(db.Integer)
    niche=db.Column(db.String,nullable=False)

class Time(db.Model,UserMixin):
    __tablename__='time'
    campaign_id=db.Column(db.Integer,db.ForeignKey('campaign.campaign_id'),primary_key=True)
    start=db.Column(db.DateTime,nullable=False)
    end=db.Column(db.DateTime,nullable=False)
    status=db.Column(db.Integer,nullable=False)
    visibility=db.Column(db.Integer,nullable=False)
    
class Request(db.Model,UserMixin):
    __tablename__='request'
    request_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    campaign_id=db.Column(db.Integer,db.ForeignKey('campaign.campaign_id'))
    influencer_id=db.Column(db.Integer,db.ForeignKey('influencer.influencer_id'))
    amount=db.Column(db.Double,nullable=False)
