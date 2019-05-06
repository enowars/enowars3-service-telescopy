from planet import Planet    
from app import db
from app import app
import cryptography.fernet as f
import subprocess as planet
import base64
from planet import Planet    
from flask import request
import json
from flask import jsonify 
from flask import render_template
import hashlib


db.create_all()


def representsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

@app.route('/index.html')
def getIndex():
	return render_template("index.html")
 
def checkTicketValidity(ticket):
    pass 


@app.route('/getAll')
def getAll():
    planets = Planet.query.all()
    result = {}
    for p in planets:
        result.update({p.id : p.name})
    return jsonify(result)

@app.route('/getPlanet')
def getPlanet():
    
    dec = request.args.get('declination')
    ra = request.args.get('rightAscension')
    idd = request.args.get('id')
    t = request.args.get('ticket')
 
    if(t is None or not representsInt(t) or (idd is None and (dec is None or ra is None))):
        return "can't do that!"

    s = planet.call("ticketCheck " + t, True)
    if(s != 1):
        "can't do that!"

    if(idd is not None):
        ra = Planet.query.filter(Planet.planetId == idd).first()
        if(ra is not None):
            return jsonify(Planet.query.filter(Planet.planetId == idd).first().to_dict())
        else:
            return "nothing found!"

    re = Planet.query.filter(Planet.declination == dec).filter(Planet.rightAscension == ra).first()
    if( re is not None):
        return jsonify(ra.to_dict())
    else:
        return "nothing found"

def iding(i):
    e = i.name.encode('utf-8')
    h = hashlib.md5(e)
    i.planetId = h.hexdigest()

@app.route('/addPlanet')
def addPlanet():
    planet1 = Planet(request.args.get('name'),
    request.args.get('declination'),
    request.args.get('rightAscension'),
    request.args.get('flag')
    )
    iding(planet1)
    db.session.add(planet1)
    db.session.commit()
    return "black hole added"


def calculateLocation(bh, angle):
    data = base64.b64encode(str.encode(bh.bhId))
    k = f.Fernet(data)
    bh.location = k.encrypt(str.encode(angle))

if __name__ == '__main__':
    #ToDo main doesn't get called by flask app; tables don't get created
    db.create_all()
    app.run(host='0.0.0.0',port=80, debug=True)

    



    