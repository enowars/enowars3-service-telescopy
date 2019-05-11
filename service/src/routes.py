from app import db
import cryptography.fernet as f
import subprocess as planet
import base64
from planet import Planet
from flask import request, jsonify, render_template, Blueprint, session, render_template_string
import hashlib

routes = Blueprint("routes", __name__)


@routes.route('/')
def index():
    planets = Planet.query.all()
    if request.method == 'POST':
        planets = Planet.query.all()
        return render_template('index.html', planets=planets)
    return render_template("index.html", planets=planets)


@routes.route('/getAll')
def get_all():
    planets = Planet.query.all()
    result = {}
    for p in planets:
        result.update({p.id: p.name})
    return jsonify(result)


@routes.route('/getPlanet')
def get_planet():
    dec = request.args.get('declination')
    ra = request.args.get('rightAscension')
    idd = request.args.get('id')
    t = request.args.get('ticket')

    if t is None or not represent_int(t) or (idd is None and (dec is None or ra is None)):
        return "can't do that!"

    s = check_ticket_validity(t)
    if s != 1:
        return "Invalid ticket! Try again :)"

    if idd is not None:
        ra = Planet.query.filter(Planet.planetId == idd).first()
        if ra is not None:
            return jsonify(Planet.query.filter(Planet.planetId == idd).first().to_dict())
        else:
            return "Planet not found!"

    re = Planet.query.filter(Planet.declination == dec).filter(Planet.rightAscension == ra).first()
    if re is not None:
        return jsonify(ra.to_dict())
    else:
        return "Planet not found"


@routes.route('/addPlanet')
def add_planet():
    name = request.args.get('name')
    dec = request.args.get('declination')
    ri = request.args.get('rightAscension')

    if name is None or name == "" or dec is None or dec == "" or ri is None or ri == "":
        return "Please provide all planet information!"

    if Planet.query.filter_by(name=name).first():
        return "A planet with that name already exists!"

    p = Planet(name, dec, ri)
    iding(p)
    db.session.add(p)
    db.session.commit()
    return "Your Planet was created!"


@routes.route('/planet_details')
def get_planet_details():
    name = request.args.get('name')
    planeta = None
    if name:
        planets = Planet.query.all()
        # Session vulnerability here.
        # TODO check if too difficult o too easy.
        session['planets'] = planets
        for p in planets:
            if p.name in name:
                planeta = p.to_dict()
                break
    template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Telescopy</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
          integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
</head>
<body>

<div class="container">
    <div class="card mt-4">
        <div class="card-body">
            <div class="row">
                <div class="col-md-4 mb-3">
                    <label><strong>Name: </strong></label>
                </div>
                <div class="col-md-8 mb-3 ml-0">
                    <label>%s</label>
                </div>
            </div>
            <div class="row">
                <div class="col-md-4 mb-2">
                    <label><strong>Declination: </strong></label>
                </div>
                <div class="col-md-4 mb-3 ml-0">
                    <label>{{ planet.declination }}</label>
                </div>
            </div>
            <div class="row">
                <div class="col-md-4 mb-2">
                    <label><strong>Right Ascension: </strong></label>
                </div>
                <div class="col-md-5 mb-2 ml-0">
                    <label>{{ planet.rightAscension }}</label>
                </div>
            </div>
            <div class="row">
                <div class="col-md-4 mb-2">
                    <label><strong>Location: </strong></label>
                </div>
                <div class="col-md-5 mb-2 ml-0">
                    <label>{{ planet.location }}</label>
                </div>
            </div>
        </div>
    </div>
    <div class="ml-5 pl-5 mt-5">
        <a class="btn btn-secondary" href="/" role="button">Return to Index</a>
    </div>
</div>

<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
        integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
        crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
        integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
        crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
        integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
        crossorigin="anonymous"></script>
</body>
</html>''' % name
    return render_template_string(template, planet=planeta)


def iding(i):
    e = i.name.encode('utf-8')
    d = i.declination.encode('utf-8')
    r = i.rightAscension.encode('utf-8')
    h = hashlib.md5(e+d+r)
    i.planetId = h.hexdigest()


def check_ticket_validity(ticket):
    return planet.call("ticketCheck " + ticket, True)


def calculate_location(bh, angle):
    data = base64.b64encode(str.encode(bh.bhId))
    k = f.Fernet(data)
    bh.location = k.encrypt(str.encode(angle))


def represent_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


