from socket import * 
import logging
import os

#Configurazione del logging per rendere visibili sul terminale anche i log di livello info
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

serverPort=8080
#Creazione di una socket TCP con indirizzamento IPv4
serverSocket = socket(AF_INET, SOCK_STREAM)
serverAddress=('localhost',serverPort)
#Collegamento della socket all'indirizzo del server
serverSocket.bind(serverAddress)

#La socket è in ascolto per richieste di connessione
serverSocket.listen(1)
print("the web server is running and listening on port: ", serverPort)

#Dizionario dei MIME types
mime_types = {
    ".html": "text/html",
    ".css": "text/css",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".txt": "text/plain"
}

path = 'www'

while True:

    #Blocca il server fino a che non è stata accettata una richiesta di connessione.
    #Restituisce quindi una nuova socket per la comunicazione e l'indirizzo del client.
    communicationSocket, clientAddress = serverSocket.accept()
    print("new enstablished socket for comunication: ", communicationSocket)
    print("client address: ", clientAddress)

    try:
        
        #Cerca di ricevere una richiesta dal client. Massimo 1024 bytes
        message = communicationSocket.recv(1024)
        if len(message.split()) > 0: 

            #Log della richiesta ricevuta
            method = message.split()[0].decode()
            filename = message.split()[1].decode()
            logging.info(f"Request from {clientAddress}: {method} {filename}")

            if filename == '/':
                filename = '/index.html'
            filepath = os.path.join(path, filename.lstrip('/'))

            #Determina il MIME type
            ext = '.' + filepath.split('.')[-1]
            mime_type = mime_types.get(ext.lower(), "application/octet-stream")

            #Il file viene aperto in modalità binaria
            f = open(filepath,'rb') 
            outputdata = f.read()

                
            #Invia l'header HTTP 200 OK, il Content-Type e il contenuto del file in bytes
            communicationSocket.send("HTTP/1.1 200 OK\r\n".encode())
            communicationSocket.send(f"Content-Type: {mime_type}\r\n\r\n".encode())
            communicationSocket.send(outputdata)
            communicationSocket.send("\r\n".encode())

            print("")
            

    except IOError:
        #Log dell'errore 404
        logging.warning(f"File not found: {filename} from {clientAddress}")
        #Invia l'header HTTP 404 Not Found e una semplice pagina html di errore
        communicationSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        communicationSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())

    finally:
        communicationSocket.close()


