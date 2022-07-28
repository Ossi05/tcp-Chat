import threading
import socket

# ip ja portti
host ="127.0.0.1" #ip on talla hetkella localhost
port = 55555

# kaynnistaa serverin
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

#Kayttajat ja nimet
clients = []
nicknames = []

# Lahettaa viestin kaikille kayttajille
def broadcast(message):
    for client in clients:
        client.send(message)

        
        
        
        # Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Poistaa kayttajan
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nickname[index]
            broadcast(f"{nickname} left the chat!".encode("ascii"))
            nicknames.remove(nickname)
            break





# Receiving / Listening Function

def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Request And Store Nickname
        client.send("NICK".encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)

         # Print And Broadcast Nickname
        print(f"Nickname of the client is {nickname}!")
        broadcast(f"{nickname} joined the chat!".encode("ascii"))
        client.send("Connected to the server!".encode("ascii"))
        
         # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening...")
receive()