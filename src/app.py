import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planetas, Personajes, Naves, Favoritos
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def cargar_usuarios():

    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))

    return jsonify(all_users), 200

@app.route('/planetas', methods=['GET'])
def cargar_planetas():

    planetas = Planetas.query.all()
    all_planetas = list(map(lambda x: x.serialize(), planetas))

    return jsonify(all_planetas), 200

@app.route('/personajes', methods=['GET'])
def cargar_personajes():

    personajes = Personajes.query.all()
    all_personajes = list(map(lambda x: x.serialize(), personajes))

    return jsonify(all_personajes), 200

@app.route('/naves', methods=['GET'])
def cargar_naves():

    naves = Naves.query.all()
    all_naves = list(map(lambda x: x.serialize(), naves))

    return jsonify(all_naves), 200

@app.route('/users/favoritos', methods=['GET'])
def cargar_favoritos():

    favoritos = Favoritos.query.all()
    all_favoritos = []

    for favorito in favoritos:
        favorito_data = favorito.serialize()

        favorito_data['usuario'] = favorito.user.name if favorito.user else None

        if favorito.planeta:
            favorito_data['planeta'] = favorito.planeta.serialize()
        if favorito.personaje:
            favorito_data['personaje'] = favorito.personaje.serialize()
        if favorito.nave:
            favorito_data['nave'] = favorito.nave.serialize()

        all_favoritos.append(favorito_data)

    return jsonify(all_favoritos), 200

@app.route('/users/<int:usuario_id>', methods=['GET'])
def cargar_usuario(usuario_id):

    user = User.query.get(usuario_id)

    if user is None:
        raise APIException("Usuario no encontrado", status_code=404)
    
    user_data = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "password": user.password
    }

    return jsonify(user_data), 200

@app.route('/planetas/<int:planeta_id>', methods=['GET'])
def cargar_planeta(planeta_id):

    planeta = Planetas.query.get(planeta_id)

    if planeta is None:
        raise APIException("Planeta no encontrado", status_code=404)
    
    planeta_data = {
        "id": planeta.id,
        "name": planeta.name,
        "diameter": planeta.diameter,
        "rotation_period": planeta.rotation_period,
        "population": planeta.population,
        "climate": planeta.climate,
        "terrain": planeta.terrain
    }

    return jsonify(planeta_data), 200

@app.route('/personajes/<int:personaje_id>', methods=['GET'])
def cargar_personaje(personaje_id):

    personaje = Personajes.query.get(personaje_id)

    if personaje is None:
        raise APIException("Personaje no encontrado", status_code=404)
    
    personaje_data = {
        "id": personaje.id,
        "name": personaje.name,
        "height": personaje.height,
        "mass": personaje.mass,
        "hair_color": personaje.hair_color,
        "skin_color": personaje.skin_color,
        "eye_color": personaje.eye_color,
        "birth_year": personaje.birth_year,
        "gender": personaje.gender
    }

    return jsonify(personaje_data), 200

@app.route('/naves/<int:nave_id>', methods=['GET'])
def cargar_nave(nave_id):

    nave = Naves.query.get(nave_id)

    if nave is None:
        raise APIException("Nave no encontrada", status_code=404)
    
    nave_data = {
        "id": nave.id,
        "name": nave.name,
        "model": nave.model,
        "manufacturer": nave.manufacturer,
        "cost_in_credits": nave.cost_in_credits,
        "length": nave.length,
        "crew": nave.crew,
        "passengers": nave.passengers
    }

    return jsonify(nave_data), 200

@app.route('/users', methods=['POST'])
def crear_usuario():    
    body = request.get_json()
    user= User(name=body['name'], email=body['email'], password=body['password'])
    db.session.add(user)
    db.session.commit()
    response_body = {
        "msg": "Usuario creado "
    }
    return jsonify(response_body), 200

@app.route('/planetas', methods=['POST'])
def crear_planeta():    
    body = request.get_json()
    planeta = Planetas(name=body['name'], diameter=body['diameter'], rotation_period=body['rotation_period'], population=body['population'], climate=body['climate'], terrain=body['terrain'])
    db.session.add(planeta)
    db.session.commit()
    response_body = {
        "msg": "Planeta creado "
    }
    return jsonify(response_body), 200

@app.route('/user/<int:user_id>/favorito/planeta/<int:planeta_id>', methods=['POST'])
def añadir_favorito_planeta(planeta_id, user_id):    
    # Validar la existencia del planeta en la base de datos
    planeta = Planetas.query.get(planeta_id)
    if not planeta:
        return jsonify({"error": "Planeta no encontrado"}), 404

    # Crear una nueva entrada en la tabla Favoritos
    favorito_existente = Favoritos.query.filter_by(user_id=user_id, planeta_id=planeta_id).first()
    if favorito_existente:
        return jsonify({"error": "El planeta ya está en favoritos"}), 400

    nuevo_favorito = Favoritos(user_id = user_id, planeta_id = planeta_id)
    db.session.add(nuevo_favorito)
    db.session.commit()

    response_body = {
        "msg": f"Planeta '{planeta.name}' añadido a favoritos"
    }
    return jsonify(response_body), 200


@app.route('/personajes', methods=['POST'])
def crear_personaje():    
    body = request.get_json()
    personaje = Personajes(name=body['name'], height=body['height'], mass=body['mass'], hair_color=body['hair_color'], skin_color=body['skin_color'], eye_color=body['eye_color'], birth_year=body['birth_year'], gender=body['gender'] )
    db.session.add(personaje)
    db.session.commit()
    response_body = {
        "msg": "Personaje creado "
    }

    return jsonify(response_body), 200
@app.route('/favorito/personaje/<int:personaje_id>/<int:user_id>', methods=['POST'])
def añadir_favorito_personaje(personaje_id, user_id):
    # Obtener el usuario actual (simulado, asegúrate de obtener el usuario real)

    # Validar la existencia del planeta en la base de datos
    personaje = Personajes.query.get(personaje_id)
    if not personaje:
        return jsonify({"error": "Personaje no encontrado"}), 404

    # Crear una nueva entrada en la tabla Favoritos
    favorito_existente = Favoritos.query.filter_by(user_id=user_id, personaje_id=personaje_id).first()
    if favorito_existente:
        return jsonify({"error": "El personaje ya está en favoritos"}), 400

    nuevo_favorito = Favoritos(user_id = user_id, personaje_id = personaje_id)
    db.session.add(nuevo_favorito)
    db.session.commit()

    response_body = {
        "msg": f"Personaje '{personaje.name}' añadido a favoritos"
    }
    return jsonify(response_body), 200

@app.route('/naves', methods=['POST'])
def crear_nave():    
    body = request.get_json()
    nave = Naves(name=body['name'], model=body['model'], manufacturer=body['manufacturer'], cost_in_credits=body['cost_in_credits'], length=body['length'], crew=body['crew'], passengers=body['passengers'] )
    db.session.add(nave)
    db.session.commit()
    response_body = {
        "msg": "Nave creada"
    }

    return jsonify(response_body), 200

@app.route('/favorito/naves/<int:nave_id>/<int:user_id>', methods=['POST'])
def añadir_favorito_nave(nave_id, user_id):
    # Obtener el usuario actual (simulado, asegúrate de obtener el usuario real)

    # Validar la existencia del planeta en la base de datos
    nave = Naves.query.get(nave_id)
    if not nave:
        return jsonify({"error": "Nave no encontrada"}), 404

    # Crear una nueva entrada en la tabla Favoritos
    favorito_existente = Favoritos.query.filter_by(user_id=user_id, nave_id=nave_id).first()
    if favorito_existente:
        return jsonify({"error": "La nave ya está en favoritos"}), 400

    nuevo_favorito = Favoritos(user_id = user_id, nave_id = nave_id)
    db.session.add(nuevo_favorito)
    db.session.commit()

    response_body = {
        "msg": f"Nave '{nave.name}' añadida a favoritos"
    }
    return jsonify(response_body), 200

@app.route('/users/<int:usuario_id>', methods=['PUT'])
def editar_usuario(usuario_id):
    body = request.get_json()

    user = User.query.get(usuario_id)

    if user is None:
        raise APIException("Usuario no encontrado", status_code=404)
    
    if body is not None:
        if "name" in body:
            user.name = body["name"]
        if "email" in body:
            user.email = body["email"]
        
        # Commit para guardar los cambios en la base de datos
        db.session.commit()

        response_body = {
            "msg": "Usuario editado exitosamente",
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
        return jsonify(response_body), 200
    else:
        raise APIException("No se proporcionaron datos para editar el usuario", status_code=400)
    
@app.route('/planetas/<int:planeta_id>', methods=['PUT'])
def editar_planeta(planeta_id):
    body = request.get_json()

    planeta = Planetas.query.get(planeta_id)

    if planeta is None:
        raise APIException("Planeta no encontrado", status_code=404)
    
    if body is not None:
        if "name" in body:
            planeta.name = body["name"]
        if "diameter" in body:
            planeta.diameter = body["diameter"]
        if "rotation_period" in body:
            planeta.rotation_period = body["rotation_period"]
        if "population" in body:
            planeta.population = body["population"]
        if "climate" in body:
            planeta.climate = body["climate"]
        if "terrain" in body:
            planeta.terrain = body["terrain"]
        
        # Commit para guardar los cambios en la base de datos
        db.session.commit()

        response_body = {
            "msg": "Planeta editado exitosamente",
            "id": planeta.id,
            "name": planeta.name,
            "diameter": planeta.diameter,
            "rotation_period": planeta.rotation_period,
            "population": planeta.population,
            "climate": planeta.climate,
            "terrain": planeta.terrain
        }
        return jsonify(response_body), 200
    else:
        raise APIException("No se proporcionaron datos para editar el planeta", status_code=400)
    
@app.route('/personajes/<int:personaje_id>', methods=['PUT'])
def editar_personaje(personaje_id):
    body = request.get_json()

    personaje = Personajes.query.get(personaje_id)

    if personaje is None:
        raise APIException("Personaje no encontrado", status_code=404)
    
    if body is not None:
        if "name" in body:
            personaje.name = body["name"]
        if "height" in body:
            personaje.height = body["height"]
        if "mass" in body:
            personaje.mass = body["mass"]
        if "hair_color" in body:
            personaje.hair_color = body["hair_color"]
        if "skin_color" in body:
            personaje.skin_color = body["skin_color"]
        if "eye_color" in body:
            personaje.eye_color = body["eye_color"]
        if "birth_year" in body:
            personaje.birth_year = body["birth_year"]
        if "gender" in body:
            personaje.gender = body["gender"]

        # Commit para guardar los cambios en la base de datos
        db.session.commit()

        response_body = {
            "msg": "Personaje editado exitosamente",
            "id": personaje.id,
            "name": personaje.name,
            "height": personaje.height,
            "mass": personaje.mass,
            "hair_color": personaje.hair_color,
            "skin_color": personaje.skin_color,
            "eye_color": personaje.eye_color,
            "birth_year": personaje.birth_year,
            "gender": personaje.gender
        }
        return jsonify(response_body), 200
    else:
        raise APIException("No se proporcionaron datos para editar el personaje", status_code=400)
    
@app.route('/naves/<int:nave_id>', methods=['PUT'])
def editar_nave(nave_id):
    body = request.get_json()

    nave = Naves.query.get(nave_id)

    if nave is None:
        raise APIException("Nave no encontrada", status_code=404)
    
    if body is not None:
        if "name" in body:
            nave.name = body["name"]
        if "model" in body:
            nave.model = body["model"]
        if "manufacturer" in body:
            nave.manufacturer = body["manufacturer"]
        if "cost_in_credits" in body:
            nave.cost_in_credits = body["cost_in_credits"]
        if "length" in body:
            nave.length = body["length"]
        if "crew" in body:
            nave.crew = body["crew"]
        if "passengers" in body:
            nave.passengers = body["passengers"]


        # Commit para guardar los cambios en la base de datos
        db.session.commit()

        response_body = {
            "msg": "Nave editada exitosamente",
            "id": nave.id,
            "name": nave.name,
            "model": nave.model,
            "manufacturer": nave.manufacturer,
            "cost_in_credits": nave.cost_in_credits,
            "length": nave.length,
            "crew": nave.crew,
            "passengers": nave.passengers
        }
        return jsonify(response_body), 200
    else:
        raise APIException("No se proporcionaron datos para editar la nave", status_code=400)
    
@app.route('/users/<int:usuario_id>', methods=['DELETE'])
def eliminar_usuario(usuario_id):
    body = request.get_json()

    user = User.query.get(usuario_id)

    if user is None:
        raise APIException("Usuario no encontrado", status_code=404)
    
    db.session.delete(user)
    db.session.commit()

    return jsonify("Usuario eliminado"), 200

@app.route('/planetas/<int:planeta_id>', methods=['DELETE'])
def eliminar_planeta(planeta_id):
    body = request.get_json()

    planeta = Planetas.query.get(planeta_id)

    if planeta is None:
        raise APIException("Planeta no encontrado", status_code=404)
    
    db.session.delete(planeta)
    db.session.commit()

    return jsonify("Planeta eliminado"), 200

@app.route('/personajes/<int:personaje_id>', methods=['DELETE'])
def eliminar_personaje(personaje_id):
    body = request.get_json()

    personaje = Personajes.query.get(personaje_id)

    if personaje is None:
        raise APIException("Personaje no encontrado", status_code=404)
    
    db.session.delete(personaje)
    db.session.commit()

    return jsonify("Personaje eliminado"), 200

@app.route('/naves/<int:nave_id>', methods=['DELETE'])
def eliminar_nave(nave_id):
    body = request.get_json()

    nave = Naves.query.get(nave_id)

    if nave is None:
        raise APIException("Nave no encontrada", status_code=404)
    
    db.session.delete(nave)
    db.session.commit()

    return jsonify("Nave eliminada"), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)