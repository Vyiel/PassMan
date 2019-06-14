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
        try:
            self.c.execute("INSERT INTO userinfo (uname, passw, service) VALUES (?, ?, ?)",
                           (self.uname, self.passw, self.service))
            self.conn.commit()
            print "Information for " + self.uname + " Saved to Database successfully"
            print db.read_all()
            main()
        except:
            "Couldn't save to Database!!!"
            main()

    def read_all(self):
        self.c.execute("SELECT * FROM userinfo")
        return self.c.fetchall()

    def read_one(self, id):
        self.id = id
        self.c.execute("SELECT * FROM userinfo WHERE ID = ?", [self.id])
        return self.c.fetchone()

    def update(self, uname, passw, service, id):
        self.uname = uname
        self.passw = passw
        self.service = service
        self.id = id
        try:
            self.c.execute \
                ("""
            UPDATE userinfo SET uname=?, passw=?, service=? WHERE ID = ?"""
                 , (self.uname, self.passw, self.service, self.id))
            self.conn.commit()
            print "Credentials updated successfully"
            main()
        except:
            "Couldn't Update Database!!!"
            main()

    def remove(self, id):
        self.id = id
        try:
            self.c.execute("DELETE FROM userinfo WHERE ID = ?", [self.id])
            self.conn.commit()
            print "Credentials successfully removed"
            print db.read_all()
            main()
        except:
            print "Couldn't delete information from Database!!!"
            main()


class login:
    def google(self, uname, passw):
        self.uname = uname
        self.passw = passw
        driver = webdriver.Chrome('C:\chromedriver')
        driver.get(
            'https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
        driver.find_element_by_id("identifierId").send_keys(self.uname)
        driver.find_element_by_class_name('CwaK9').click()
        time.sleep(2)
        driver.find_element_by_name("password").send_keys(passw)
        driver.find_element_by_class_name("CwaK9").click()
        driver.close()
        main()

    def facebook(self, uname, passw):
        self.uname = uname
        self.passw = passw
        driver = webdriver.Chrome('C:\chromedriver')
        driver.get('https://www.facebook.com')
        time.sleep(2)
        driver.find_element_by_id('email').send_keys(self.uname)
        driver.find_element_by_id('pass').send_keys(self.passw)
        driver.find_element_by_id('u_0_a').click()
        driver.close()
        main()


class basic:
    found = False
    listall = {}
    list_of_id = []

    def __init__(self):
        listInfo = db.read_all()
        if len(listInfo) == 0:
            print "There is no information in the database. Please add logins first!!! "
            main()
        else:
            for i in listInfo:
                id = int(i[0])
                name = str(i[1])
                service = str(i[3])
                listall[id] = name, service




    def check_id(self, id, list_of_id):
        self.id = id
        self.list_of_id = list_of_id

        if self.id in self.list_of_id:
            return True
        else:
            return False

    @staticmethod
    def display():

        print "--> All Accounts <--"

        for items in listall:
            if listall[items][1] == "ggl":
                service = "Google"
            elif listall[items][1] == "fb":
                service = "Facebook"

            print (str(items) +"     "+ listall[items][0]+"     "+ service)
        print


    @staticmethod
    def add():
        while True:
            uname = raw_input('Enter Username: ')
            passw = raw_input('Enter Password: ')
            service = raw_input('Enter Service -> ggl for "Google" and fb for "Facebook" : ')
            if service == "ggl" or service == "fb":
                db.save(uname, passw, service)
                break
            else:
                print ("Incorrect Service Name!")
                continue



    @staticmethod
    def update():
        print "--> Update Accounts <--"
        for items in listall:
            if listall[items][1] == "ggl":
                service = "Google"
            elif listall[items][1] == "fb":
                service = "Facebook"

            print (str(items) + "     " + listall[items][0] + "     " + service)
        print

        while True:
            try:
                select = int(input("Enter choice of ID from before the User Names to Update: "))
                break
            except:
                print "selection type for update not integer!!! "
                continue

        list_of_id = listall.keys()
        opt = bf.check_id(select, list_of_id)
        if opt is True:
            uname = raw_input('Enter Username to update: ')
            passw = raw_input('Enter Password to update: ')
            while True:
                service = raw_input('Enter Service initials: ex:- "ggl/fb": ')
                if service == "ggl" or service == "fb":
                    db.update(uname, passw, service, select)
                    break
                else:
                    print "Service Initials are not correct!!! "
                    continue
        else:
            print "User information for this ID not found in the Database"

    @staticmethod
    def delete():
        print "--> Delete Accounts <--"
        for items in listall:
            if listall[items][1] == "ggl":
                service = "Google"
            elif listall[items][1] == "fb":
                service = "Facebook"

            print (str(items) + "     " + listall[items][0] + "     " + service)
        print

        while True:
            try:
                select = int(input("Enter choice of ID from before the User Names to Delete: "))
                break
            except:
                print "selection type for deletion not integer!!! "
                continue

        list_of_id = listall.keys()
        opt = bf.check_id(select, list_of_id)

        if opt is True:
            db.remove(select)
        else:
            print "User information for this ID not found in the Database"
            main()


    @staticmethod
    def login():
        print "--> Login <--"
        for items in listall:
            if listall[items][1] == "ggl":
                service = "Google"
            elif listall[items][1] == "fb":
                service = "Facebook"

            print (str(items) + "     " + listall[items][0] + "     " + service)
        print

        while True:
            try:
                select = int(input("Enter choice of ID from before the User Names to Login: "))
                break
            except:
                print "selection type for deletion not integer!!! "
                continue

        list_of_id = listall.keys()
        opt = bf.check_id(select, list_of_id)
        if opt is True:
            creds = db.read_one(select)
            uname = creds[1]
            passw = creds[2]
            service = creds[3]
            if service == "ggl":
                lg.google(uname, passw)
            elif service == "fb":
                lg.facebook(uname, passw)
            else:
                print "Invalid Service!!!"
        else:
            print "User information for this ID not found in the Database"
            main()


db = db_methods()
bf = basic()
lg = login()

def main():
    basic()
    sdict_select = int()
    sdict_res = str()

    print """
        --> Choice of Options <--
        
        1 -> Display Accounts
        2 -> Add User Information
        3 -> Update User Information
        4 -> Delete User Information
        5 -> Login with Credentials
    
        """

    sdict = {
        1: bf.display,
        2: bf.add,
        3: bf.update,
        4: bf.delete,
        5: bf.login
    }

    while True:

        try:
            sdict_select = int(input("Enter choice of action: "))
            sdict_res = sdict.get(sdict_select, False)()
            break

        except:
            print ("Invalid Selection!!! ")
            continue

if __name__ == '__main__':
    main()






# TEST RUN FOR INDIVIDUAL DATABASE FUNCTIONS #
# db.save('whatever u', 'whatever p', 'ggl') # WORKS FINE #
# print db.read_all() # WORKS FINE #
# print db.read_one(2) # WORKS FINE #
# db.update('what', 'what', 'fb', 3) # WORKS FINE #
# db.remove(3) # WORKS FINE #

# TEST RUN FOR INDIVIDUAL BASIC FUNCTIONS #
# bf.add() # WORKS FINE AFTER MODIFICATION #
# bf.update() # WORKS FINE #
# bf.login() # WORKS FINE #
# bf.delete() # WORKS FINE #
# bf.display() # WORKS FINE #