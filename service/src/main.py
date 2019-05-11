from app import db, app
from routes import routes

db.create_all()
app.register_blueprint(routes)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
