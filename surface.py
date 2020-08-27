import tkinter as tk
from tkinter import font, simpledialog, messagebox, ttk
import threading
from multiprocessing import Process
import time
import socket
import json

import Adafruit_BBIO.GPIO as GPIO
from rfid import RFID

BUZZER = 'P8_10'
DEF_BLOCK = 12
NAME_BLOCK = 13
PRICE_BLOCK = 14
rdr = RFID()
state = 'READ'

window = tk.Tk()
tree = ttk.Treeview(window)
member_name = tk.Label(window, text='None', font=('Times', 14), bg='white')


def buzzer():
    GPIO.setup(BUZZER, GPIO.OUT)
    GPIO.output(BUZZER, GPIO.HIGH)
    time.sleep(0.3)
    GPIO.output(BUZZER, GPIO.LOW)

def read_product():
	global state
	while True:
		time.sleep(3)
		print(state)
		if state == 'READ':
			result = rfid_read()
			if result:
				print(result)
				if len(result) == 1:
					print('member')
					member_name['text'] = result[0]
				elif len(result) == 2:
					print('read result: ', result[0], result[1])
					tree.insert("",0,values=result)


# input a string return a list of number(ascii code)
def str_to_ascii(tar):
	ascii = []
	for t in tar:
		ascii.append(ord(t))
	ascii.append(3)
	return ascii

# input a list of number(ascii code) return a string
def ascii_to_str(tar):
	string = ''
	for t in tar:
		if t == 3:
			return string
		string = string + chr(t)

# input a string and write to rfid tag
def write_to_rfid(target, block):
	target = str_to_ascii(target)
	count = 0
	while len(target) > 0:
		if len(target) > 16:
			temp = target[:16]
			if rdr.write(block+count, temp):
				return 'error'
			print('write', block+count, temp)
			target = target[16:]
			count = count + 1
		else:
			n = 16-len(target)
			zero = [0 for i in range(n)]
			target = target + zero
			if rdr.write(block+count, target):
				return 'error'
			print('write', block+count, target)
			target = []
	return 'OK'

# input block number output a string
def read_from_rfid(block):
	result = []
	while True:
		data = rdr.read(block)
		if data[0]:
			return 'error'
		result = result + data[1]
		if 3 in data[1]:
			break
		else:
			block = block +1
	result = ascii_to_str(result)
	return result

# if there is an error return False otherwise 
# 1. return (member) if that is a member card.
# 2. return (name, price) if that is a product tag
def rfid_read():
	rdr.wait_for_tag()
	buzzer()
	(error, tag_type) = rdr.request()
	if not error:
		print("Tag detected")
		(error, uid) = rdr.anticoll()
		if not error:
			print("UID: " + str(uid))
			if not rdr.select_tag(uid):
				if not rdr.card_auth(rdr.auth_a, 14, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], uid):
					definition = read_from_rfid(DEF_BLOCK)
					if definition == 'product':
						name = read_from_rfid(NAME_BLOCK)
						price = read_from_rfid(PRICE_BLOCK)
						rdr.stop_crypto()
						if name == 'error' or price == 'error':
							return False
						else:
							# print("Reading: " ,(name, price))
							return (name, price)
					else:
						with open("members.json",'r') as load_f:
							load_dict = json.load(load_f)
							if str(uid) == load_dict['uid']:
								return (load_dict['name'],)


# if there is an error return False otherwise reutrn Ture
def rfid_write(name, price):
	rdr.wait_for_tag()
	buzzer()
	(error, tag_type) = rdr.request()
	if not error:
		print("Tag detected")
		(error, uid) = rdr.anticoll()
		if not error:
			print("UID: " + str(uid))
			if not rdr.select_tag(uid):
				if not rdr.card_auth(rdr.auth_a, 14, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], uid):
					ed1 = write_to_rfid(name, NAME_BLOCK)
					ed2 = write_to_rfid(price, PRICE_BLOCK)
					ed3 = write_to_rfid('product',DEF_BLOCK)
					rdr.stop_crypto()
					if ed1 =='error' or ed2 =='error' :
						return False
					else:
						return True

def network(message):
	hostname = '192.168.9.102'
	port = 6666
	addr = (hostname,port)
	clientsock = socket.socket()
	clientsock.connect(addr)
	message = str(message)
	clientsock.send(bytes(message, encoding='utf8'))
	recvdata = clientsock.recv(1024)
	print(str(recvdata,encoding='utf8'))
	clientsock.close()

def checkout():
	items = []
	children = tree.get_children("")
	for child in children:
		items.append(tree.item(child)["values"][0])
	transection = {
	"member" : member_name['text'],
	"items" : items
	}

	network(transection)
	member_name['text'] = 'None'
	tree.delete(*tree.get_children())

def member():
	global state
	state = 'WRITE'
	member_win = tk.Tk()
	uid_entry = tk.Entry(member_win)

	def member_comfirm():
		global state
		new_name = name.get()
		new_phone = phone.get()
		new_uid = uid_entry.get()

		new_memboer = {
		'uid' : new_uid,
		"name" : new_name,
		"phone" : new_phone
		}
		with open("members.json","w") as f:
			json.dump(new_memboer,f)
		state = 'READ'
		member_win.destroy()
		messagebox.showinfo('Success','Add new member success')

	# if there is an error return False otherwise reutrn uid
	def read_new_member():
		rdr.wait_for_tag()
		buzzer()
		(error, tag_type) = rdr.request()
		if not error:
			print("Tag detected")
			(error, uid) = rdr.anticoll()
			if not error:
				uid_entry.insert(0,str(uid))
				return True
			else:
				print('get uid error')
				return False

	# define the member window
	member_win.geometry('300x250')
	member_win.title('New Meneber')
	title = tk.Label(member_win, text='Please scan a rfid card...',font=("Times", 12, "italic")).place(x=20, y=20, anchor='nw')
	t0 = tk.Label(member_win, text='uid :').place(x=20, y=60, anchor='nw')
	uid_entry.place(x=65, y=60, anchor='nw')
	t1 = tk.Label(member_win, text='name :').place(x=20, y=100, anchor='nw')
	name = tk.Entry(member_win)
	name.place(x=65, y=100, anchor='nw')
	t2 = tk.Label(member_win, text='phone :').place(x=20, y=140, anchor='nw')
	phone = tk.Entry(member_win)
	phone.place(x=65, y=140, anchor='nw')
	comfirm_btn = tk.Button(member_win,text=' confirm ',font=('Times', 10), command=member_comfirm, bg='white').place(x=60, y=180, anchor='nw')

	s = threading.Thread(target = read_new_member)
	s.start()

	member_win.mainloop()
	


def regist():
	global state
	state = 'WRITE'

	def reg_comfirm():
		global state
		# define wait_tag window
		# wait_tag = tk.Tk()
		# wait_tag.geometry('300x100')
		# wait_tag.title('Wait for tag...')
		# title = tk.Label(wait_tag, text='Please detect a tag...',font=("Times", 12, "italic")).place(x=20, y=20, anchor='nw')

		# get data from window
		new_name = name.get()
		new_price = price.get()
		reg_win.destroy()

		if not rfid_write(new_name, new_price):
			#wait_tag.destroy()
			state = 'READ'
			messagebox.showerror('Errro','Write to RFID error')
		else:
			#wait_tag.destroy()
			state = 'READ'
			messagebox.showinfo('Success','Write to RFID success')
		# wait_tag.mainloop()

	# define the registering window
	reg_win = tk.Tk()
	reg_win.geometry('300x200')
	reg_win.title('New Product')
	title = tk.Label(reg_win, text='Please type the information',font=("Times", 12, "italic")).place(x=20, y=20, anchor='nw')
	t2 = tk.Label(reg_win, text='name :').place(x=20, y=60, anchor='nw')
	name = tk.Entry(reg_win)
	name.place(x=65, y=60, anchor='nw')
	t3 = tk.Label(reg_win, text='price :').place(x=20, y=100, anchor='nw')
	price = tk.Entry(reg_win)
	price.place(x=65, y=100, anchor='nw')
	comfirm_btn = tk.Button(reg_win,text=' confirm ',font=('Times', 10), command=reg_comfirm, bg='white').place(x=60, y=140, anchor='nw')
	reg_win.mainloop()


def mainwindow():
	# define the main window
	window.configure(background='white')
	window.title('Smart Cashier')
	window.geometry('600x400')
	checkout_btn = tk.Button(window,text='Check Out',font=('Times', 12), command=checkout, bg='yellow').place(x=475, y=50, anchor='nw')
	regist_btn = tk.Button(window,text='New Product',font=('Times', 12), command=regist, bg='yellow').place(x=475, y=110, anchor='nw')
	regist_btn = tk.Button(window,text='New Member',font=('Times', 12), command=member, bg='yellow').place(x=475, y=170, anchor='nw')
	t4 = tk.Label(window, text='Buy list :', font=('Times', 14), bg='white').place(x=20, y=20, anchor='nw')
	t5 = tk.Label(window, text='Memeber :', font=('Times', 14), bg='white').place(x=20, y=300, anchor='nw')
	member_name.place(x=130, y=300, anchor='nw')

	tree["columns"]=("product","price")
	tree.column("product",width=120)
	tree.column("price",width=120)

	tree.heading("product",text="product")
	tree.heading("price",text="price")

	tree.place(x=20, y=50, anchor='nw')
	window.mainloop()


if __name__=="__main__":
	t = threading.Thread(target = read_product)
	# t = Process(target = read_product,args=())
	t.start()
	mainwindow()
