import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planetas, Personajes, Vehiculos, FavoritosPlaneta, FavoritosPersonaje, FavoritosVehiculo
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


@app.route('/vehiculos', methods=['GET'])
def cargar_vehiculos():

    vehiculos = Vehiculos.query.all()
    all_vehiculos = list(map(lambda x: x.serialize(), vehiculos))

    return jsonify(all_vehiculos), 200


@app.route('/users/favoritos', methods=['GET'])
def cargar_favoritos():

    planetasFavoritos= FavoritosPlaneta.query.all()
    all_planetasFavoritos = list(map(lambda x: x.serialize(),planetasFavoritos))
    personajesFavoritos= FavoritosPersonaje.query.all()
    all_personajesFavoritos = list(map(lambda x: x.serialize(),personajesFavoritos))
    vehiculosFavoritos= FavoritosVehiculo.query.all()
    all_vehiculosFavoritos = list(map(lambda x: x.serialize(),vehiculosFavoritos))
#planetas favoritos y todos los planetas favoritos

    return jsonify({"planetas":all_planetasFavoritos, "personajes":all_personajesFavoritos, "vehiculos":all_vehiculosFavoritos }), 200# añadir vehiculos 


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


@app.route('/vehiculos/<int:vehiculo_id>', methods=['GET'])
def cargar_vehiculo(vehiculo_id):

    vehiculo = Vehiculos.query.get(vehiculo_id)

    if vehiculo is None:
        raise APIException("Nave no encontrada", status_code=404)
    
    vehiculo_data = {
        "id": vehiculo.id,
        "name": vehiculo.name,
        "model": vehiculo.model,
        "manufacturer": vehiculo.manufacturer,
        "cost_in_credits": vehiculo.cost_in_credits,
        "length": vehiculo.length,
        "crew": vehiculo.crew,
        "passengers": vehiculo.passengers
    }

    return jsonify(vehiculo_data), 200


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
    favorito_existente = FavoritosPlaneta.query.filter_by(user_id=user_id, planeta_id=planeta_id).first()

    if favorito_existente:
        
        return jsonify({"error": "El planeta ya está en favoritos"}), 400

    nuevo_favorito = FavoritosPlaneta(user_id = user_id, planeta_id = planeta_id)
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
    favorito_existente = FavoritosPersonaje.query.filter_by(user_id=user_id, personajes_id=personaje_id).first()

    if favorito_existente:

        return jsonify({"error": "El personaje ya está en favoritos"}), 400

    nuevo_favorito = FavoritosPersonaje(user_id = user_id, personajes_id = personaje_id)
    db.session.add(nuevo_favorito)
    db.session.commit()
    response_body = {
        "msg": f"Personaje '{personaje.name}' añadido a favoritos"
    }

    return jsonify(response_body), 200


@app.route('/vehiculos', methods=['POST'])
def crear_vehiculo():    

    body = request.get_json()
    vehiculo = Vehiculos(name=body['name'], model=body['model'], manufacturer=body['manufacturer'], cost_in_credits=body['cost_in_credits'], length=body['length'], crew=body['crew'], passengers=body['passengers'] )
    db.session.add(vehiculo)
    db.session.commit()
    response_body = {
        "msg": "Vehiculo creado"
    }

    return jsonify(response_body), 200


#comparar con favoritos personaje y ajustar (igual)
@app.route('/favorito/vehiculo/<int:vehiculo_id>/<int:user_id>', methods=['POST'])
def añadir_favorito_vehiculo(vehiculo_id, user_id):
    # Obtener el usuario actual (simulado, asegúrate de obtener el usuario real)

    # Validar la existencia del vehiculo en la base de datos
    vehiculo = Vehiculos.query.get(vehiculo_id)

    if not vehiculo:

        return jsonify({"error": "Vehiculo no encontrado"}), 404

    # Crear una nueva entrada en la tabla Favoritos
    favorito_existente = FavoritosVehiculo.query.filter_by(user_id=user_id, vehiculos_id=vehiculo_id).first()

    if favorito_existente:

        return jsonify({"error": "El vehiculo ya está en favoritos"}), 400

    nuevo_favorito = FavoritosVehiculo(user_id = user_id, vehiculos_id = vehiculo_id)
    db.session.add(nuevo_favorito)
    db.session.commit()

    response_body = {
        "msg": f"Vehiculo '{vehiculo.name}' añadido a favoritos"
    }

    return jsonify(response_body), 200









#despues hacer los deletes






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
    

@app.route('/vehiculos/<int:vehiculo_id>', methods=['PUT'])
def editar_vehiculo(vehiculo_id):

    body = request.get_json()
    vehiculo = Vehiculos.query.get(vehiculo_id)

    if vehiculo is None:
        raise APIException("vehiculo no encontrado", status_code=404)
    
    if body is not None:
        if "name" in body:
            vehiculo.name = body["name"]
        if "model" in body:
            vehiculo.model = body["model"]
        if "manufacturer" in body:
            vehiculo.manufacturer = body["manufacturer"]
        if "cost_in_credits" in body:
            vehiculo.cost_in_credits = body["cost_in_credits"]
        if "length" in body:
            vehiculo.length = body["length"]
        if "crew" in body:
            vehiculo.crew = body["crew"]
        if "passengers" in body:
            vehiculo.passengers = body["passengers"]


        # Commit para guardar los cambios en la base de datos
        db.session.commit()

        response_body = {
            "msg": "Vehiculo editado exitosamente",
            "id": vehiculo.id,
            "name": vehiculo.name,
            "model": vehiculo.model,
            "manufacturer": vehiculo.manufacturer,
            "cost_in_credits": vehiculo.cost_in_credits,
            "length": vehiculo.length,
            "crew": vehiculo.crew,
            "passengers": vehiculo.passengers
        }

        return jsonify(response_body), 200
    else:
        raise APIException("No se proporcionaron datos para editar el vehiculo", status_code=400)
    

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


@app.route('/vehiculos/<int:vehiculo_id>', methods=['DELETE'])
def eliminar_vehiculo(vehiculo_id):

    body = request.get_json()
    vehiculo = Vehiculos.query.get(vehiculo_id)

    if vehiculo is None:
        raise APIException("Vehiculo no encontrado", status_code=404)
    
    db.session.delete(vehiculo)
    db.session.commit()

    return jsonify("Vehiculo eliminado"), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)