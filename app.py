import regex
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
import re
from models import *


@app.route("/")
def hello():
    return {
               "message": "hello world"
           }, 200


'''@app.route("/division/<numero1>/<numero2>",methods=["GET"])
def division(numero1,numero2):
    valor = int(numero1)/int(numero2)
    print("valor es:",valor)
    return ""+str(int(valor))'''


@app.route("/user",methods=["POST"])
def crearUsuario():
    data = request.json
    print("DATOS:",data)
    if not data:
        return {
                   "mensaje": "No hay datos"
               }, 400
    user = Usuario().create(**data)
    if user:
        return {
            "mensaje": "Usuario creado",
            "datos": user
        }
    else:
        return {
                   "message": "Error creando al usuario"
               }, 500

@app.route("/user/<nombre>",methods=["GET"])
def obtenerUsuario(nombre):
    try:
        if nombre is None:
            return {
               "mensaje": "Falta el nombre del usuario"
           }, 400

        user = Usuario().get_by_name(nombre)
        if not user:
            return {
                       "mensaje": "Usuario no existente"
                   }, 400
        print("USER ",user)
        datos = {}
        datos['nombre'] = user['nombre']
        datos['calorias']=user['calorias']
        datos['metabolismobasal'] = user['metabolismobasal']
        return datos
        #datos['MetabolismoBasal']=user['MetabolismoBasal']

    except:
        return {
                   "message": "Error al obtener el usuario"
               }, 500


def limpiarJSON(text):
    #text = 'Entendido, José. Aquí te dejo una opción de desayuno de aproximadamente 658 calorías que puedes consumir para ayudarte a bajar de peso:```json{  "desayuno": [    {      "alimento": "Huevos revueltos con espinacas",      "porcion": "2 huevos",      "calorias": 200    },    {      "alimento": "Pan integral tostado con aguacate",      "porcion": "2 rebanadas de pan",      "calorias": 458    }  ]}```Este desayuno incluye huevos revueltos con espinacas, que son ricos en proteínas y fibra, y pan integral tostado con aguacate, que proporciona gras'

    pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}')
    result=pattern.findall(text)
    data = json.loads(result[0])
    '''if "desayuno" in data:
        return data['desayuno']
    if "comida" in data:
        return data['comida']
    if "cena" in data:
        return data['cena']'''
    return data

@app.route("/comida/<tipo>",methods=["POST"])
def crearComida(tipo):
    tipoaux=0
    if not tipo:
        return {
                   "mensaje": "Falta el tipo"
               }, 400
    data = request.data
    if not data:
        return {
                   "mensaje": "No hay datos"
               }, 400
    data = data.decode('UTF-8')
    data = limpiarJSON(data)
    if "desayuno" in tipo.lower():
        tipoaux =Comida.TIPO_DESAYUNO
        data["comida"] = data.pop("desayuno")
    elif "comida" in tipo.lower():
        tipoaux = Comida.TIPO_COMIDA
        data["comida"] = data.pop("comida")
    else:
        tipoaux=Comida.TIPO_CENA
        data["comida"] = data.pop("cena")




    data['tipo']=tipoaux
    data['timestamp']=time.time()
    comida = Comida().create(data)
    if comida:
        respuesta = {}
        respuesta['respuesta'] = Comida().getAlexaNL(comida)
        return respuesta,200
    else:
        return {
                   "message": "Error creando la comida"
               }, 500

'''@app.route("/comida/<nickname>/<starttime>/<endtime>",methods=["GET"])
def obtenerComidas(nickname,starttime,endtime):
    try:
        if nickname is None or starttime is None or endtime is None:
            return {
                       "message": "Datos incompletos"
                   }, 400
        comidas = Comida().get_comida_by_time(nickname,starttime,endtime)
        print("Comidas "+str(comidas))
        if comidas:
            return {

                "datos": comidas
            }
        else:
            return {
                       "message": "No hay comidas de " + str(nickname)+" en la fecha indicada"
                   }, 400
    except Exception as e:
        print("ERROR "+str(e))
        return {
                   "message": "Error al obtener las comidas de "+str(nickname)
               }, 500

@app.route("/calorias/<nickname>/<starttime>/<endtime>",methods=["GET"])
def obtenerCalorias(nickname,starttime,endtime):
    try:
        if nickname is None or starttime is None or endtime is None:
            return {
                       "message": "Datos incompletos"
                   }, 400
        calorias = Comida().get_calories_by_time(nickname,starttime,endtime)

        if calorias:
            return calorias
        else:
            return {
                       "message": "Error al obtener las calorias de " + str(nickname)
                   }, 500
    except Exception as e:
        print("ERROR "+str(e))
        return {
                   "message": "Error al obtener las calorias de "+str(nickname)
               }, 500'''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5002, debug=False)
    import ssl

    #context = ssl.SSLContext()
    #context.load_cert_chain("/home/master/dev/plannutricional/diarionutricional/conversational_ugr_es.pem", "/home/master/dev/plannutricional/diarionutricional/conversational_ugr_es.key")
    #CORS(app)
    #app.run(host='0.0.0.0', port=5002, ssl_context=context, debug=False)
