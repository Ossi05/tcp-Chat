import socket
import threading

#Valitse nimi
nickname = input("Choose your nickname: ")
if nickname == 'admin':
    password = input("Enter password for admin: ")

#Yhdistaa serveriin
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1',55555))

stop_thread = False


# Listening to Server and Sending Nickname
def recieve():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                #Salasana
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Connection was refused! Wrong password!")
                        stop_thread = True
                elif next_message == 'BAN':
                    print('Connection refused because of ban!')
                    client.close()
                    stop_thread = True

                    
                
            else:
                print(message)

        except:
            #Sulkee yhteyden kun tulee error
            print('An error occured!')
            client.close()
            break
#Lahettaa viesteja serverille
def write():
    while True:
        if stop_thread:
            break


        message = f'{nickname}: {input("")}'
        
        #Ohittaa nimen ja katsoo jos viesti alkaa / merkilla
        if message[len(nickname)+2:].startswith('/'):
            #Jos nimi on admin
            if nickname == 'admin':
                if message[len(nickname)+2:].startswith('/kick'):
                    client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('ascii'))
                elif message[len(nickname)+2:].startswith('/ban'):
                    client.send(f'BAN {message[len(nickname)+2+5:]}'.encode('ascii'))

            else:
                print("Commands can only be executed by the admin!")
        else:
            client.send(message.encode('ascii'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=recieve)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()