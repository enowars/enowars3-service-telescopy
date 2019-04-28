
from app import app
from app import db
import cryptography.fernet as f
import base64
from blackHole import blackhole 
import random
from flask import request
import json
from flask import jsonify 


flag = "you got the flag!!"
global smbh




# @app.route('/directTelscopeTo/<float:angle>')
# def directTo(angle):
#     if(angle == smbh.angle):
#         return "blackHole Detected"
#     else:
#         return "maybe a star but not a black hole" + str(smbh.angle)
    


# @app.route('/getSmbhDetails')
# def giveInfo():
#     return jsonify({
#         "name" : smbh.name,
#         "id": smbh.id,
#         "location": str(smbh.location)
#     })

@app.route('/addBlackHole')
def addBlackHole():
    bh = blackhole(request.args.get('name'),
    request.args.get('description'),
    request.args.get('age'))
    calculateLocation(bh, request.args.get('angle'))
    db.session.add(bh)
    db.session.commit()
    return "black hole added"

@app.route('/getBlackHole=<bh>')
def getBlackHole(bh):
    return jsonify(blackhole.query.filter(blackhole.age == bh).first().to_dict())



def calculateLocation(bh, angle):
    data = base64.b64encode(str.encode(bh.bhId))
    k = f.Fernet(data)
    bh.location = k.encrypt(str.encode(angle))

if __name__ == '__main__':
    print("hi")
    db.create_all()

    # bh = blackhole("jdfs","flksjdf", "sldkfjd","Sdfsdf")
    # db.session.add(bh)
    # db.session.commit()

    app.run(host='0.0.0.0',port=8000, debug=True)
    



    