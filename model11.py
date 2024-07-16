from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,current_user,login_user,logout_user,login_required
from sqlalchemy import event, text
from sqlalchemy.orm import Session

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
    amount=db.Column(db.Double,nullable=True)
    influencer_id=(db.Column(db.Integer,db.ForeignKey('influencer.influencer_id')))
    time=db.relationship('Time',uselist=False,backref=db.backref('campaign',uselist=False),cascade='all,delete-orphan')
    request=db.relationship('Request',backref=db.backref('campaign'),cascade='all,delete-orphan')
    
    
class Influencer(db.Model,UserMixin):
    __tablename__='influencer'
    influencer_id=db.Column(db.Integer,db.ForeignKey('roles.user_id'),primary_key=True)
    fname=db.Column(db.String,nullable=False)
    lname=db.Column(db.String)
    image=db.Column(db.String)
    reach=db.Column(db.Integer)
    niche=db.Column(db.String,nullable=False)
    amount=db.Column(db.String)

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

# @event.listens_for(Influencer.__table__, 'after_create')
# def create_search_index(target, connection, **kw):
#     connection.execute(text('CREATE VIRTUAL TABLE influencer_index USING fts5(influencer_id,fname,niche)'))

# @event.listens_for(Influencer,'after_insert')
# def insert_influencer(mapper,connection,target):
#     connection.execute(
#         text('INSERT INTO influencer_index (influencer_id, fname, niche) VALUES (:influencer_id, :fname, :niche)'),
#         {'influencer_id': target.influencer_id, 'fname': target.fname, 'niche': target.niche}
#     )
    

# @event.listens_for(Influencer,'after_update')
# def update_influencer(mapper,connection,target):
#     connection.execute(
#         text('UPDATE influencer_index SET fname = :fname, niche = :niche WHERE influencer_id = :influencer_id'),
#         {'influencer_id': target.influencer_id, 'fname': target.fname, 'niche': target.niche}
#     )
        

# @event.listens_for(Influencer,'after_delete')
# def delete_influencer(mapper,connection,target):
#     connection.execute(
#         text('DELETE FROM influencer_index WHERE influencer_id = :influencer_id'),
#         {'influencer_id': target.influencer_id}
#     )
        
