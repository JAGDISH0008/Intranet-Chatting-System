from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
import schedule
import threading 
import time


def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        global names
        names = []
        

        print("%s:%s has connected." % client_address)
        names = clients.values()
        #print (clients.values())
        #client.send(bytes("", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

#def 
def handle_client(client):  
    name = client.recv(BUFSIZ).decode("utf8")
    names1 = " "
    welcome = 'Welcome %s! ' % name + "\n " + names1.join(names) + " are online. "
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined " % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name


    while True:
        msg = client.recv(BUFSIZ)
        print(msg)

        if msg == bytes("File_Comming", "utf8"):

            filename = client.recv(BUFSIZ).decode("utf8")
            print(filename+" 123")

            f = open("/home/jagdish/Desktop/Network/Python/Server/Server_data/"+filename,"w")        	
        	
            while True:



                msg1 = client.recv(BUFSIZ)
                print(msg1.decode("utf8"))


                if msg1 != bytes("File_Sent","utf8"):

                    f.write(msg1.decode("utf8"))

                else :
                    break

            f.close()

   
        elif msg == bytes("Image_Comming", "utf8"):
        	Imagename = client.recv(BUFSIZ).decode("utf8")
        	f = open("/home/jagdish/Desktop/Network/Python/Server/Server_data/"+filename,"w")
        	while True:
        		msg1 = client.recv(BUFSIZ)
        		print(msg1.decode("utf8"))
        		if msg1 != bytes("Image_Sent","utf8"):
        			f.write(msg1.decode("utf8"))
        		else:
        			break
        	f.close()


        	

        elif msg == bytes("Queue_msg","utf8"):
            filename = client.recv(BUFSIZ).decode("utf8")+".txt"
            f = open("/home/jagdish/Desktop/Network/Python/Server/Data/"+filename,"a")
            recv_msg = "\n"+client.recv(BUFSIZ).decode("utf8")
            f.write(recv_msg)
            f.close()

        elif msg == bytes("Send_Messages","utf8"):
            client_name = client.recv(BUFSIZ).decode("utf8")
            send_filename = client_name+".txt"
            f = open("/home/jagdish/Desktop/Network/Python/Server/Data/"+send_filename,"r")
            msg_to_send = f.read(1024)
            #key_list = list(clients.keys())
            #val_list = list(clients.values())
            #addr = str(key_list[val_list.index(client_name)])
            client.send(bytes("Sending_data","utf8"))
            time.sleep(1)
            client.send(bytes(msg_to_send,"utf8"))


        elif msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left ." % name, "utf8"))
            break


def broadcast(msg, prefix=""): 
    for sock in clients:
        #print(sock)
        sock.send(bytes(prefix, "utf8")+msg)

 


clients = {}
addresses = {}
HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)


SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

names_online = []	 
def update_client():
	threading.Timer(5.0, update_client).start()
	file = open("clients.txt","w")
	#file.truncate(0)
	names_online = list(clients.values())
	for item in names_online:
		file.write("%s\n" % item)
	#file.write(names_online)
	file.close()



#schedule.every(1).second.do(update_client)
#while 1:
 #   schedule.run_pending()
 #   time.sleep(1)





if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    update_client()
    SERVER.close()
