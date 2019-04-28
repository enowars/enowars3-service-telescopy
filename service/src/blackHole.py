import string
import random
from app import db


class blackhole(db.Model):
    id = db.Column('dateaseId', db.Integer, primary_key = True)
    bhId = db.Column(db.String(32))
    name = db.Column(db.String(100))
    description = db.Column(db.String(50))  
    age = db.Column(db.String(200))
    location = db.Column(db.String(10))   

    def __init__(self, name, description, age):
        self.name = name
        self.bhId = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
        self.description = description
        self.age = age

    def to_dict(self):
        return{
            "bhId" : self.bhId,
            "name" : self.name,
            "desctiption" : self.description,
            "age" : self.description,
            "location" : self.location
        }

# class blackhole:
#     def __init__(self,name,age):
#         self.id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32));
#         self.name = name
#         self.age = age
#         self.location = "???"
#         self.angle = "???"


#     def setLocation(self, location):
#         self.location = location

#     def setAbgle(self, angle):
#         self.angle = angle