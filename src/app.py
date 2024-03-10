"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person 

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Esta ruta responde a las solicitudes GET a la raíz del servidor. 
# Devuelve un sitemap generado por la función generate_sitemap(app).
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# Esta ruta responde a las solicitudes GET a /members. 
# Devuelve una lista de todos los miembros de la familia.
@app.route('/members', methods=['GET'])  
# Obtiene todos los miembros de la familia llamando al método get_all_members() de la instancia de jackson_family y los devuelve en formato JSON.
def get_members():

    members = jackson_family.get_all_members()
    return jsonify(members), 200

# Esta ruta responde a las solicitudes GET a /member/<int:id>, donde <int:id> es el ID de un miembro. 
# Devuelve la información del miembro correspondiente al ID especificado.
@app.route('/member/<int:id>', methods=['GET'])
# Obtiene un miembro específico de la familia por su ID llamando al método get_member(id) de la instancia de jackson_family y lo devuelve en formato JSON.
def get_member(id):

    member = jackson_family.get_member(id)
    return jsonify(member), 200

# Esta ruta responde a las solicitudes POST a /member. 
# Permite agregar un nuevo miembro a la lista de miembros de la familia.
@app.route('/member', methods=['POST'])
# Crea un nuevo miembro de la familia a partir de los datos proporcionados en la solicitud POST y lo agrega a la lista de miembros de la familia. 
# Devuelve un mensaje JSON indicando que el nuevo miembro se ha agregado correctamente.
def create_member():
    body = request.get_json()
    new_member = {
        "id": body["id"],
        "first_name": body["first_name"],
        "age": body["age"],
        "lucky_numbers": body["lucky_numbers"]
    }
    jackson_family.add_member(new_member)
    response_body = {
        "msg": "New member successfully added",
        "member":  new_member
    }
    return jsonify(response_body), 200


# Esta ruta responde a las solicitudes DELETE a /member/<int:id>. Permite eliminar un miembro de la lista de miembros de la familia.
@app.route('/member/<int:id>', methods=['DELETE'])

# Elimina un miembro específico de la familia por su ID llamando al método delete_member(id) de la instancia de jackson_family. 
# Devuelve un mensaje JSON indicando que el miembro ha sido eliminado correctamente.
def delete_member(id):
    member = jackson_family.delete_member(id)
    return jsonify({"done" : True, "deleted_member": member}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
