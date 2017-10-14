# MinimoEjemploSocket
Ejemplo minimo de uso para socket tcp y udp

argumentos para servidor
./conector server tcp [puerto]
./conector server udp [puerto]

para cliente
./conector client tcp [ip] [puerto]
./conector client udp [ip] [puerto]

ejemplo 
(en el servidor)
./conector server udp 3600

(en el cliente)
./conector cliente udp 127.0.0.1 3600

para salir, enviar el mensaje "exit"
