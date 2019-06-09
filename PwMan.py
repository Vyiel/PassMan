import sqlite3
from selenium import webdriver
import time

listall = {}
id = []
name = []

class db_methods:

    def __init__(self):
        self.conn = sqlite3.connect('db')
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS userinfo
            (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                uname TEXT,
                passw TEXT,
                service TEXT
            )
            """)
        self.conn.commit()

    def save(self, uname, passw, service):
        self.uname = uname
        self.passw = passw
        self.service = service
        self.c.execute("INSERT INTO userinfo (uname, passw, service) VALUES (?, ?, ?)", (self.uname, self.passw, self.service))
        self.conn.commit()


    def read_all(self):
        self.c.execute("SELECT * FROM userinfo")
        return self.c.fetchall()

    def read_one(self, id):
        self.self = id
        self.c.execute("SELECT * FROM userinfo WHERE ID = ?", [self.id])
        return self.c.fetchone()



    def update(self, uname, passw, service, id):
        self.uname = uname
        self.passw = passw
        self.service = service
        self.id = id
        self.c.execute("UPDATE userinfo SET uname, passw, service WHERE uname = ?", [self.id])
        self.conn.commit()

    def remove(self, id):
        self.id = id
        self.c.execute("DELETE FROM userinfo WHERE ID = ?", self.id)
        self.conn.commit()

class login:
    def google(self, uname, passw):
        self.uname = uname
        self.passw = passw
        driver = webdriver.Chrome('C:\chromedriver')
        driver.get('https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
        driver.find_element_by_id("identifierId").send_keys(self.uname)
        driver.find_element_by_class_name('CwaK9').click()
        time.sleep(2)
        driver.find_element_by_name("password").send_keys(passw)
        driver.find_element_by_class_name("CwaK9").click()
        driver.close()

    def facebook(self, uname, passw):
        self.uname = uname
        self.passw = passw
        driver = webdriver.Chrome('C:\chromedriver')
        driver.get('https://www.facebook.com')
        time.sleep(1)
        driver.find_element_by_id('email').send_keys(self.uname)
        driver.find_element_by_id('pass').send_keys(self.passw)
        driver.find_element_by_id('u_0_8').click()
        driver.close()

class basic:
    found = False
    def check_id(self, id, list_of_id):
        self.id = id
        self.list_of_id = list_of_id

        if self.id in self.list_of_id:
            return True
        else:
            return False

    def add(self):
        while True:
            uname = raw_input('Enter Username: ')
            passw = raw_input('Enter Password: ')
            service = raw_input('Enter Service "ggl/fb": ')
            if service != "ggl" or service != "fb":
                print ("Incorrect Service Name!")
                return False

            db.save(uname, passw, service)

    def update(self):
        while True:
            uname = raw_input('Enter Username to update: ')
            passw = raw_input('Enter Password to update: ')
            service = raw_input('Enter Service "ggl/fb" to update: ')
            if service != "ggl" or service != "fb":
                print ("Incorrect Service Name")
                return False

    def display(self):
        listInfo = db.read_all()
        for i in listInfo:
            id = int(i[0])
            name = str(i[1])
            listall[id] = name

        for items in listall:
            print items, listall[items]






db = db_methods()
bf = basic()
lg = login()




select = int(input("Enter selection: "))

list_of_id = listall.keys()
a = bf.check_id(select, list_of_id)























