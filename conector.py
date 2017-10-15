#!/usr/bin/env python

import socket
from random import randint
from sys import argv

def servidor_tcp(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #stream de datos
    
    sock.bind(('',int(port))) #atamos puerto

    sock.listen(1) # solo escuchamos hasta una ip simultaneamente

    while 1:
        print('Esperamos a una conexión')
        conn, addr = sock.accept()
        print("Conectado con la direccion:",addr)
        
        while 1:

            data = conn.recv(1024) #recibimos la data desde la conexión
            data = data.decode() # convertimos de byte a string
            if not data: #si data es vacio lo pasamos por alto, es parte del protocolo
                continue

            print('Data recibida:\n\t', data)
            if data == "exit": #salida remota
                print("saliendo...")
                conn.sendall("Saliendo".encode()) # enviamos todo lo pendiente
                sock.close() #cerramos socket (no obligatorio, igual saldremos del programa)
                return 

            

            if data[0] != "|": #si la data no tenia el formato correcto
                mensaje = " error recibido"

            mensaje = "recibido: " + data[1:]

            conn.sendall(mensaje.encode()) #enviamos a la conexión

def cliente_tcp(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #stream de datos
    
    try:
        sock.connect((ip, int(port)))
    except:
        print("¿Estaba el servidor iniciado?\nfalló el intento e conexión")

    while 1:
        try:
            mensaje = input("Escriba un mensaje a enviar: ")

            print()#nueva linea
            
            if mensaje == "exit": #invocamos salida
                print("Cerrando servidor y saliendo")
                sock.send(mensaje.encode()) #enviamos al servidor
                data = sock.recv(16) #recibimos respuesta
                print("recibido desde el servidor:\n\t", data.decode())
                sock.close() #cerramos el socket
                return

            mensaje = "|"+mensaje # usamos nuestro formato de seguridad
            print("Enviando a servidor y esperando respuesta") 
            sock.sendall(mensaje.encode()) #enviamos todo lo pendiente
            data = sock.recv(1024) #esperamos 
            print("recibido desde el servidor:\n\t", data.decode())
        except:
            print("El servidor está caido, terminando...")
            return


def servidor_udp(port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # datagrama
    
    sock.bind(('',int(port))) #atamos el sock al puerto, escuchamos a cualquier ip

    while 1:
        print('Esperando recibir nueva data')
        
        data, addr = sock.recvfrom(1024) #debemos capturar la direccion de la que recibimos para responder
        data = data.decode() # convertimos de byte a string
        if not data: #si data es vacio, asumiremos un error
            print("Se recibió un error, fue ignorado")
            continue

        print('Data recibida desde dirección:', addr)
        if data == "exit": #salida remota
            print("saliendo...")
            sock.sendto("Saliendo".encode(), addr)
            sock.close() #cerramos socket (no obligatorio, igual saldremos del programa)
            return 

        if data[0] != "|": #si la data no tenia el formato correcto
            mensaje = " error recibido"
        
        mensaje = data[1:]
        print("data recibida:\n\t", mensaje)
        
        sock.sendto(mensaje.encode(), addr) #enviamos a la dirección


def cliente_udp(ip, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # datagrama

    while 1:
        mensaje = input("Escriba un mensaje a enviar: ")

        print()#nueva linea
        
        if mensaje == "exit": #invocamos salida
            print("Cerrando servidor y saliendo")
            sock.sendto(mensaje.encode(), (ip, int(port)))
            data = sock.recv(1024) #esperamos respuesa por el puerto que se abrió para enviar
            print("recibido desde el servidor:", data.decode())
            return

        mensaje = "|"+mensaje # usamos nuestro formato de seguridad
        print("Enviando a servidor y esperando respuesta") 
        sock.sendto(mensaje.encode(), (ip, int(port))) 
        data = sock.recv(1024) #esperamos respuesta
        print("recibido desde el servidor:\n\t", data.decode())

if len(argv) < 4 or len(argv) > 5:
    print("Argumentos erroneos")

if argv[1] == "server":
    if argv[2] == "tcp":
        servidor_tcp(argv[3])

    elif argv[2] == "udp":
        servidor_udp(argv[3])

    else:
        print("Argumentos erroneos")

elif argv[1] == "client":
    if argv[2] == "tcp":
        cliente_tcp(argv[3], argv[4])
        
    if argv[2] == "udp":
        cliente_udp(argv[3], argv[4])

    else:
        print("Argumentos erroneos")

else:
    print("Engel gay")
    
    
