from socket import * 
import logging

# Configurazione del logging così che vengano resi visibile sul termonale anche i log di info
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

serverPort=8080
#crea una socket TCP facendo uso dell'indirizzamento IPv4
serverSocket = socket(AF_INET, SOCK_STREAM)
serverAddress=('localhost',serverPort)
#collega la socket all'indirizzo del server, è ora pronta ad accettare connessioni sulla porta 8080
serverSocket.bind(serverAddress)

#la socket è in ascolto per richieste di connessione
serverSocket.listen(1)
print("the web server is running and listening on port: ", serverPort)

# Dizionario dei MIME types
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

    #accept blocca il server fino a che non è stata accettata una richiesta di connessione.
    #restituisce quindi una nuova socket per la comunicazione e l'indirizzo del client.
    communicationSocket, clientAddress = serverSocket.accept()
    print("new enstablished socket for comunication: ", communicationSocket)
    print("client address: ", clientAddress)

    try:
        
        #cerca di ricevere dei byte dal client. Massimo 1024
        message = communicationSocket.recv(1024)
        if len(message.split()) > 0: 

            # Log della richiesta ricevuta
            method = message.split()[0].decode()
            filename = message.split()[1].decode()
            logging.info(f"Request from {clientAddress}: {method} {filename}")

            if filename == '/':
                filename = '/index.html'
            filepath = path + filename

            # Determina il MIME type
            ext = '.' + filepath.split('.')[-1]
            mime_type = mime_types.get(ext.lower(), "application/octet-stream")

            #apre il file e se non esiste viene generato un errore di I/O
            f = open(filepath,'rb') 
            outputdata = f.read()

                
            #Invia la riga di intestazione HTTP nel socket con il messaggio OK
            communicationSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
            communicationSocket.send(outputdata)
            communicationSocket.send("\r\n".encode())

            print("")
            

    except IOError:
        # Log dell'errore 404
        logging.warning(f"File not found: {filename} from {clientAddress}")
        #Invia messaggio di risposta per file non trovato
        communicationSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        communicationSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())

    finally:
        communicationSocket.close()


