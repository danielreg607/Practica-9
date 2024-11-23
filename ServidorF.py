from flask import Flask, request, jsonify
import socket
import threading
import requests

app = Flask(__name__)

# Credenciales para las APIs
OPENWEATHER_API_KEY = 'f1078f547f519dc9a90a97a28a321f23'
GEONAMES_USERNAME = 'bebechaurios'

# Rutas para el Web Service
@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang=es'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return jsonify({
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        })
    else:
        return jsonify({"error": "City not found"}), 404

@app.route('/geonames', methods=['GET'])
def get_geonames():
    place = request.args.get('place')
    if not place:
        return jsonify({"error": "Place parameter is required"}), 400

    url = f'http://api.geonames.org/wikipediaSearchJSON?q={place}&maxRows=1&username={GEONAMES_USERNAME}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'geonames' in data and data['geonames']:
            return jsonify({
                "summary": data['geonames'][0]['summary']
            })
        else:
            return jsonify({"error": "Place not found"}), 404
    else:
        return jsonify({"error": "Failed to connect to Geonames"}), 500

# Funciones para los servidores de sockets
def obtener_clima_socket(ciudad):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={OPENWEATHER_API_KEY}&units=metric&lang=es'
    response = requests.get(url)
    data = response.json()
    return data['weather'][0]['description']

def servidor_openweather_socket():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('localhost', 8000))
    servidor.listen(1)

    print("Servidor OpenWeather (sockets) iniciado en el puerto 8000...")
    while True:
        conn, addr = servidor.accept()
        with conn:
            print(f"Conexión establecida desde {addr}")
            ciudad = conn.recv(1024).decode()
            if not ciudad:
                break
            clima = obtener_clima_socket(ciudad)
            conn.send(clima.encode())

def obtener_descripcion_geonames(lugar):
    url = f'http://api.geonames.org/wikipediaSearchJSON?q={lugar}&maxRows=1&username={GEONAMES_USERNAME}'
    response = requests.get(url)
    data = response.json()
    if 'geonames' in data and data['geonames']:
        return data['geonames'][0]['summary']
    else:
        return "No se encontró una descripción para este lugar."

def servidor_geonames_socket():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('localhost', 9000))
    servidor.listen(1)

    print("Servidor Geonames (sockets) iniciado en el puerto 9000...")
    while True:
        conn, addr = servidor.accept()
        with conn:
            print(f"Conexión establecida desde {addr}")
            lugar = conn.recv(1024).decode()
            if not lugar:
                break
            descripcion = obtener_descripcion_geonames(lugar)
            conn.send(descripcion.encode())

if __name__ == '__main__':
    # Inicia los servidores de sockets en hilos separados
    threading.Thread(target=servidor_openweather_socket, daemon=True).start()
    threading.Thread(target=servidor_geonames_socket, daemon=True).start()

    # Inicia el servidor Flask
    print("Servidor Web Service iniciado en el puerto 5000...")
    app.run(debug=True, host='0.0.0.0', port=5000)
