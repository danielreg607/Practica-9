import socket
import requests

def cliente_web_service():
    print("Seleccione el servicio Web Service:")
    print("1. OpenWeather")
    print("2. Geonames")
    opcion = input("Ingrese el número de la opción deseada: ")

    if opcion == '1':
        ciudad = input("Ingrese el nombre de la ciudad: ")
        response = requests.get(f'http://localhost:5000/weather?city={ciudad}')
        if response.status_code == 200:
            data = response.json()
            print(f"El clima en {ciudad} es {data['description']} con una temperatura de {data['temperature']}°C.")
        else:
            print("Error:", response.json()["error"])
    elif opcion == '2':
        lugar = input("Ingrese el nombre del lugar: ")
        response = requests.get(f'http://localhost:5000/geonames?place={lugar}')
        if response.status_code == 200:
            data = response.json()
            print(f"Descripción de {lugar}: {data['summary']}")
        else:
            print("Error:", response.json()["error"])
    else:
        print("Opción no válida.")

def cliente_socket():
    print("Seleccione el servidor de sockets:")
    print("1. OpenWeather")
    print("2. Geonames")
    opcion = input("Ingrese el número de la opción deseada: ")

    if opcion == '1':
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 8000))
            ciudad = input("Ingrese el nombre de la ciudad: ")
            s.sendall(ciudad.encode())
            data = s.recv(1024)
            print(f"Clima desde servidor de sockets: {data.decode()}")
    elif opcion == '2':
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 9000))
            lugar = input("Ingrese el nombre del lugar: ")
            s.sendall(lugar.encode())
            data = s.recv(1024)
            print(f"Descripción desde servidor de sockets: {data.decode()}")
    else:
        print("Opción no válida.")

def main():
    print("Seleccione el mecanismo de comunicación:")
    print("1. Web Service")
    print("2. Sockets")
    opcion = input("Ingrese el número de la opción deseada: ")

    if opcion == '1':
        cliente_web_service()
    elif opcion == '2':
        cliente_socket()
    else:
        print("Opción no válida.")

if __name__ == '__main__':
    main()

	

