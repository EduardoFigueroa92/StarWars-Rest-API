from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)    
    
    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }
    
class Favoritos(db.Model):
    __tablename__ = 'favoritos'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
    user = db.relationship("User", backref='favoritos', lazy=True)

    planeta_id = db.Column(db.Integer, db.ForeignKey("planetas.id"))
    planeta = db.relationship("Planetas", backref='favoritos', lazy=True)

    personaje_id = db.Column(db.Integer, db.ForeignKey("personajes.id"))
    personaje = db.relationship("Personajes", backref='favoritos', lazy=True)

    nave_id = db.Column(db.Integer, db.ForeignKey("naves.id"))
    nave = db.relationship("Naves", backref='favoritos', lazy=True)

    def __repr__(self):
        return '<Favoritos %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planeta": self.planeta.serialize() if self.planeta else None,
            "personaje": self.personaje.serialize() if self.personaje else None,
            "nave": self.nave.serialize() if self.nave else None
        }    

class Planetas(db.Model):
    __tablename__ = 'planetas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    diameter = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    population = db.Column(db.String(200))
    climate = db.Column(db.String(200))
    terrain = db.Column(db.String(200))

    def __repr__(self):
        return '<Planetas %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain
        }

class Personajes(db.Model):
    __tablename__ = 'personajes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    hair_color = db.Column(db.String(200))    
    skin_color = db.Column(db.String(200))
    eye_color = db.Column(db.String(200))
    birth_year = db.Column(db.String(200))
    gender = db.Column(db.String(200))

    def __repr__(self):
        return '<Personajes %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender
        }
    
class Naves(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    model = db.Column(db.String(200))
    manufacturer = db.Column(db.String(200))
    cost_in_credits = db.Column(db.String(200))
    length = db.Column(db.Float)
    crew = db.Column(db.Integer)
    passengers = db.Column(db.Integer)
    

    def __repr__(self):
        return '<Naves %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers
        }