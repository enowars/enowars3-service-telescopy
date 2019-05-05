import string
import random
from app import db


class Planet(db.Model):
    id = db.Column('dateaseId', db.Integer, primary_key = True)
    planetId = db.Column(db.String(32))
    name = db.Column(db.String(100))
    declination = db.Column(db.String(50))  
    rightAscension = db.Column(db.String(200))
    location = db.Column(db.String(200))
    flag = db.Column(db.String(200))


    def __init__(self, name, declination, rightAscension, flag):
        self.name = name
        self.planetId = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
        self.declination = declination
        self.rightAscension = rightAscension
        self.flag = flag

    def to_dict(self):
        return{
            "planetId" : self.planetId,
            "name" : self.name,
            "declination" : self.declination,
            "rightAscension" : self.rightAscension,
            "flag" : self.flag
        }
