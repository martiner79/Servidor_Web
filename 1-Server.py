
from flask import Flask,request,jsonify

# Hacemos mención a nuestro archivo.
app = Flask(__name__)

claves = ("name","type")
alumnos = []

#Utilizamos esto para que el ouput sea ordenado.
app.config['JSON_SORT_KEYS'] = False    

#Ejemplo de cómo deberían quedar los datos ingresados.
"""
alumnos = [
    {"id":1,"nombre":"Pedro","Carrera":"Ingenieria"},
    {"id":2,"nombre":"Marcela","Carrera":"Abogacia"},
    {"id":3,"nombre":"Lucas","Carrera":"Programacion"}
]
"""

#Creamos las rutas de nuestra página.

@app.route("/")
def index_home():
    return "<h1><strong>¡Bienvenidos Estudiantes!</strong></h1><h4>Diríjase a 127.0.0.1:5000/alumnos Para visualizar y modificar los alumnos</h4>"

#Página de ejemplo.
@app.route("/Premium")
def nuevo():
    return "<h2><strong>Página en Construcción.. Vuelva Pronto! :)</strong></h2>"

#Especificamos los métodos a utilizaar en /alumnos. De no hacerlo, toma por defecto a GET.

#GET

@app.route("/alumnos", methods = ["GET"])
def get_alumno():
    if request.method == "GET":
        return jsonify({"alumnos":alumnos}),200

#Especificamos los alumnos a buscar por id
@app.route("/alumnos/<int:dato_id>", methods = ["GET"])
def get_id(dato_id):
    try:
        if request.method == "GET":
            return jsonify(alumnos[dato_id]),200
    except IndexError:
        return jsonify({"Error":"No se encuentra el dato ingresado"}),400
        
#POST

@app.route("/alumnos", methods = ["POST"])
def post_alumno():
    if request.method == "POST":
        carga = request.get_json()
    for i in claves:
        if i not in carga:
            return jsonify({"Error":"Los datos ingresados son incorrectos"}),400
        else:
            info = {"id": len(alumnos), "Nombre": carga["name"], "Especialidad":carga["type"]}
            alumnos.append(info)
            return jsonify("Los datos se han cargado satisfactoriamente!"),201 

#PUT

@app.route("/alumnos/<int:dato_id>", methods = ["PUT"])
def put_alumno(dato_id):
   if request.method == "PUT":
        carga = request.get_json()
        try:
            if "name" in carga and "type" not in carga:
                if carga["name"] is not None:
                    alumnos[dato_id]["Nombre"] = carga["name"]
                    return jsonify("El Nombre se ha cambiado con éxito."),201 
            elif "type" in carga and "name" not in carga:
                if carga["type"] is not None:
                    alumnos[dato_id]["Especialidad"] = carga["type"]
                    return jsonify("La Especialidad se ha cambiado con éxito."),201
            elif "name" in carga and "type" in carga:
                if carga["name"] is not None:
                    alumnos[dato_id]["Nombre"] = carga["name"]
                if carga["type"] is not None:
                    alumnos[dato_id]["Especialidad"] = carga["type"]
                return jsonify("¡Los datos han sido modificados con éxito!"),201
            else:
                return jsonify({"Error":"Datos incorrectos!"}),400
        except IndexError:
            return jsonify({"Error":"El id ingresado es incorrecto"}),404

#DELETE

@app.route("/alumnos/<int:dato_id>", methods=["DELETE"])   
def delete_alumno(dato_id):
    if request.method == "DELETE":
        try:
            del alumnos[dato_id]
            contador = len(alumnos)
            for i in range(contador):   #Actualizamos el contador
                alumnos[i]["id"] = i
            return jsonify("El alumno indicado se ha eliminado."),200
        except IndexError:
            return jsonify({"Error":"El id ingresado es incorrecto!"}),202



if __name__ == "__main__":
    app.run(debug=True)