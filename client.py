from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
from tkinter import filedialog, simpledialog
import os
import shutil
#from test3 import *
from tkinter import *
import tkinter.messagebox as tm
from OpenSSL import rand
import time
import datetime




Packet_Size = 1024


#from attach_client import *
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            if msg == "Sending_data":
            	get_msg()
            else:
            	msg_list.insert(tk.END, msg)
        except OSError:  
            break


def send(event=None):  

    msg = my_msg.get()
    my_msg.set("")  
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        homepage.quit()

def file_client(filename):
	f = open(filename,'r') 
	l = f.read(1024)
	l = str(l)
	while(l):
		client_socket.send(bytes(l,"utf8"))
		l = f.read(1024)
		l = str(l)
	f.close()
	time.sleep(1)
	file_sent_ack()

def file_sent_ack():
	client_socket.send(bytes("File_Sent","utf8"))


def image_client(filename):
	fp = open(filename,'rb')
	i = fp.read(1024)
	i = str(i)
	while (i):
		client_socket.send(bytes(i,"utf8"))
		i = fp.read(1024)
		i = str(i)
	fp.close()
	time.sleep(1)
	image_sent_ack()
	
def image_sent_ack():
	client_socket.send(bytes("Image_Sent","utf8"))


def on_closing(event=None):
    
    my_msg.set("{quit}")
    send()


def attach():
	
	attach_window = tk.Toplevel(master = homepage)
	my_filetypes = [('all files', '.*'), ('text files', '.txt')]
	filepath = filedialog.askopenfilename(parent=attach_window,initialdir=os.getcwd(),title="Please select a file:",filetypes=my_filetypes)
	head, tail = os.path.split(filepath)
	
	filename = tail
	filename1 = filename + " has been sent"

	
	
	if filepath.endswith(".txt"):
		#l1 = "File_Comming"
		#l2 = "\0"*max(1024-len(l1))
		#l2 = str(l2)
		#l3 = "\x00"*max(1024-len(filename))
		#l3 = str(l3)
		#l2 = bytearray(1024-len(filename))
		#b = rand.bytes(1024-len(filename))
		client_socket.sendall(bytes("File_Comming" ,"utf8"))
		time.sleep(2)
		send_filename(filename)


		#client_socket.sendall(bytes(filename  ,"utf8"))
		#client_socket.sendall(b)
		time.sleep(2)


		file_client(filename)
		time.sleep(2)
		send_ack_end(filename1)

	else :
		client_socket.sendall(bytes("Image_Comming" ,"utf8"))
		time.sleep(2)
		send_filename(filename)
		time.sleep(2)
		image_client(filename)
		time.sleep(2)
		send_ack_end(filename1)
	

def send_filename(filename):
	client_socket.send(bytes(filename,"utf8"))
def send_ack_end(filename1):
	client_socket.sendall(bytes(filename1, "utf8"))

BUFSIZ = 1024
HOST = "127.0.0.1"
PORT = 33000
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
usernames = []
usernames = ["jagadeesh","ayyappa","vinay","admin"]
passwords = {}
passwords = {"jagadeesh" :"password1","ayyappa" : "password2", "vinay" : "password3", "admin" : "password4"}
def sendn():
	client_socket.send(bytes(username1, "utf8"))
	
def HomePage():
	global homepage
	master.withdraw()
	homepage = tk.Toplevel(master)
	homepage.title("Messenger")
	messages_frame = tk.Frame(homepage)
	global my_msg
	my_msg = tk.StringVar()
	scrollbar = tk.Scrollbar(messages_frame)
	global msg_list
	msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
	scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
	msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
	msg_list.pack()
	messages_frame.pack()
	src = "/home/jagdish/Desktop/Network/Python"
	dst = "/home/jagdish/Desktop/Network/Server"
	client_socket.send(bytes(username1, "utf8"))
	entry_field = tk.Entry(homepage, textvariable=my_msg)
	entry_field.bind("<Return>", send)
	entry_field.pack()
	send_button = tk.Button(homepage, text="Send", command=send)
	attach_button = tk.Button(homepage,text="Attach", command=attach)
	p2p_button = tk.Button(homepage,text="Send_P2P", command=p2p_window)
	ask_msg_button = tk.Button(homepage,text="Refresh", command=ask_msg)
	display_msg_button = tk.Button(homepage,text="Display_Messages", command=display_msg)
	send_button.pack(side = tk.LEFT)
	attach_button.pack(side=tk.LEFT)
	p2p_button.pack(side=tk.LEFT)
	ask_msg_button.pack(side=tk.LEFT)
	display_msg_button.pack(side=tk.LEFT)
	
	homepage.protocol("WM_DELETE_WINDOW", on_closing)



def p2p_window():
	global newpage
	global entry_to
	global entry_message
	newpage = tk.Toplevel(homepage)
	newpage.title("Compose")
	label_to = Label(newpage, text="To")
	label_message = Label(newpage, text="Message BOX")
	entry_to = Entry(newpage)
	#global p2p_msg
	#p2p_msg = tk.StringVar()
	entry_message = Entry(newpage)
	label_to.grid(row=0, sticky=E)
	label_message.grid(row=1, sticky=E)
	entry_to.grid(row=0, column=1)
	entry_message.grid(row=1, column=1)
	sendbtn = Button(newpage, text="Send", command=msgdata)
	sendbtn.grid(columnspan=2)
	newpage.geometry("500x300")




def msgdata():
	client_socket.send(bytes("Queue_msg","utf8"))
	time.sleep(1)
	filename()
	time.sleep(1)
	msg_send()




def filename():
	data_filename = entry_to.get()
	client_socket.send(bytes(data_filename,"utf8"))


def msg_send():
	message = entry_message.get()
	currentDT = datetime.datetime.now()
	data_message = "[ " + str(currentDT.strftime("%Y-%m-%d %H:%M:%S"))+ " ] " + username1 + " : " + message
	client_socket.sendall(bytes(data_message,"utf8"))
	time.sleep(1)
	newpage.withdraw()

def ask_msg():
	client_socket.send(bytes("Send_Messages","utf8"))
	time.sleep(1)
	client_socket.send(bytes(username1,"utf8"))

def get_msg():
	msg1 = client_socket.recv(BUFSIZ)
	file = open(username1+".txt","a")
	file.truncate(0)
	file.write(msg1.decode("utf8"))
	file.close()

def display_msg():
	global newpage2
	newpage2 = tk.Toplevel(homepage)
	newpage2.title("Messages")
	text = Text(newpage2)
	f = open(username1+".txt","r")
	total_data = f.read()
	f.close()
	text.insert(INSERT,total_data)
	text.pack()



def _login_btn_clicked():
        # print("Clicked")
        global username1
        username1 = entry_username.get()
        password1 = entry_password.get()

        # print(username, password)

        if ((username1) in usernames) and (password1 == passwords.get(username1)):
            #tm.showinfo("Login info", "Welcome John")
            #client_socket.send(bytes(username1, "utf8"))
            master.after(1000, HomePage)
        else:
            tm.showerror("Login error", "Incorrect username")


 
master = tk.Tk()

label_username = Label(master, text="Username")
label_password = Label(master, text="Password")

entry_username = Entry(master)
entry_password = Entry(master, show="*")
#self.msg1 = tk.Message(self.master,text ="Enter_Username_and_Password").pack()
label_username.grid(row=0, sticky=E)
label_password.grid(row=1, sticky=E)
entry_username.grid(row=0, column=1)
entry_password.grid(row=1, column=1)

checkbox = Checkbutton(master, text="Keep me logged in")
checkbox.grid(columnspan=2)

logbtn = Button(master, text="Login", command=_login_btn_clicked)
logbtn.grid(columnspan=2)

   
master.geometry("500x300")
master.title("Login Page")
#master.pack()


receive_thread = Thread(target=receive)
receive_thread.start()
tk.mainloop()  

