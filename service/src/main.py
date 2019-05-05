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

db.create_all()


@app.route('/addPlanet')
def addPlanet():
    # print(request.headers.get('date'))

    # bh = blackhole(request.args.get('name'),
    # request.args.get('description'),
    # request.args.get('age'),
    # request.args.get('angle'))
    # db.session.add(bh)
    # db.session.commit()

    planet1 = Planet(request.args.get('name'),
    request.args.get('declination'),
    request.args.get('rightAscension'),
    request.args.get('flag')
    )
    db.session.add(planet1)
    db.session.commit()
    return "black hole added"
	
@app.route('/index.html')
def getIndex():
	return render_template("index.html")
 
def checkTicketValidity(ticket):
    pass 


@app.route('/getPlanet')
def getPlanet():
    dec = request.args.get('declination')
    ra = request.args.get('rightAscension')
    # print(planet.query.filter(blackhole.name == planetName).first())
    # print(blackhole.query.filter(blackhole.angle == bh).first().to_dict())

    s = planet.call("ticketCheck " + request.args.get('ticket'), shell=True) 
    if(s == 1):
        return jsonify(Planet.query.filter(Planet.declination == dec).first().to_dict())
    else:
        return "ticket not valid :("



def calculateLocation(bh, angle):
    data = base64.b64encode(str.encode(bh.bhId))
    k = f.Fernet(data)
    bh.location = k.encrypt(str.encode(angle))

if __name__ == '__main__':
    #ToDo main doesn't get called by flask app; tables don't get created
    db.create_all()
    app.run(host='0.0.0.0',port=8000, debug=True)

    



    