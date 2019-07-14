import sqlite3
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from selenium import webdriver
import time
import sys

listall = {}
id = []
name = []

class Db_methods:


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

        self.conn = sqlite3.connect('db')
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS secret
                (
                    ID INTEGER PRIMARY KEY,
                    master_pass TEXT
                )
                """)
        self.conn.commit()

    def save(self, uname, passw, service):

        try:
            self.c.execute("INSERT INTO userinfo (uname, passw, service) VALUES (?, ?, ?)",
                           (uname, passw, service))
            self.conn.commit()
            print("Information for " + uname + " Saved to Database successfully")
            #main()
        except:
            "Couldn't save to Database!!!"
            #main()

    def read_all(self):
        self.c.execute("SELECT * FROM userinfo")
        return self.c.fetchall()

    def read_one(self, id):
        self.c.execute("SELECT * FROM userinfo WHERE ID = ?", [id])
        return self.c.fetchone()

    def update(self, uname, passw, service, id):

        try:
            self.c.execute \
                ("""
            UPDATE userinfo SET uname=?, passw=?, service=? WHERE ID = ?"""
                 , (uname, passw, service, id))
            self.conn.commit()
            print("Credentials updated successfully")
            #main()
        except:
            "Couldn't Update Database!!!"
            #main()

    def remove(self, id):
        try:
            self.c.execute("DELETE FROM userinfo WHERE ID = ?", [id])
            self.conn.commit()
            print("Credentials successfully removed")
            #main()
        except:
            print("Couldn't delete information from Database!!!")
            #main()

    def save_pass(self, master_pass):
        global id
        id = 1
        try:
            self.c.execute("INSERT INTO secret (id, master_pass) VALUES (?, ?)", (id, master_pass))
            print("Master Password Successfully being saved!!! ")
            #main()
        except:
            print("Couldn't save to Database!!!")
            #main()

    def update_pass(self, master_pass):
        id = 1
        try:
            self.c.execute("UPDATE secret SET passw=? WHERE ID=?", (master_pass, id))
            print("Password successfully updated!!! ")
            #main()
        except:
            print("Couldn't update to Database")
            #main()

    def retrieve_pass(self):
        id = 1
        self.c.execute("SELECT master_pass FROM secret WHERE ID = ?", [id])
        return self.c.fetchone()


    def remove_pass(self):
        id = 1
        try:
            self.c.execute("DELETE FROM secret WHERE ID = ?", [id])
            self.conn.commit()
            print("Password successfully removed")
            #main()
        except:
            print("Couldn't remove password from Database!!!")
            #main()




class Login:
    def google(self, uname, passw):
        self.uname = uname
        self.passw = passw
        chromedriver_location = 'C:\chromedriver'
        try:
            driver = webdriver.Chrome(chromedriver_location)
        except:
            print("""Probably The chrome driver is not matched with your current one.
            Please update chrome to the latest version, and download and save the latest
            stable version of chromedriver on to C:\\ """)

        target = 'https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin'
        driver.get(target)

        driver.find_element_by_id("identifierId").send_keys(self.uname)
        driver.find_element_by_class_name('CwaK9').click()
        time.sleep(2)
        driver.find_element_by_name("password").send_keys(passw)
        driver.find_element_by_class_name("CwaK9").click()
        # driver.close()
        # #main()

    def facebook(self, uname, passw):
        self.uname = uname
        self.passw = passw
        driver = webdriver.Chrome('C:\chromedriver')
        driver.get('https://www.facebook.com')
        time.sleep(2)
        driver.find_element_by_id('email').send_keys(self.uname)
        driver.find_element_by_id('pass').send_keys(self.passw)
        driver.find_element_by_id('login_form').submit()
        driver.close()
        #main()


class Helper:
    listall = {}
    list_of_id = []

    def __init__(self):
        listall.clear()
        self.db = Db_methods()
        self.lg = Login()
        listInfo = self.db.read_all()
        if len(listInfo) == 0:
            print("There is no information in the database. Please add logins first!!! ")
        else:
            for i in listInfo:
                id = int(i[0])
                name = str(i[1])
                service = str(i[3])
                listall[id] = name, service

    @staticmethod
    def check_id(id, list_of_id):
        if id in list_of_id:
            return True
        else:
            return False
    @staticmethod
    def display():

        print("--> All Accounts <--")

        for items in listall:
            if listall[items][1] == "ggl":
                service = "Google"
            elif listall[items][1] == "fb":
                service = "Facebook"

            print(str(items) +"     "+ listall[items][0]+"     "+ service)
        print("")


    def add(self):
        while True:
            uname = input('Enter Username: ')
            passw = input('Enter Password: ')
            service = input('Enter Service -> ggl for "Google" and fb for "Facebook" : ')
            if service == "ggl" or service == "fb":
                self.db.save(uname, passw, service)
                break
            else:
                print("Incorrect Service Name!")
                continue


    def update(self):
        self.display()

        while True:
            try:
                select = int(input("Enter choice of ID from before the User Names to Update: "))
                break
            except:
                print("selection type for update not integer!!! ")
                continue

        list_of_id = listall.keys()
        opt = self.check_id(select, list_of_id)
        if opt is True:
            uname = input('Enter Username to update: ')
            passw = input('Enter Password to update: ')
            while True:
                service = input('Enter Service initials: ex:- "ggl/fb": ')
                if service == "ggl" or service == "fb":
                    self.db.update(uname, passw, service, select)
                    break
                else:
                    print("Service Initials are not correct!!! ")
                    continue
        else:
            print("User information for this ID not found in the Database")

    def delete(self):
        print("--> Remove Accounts <--")
        self.display()

        while True:
            try:
                select = int(input("Enter choice of ID from before the User Names to Delete: "))
                break
            except:
                print("selection type for deletion not integer!!! ")
                continue

        list_of_id = listall.keys()
        opt = self.check_id(select, list_of_id)
        if opt is True:
            self.db.remove(select)
        else:
            print("User information for this ID not found in the Database")


    def login(self):
        print("--> Login <--")
        self.display()

        while True:
            try:
                select = int(input("Enter choice of ID from before the User Names to Login: "))
                break
            except:
                print("selection type for deletion not integer!!! ")
                continue

        list_of_id = listall.keys()
        opt = self.check_id(select, list_of_id)
        if opt is True:
            creds = self.db.read_one(select)
            uname = creds[1]
            passw = creds[2]
            service = creds[3]
            if service == "ggl":
                self.lg.google(uname, passw)
            elif service == "fb":
                self.lg.facebook(uname, passw)
            else:
                print("Invalid Service!!!")
        else:
            print("User information for this ID not found in the Database")
            #main()

    def add_pass(self):
        while True:
            try:
                passw1 = input('Enter Master Password: ')
                passw2 = input('Re-Enter Master Password ')
                if passw1 == passw2:
                    hashed_pass = SHA256.new(passw1.encode('utf-8')).digest()
                    self.db.save_pass(hashed_pass)
                    break
                else:
                    print("The Password's didn't match")
                    continue
            except:
                print("Error!!!")
                continue

    def update_pass(self):
        while True:
            try:
                cpassw = input('Enter Current Password: ')
                retcpass = self.db.retrieve_pass()
                if cpassw == retcpass:
                    passw1 = input('Enter New Master Password: ')
                    passw2 = input('Re-Enter New Master Password ')
                    if passw1 == passw2:
                        hashed_pass = SHA256.new(passw1.encode('utf-8')).digest()
                        self.db.update_pass(hashed_pass)
                        break
                    else:
                        print("The Password's didn't match")
                        continue
                else:
                    print("The current password didn't match!!! ")
                    continue
            except:
                print("Error!!!")
                continue

    def remove_pass(self):
        while True:
            cpassw = input('Enter Current Password: ')
            retcpass = self.db.retrieve_pass()
            if cpassw == retcpass:
                self.db.remove_pass()
                break
            else:
                print("Please Enter the correct current password!!!")
                continue

    def check_pass(self):
        return self.db.retrieve_pass()






bf = Helper()
checker = bf.check_pass()
if checker is None:
    bf.add_pass()
else:
    print("Welcome")

# class security:
#     # def Encrypt(self, info):
#     def __init__(self):




# def #main():
#     bf = Helper()
#     db = Db_methods()
#     check = db.retrieve_pass()
#     if check is not None:
#         bf.add_pass()
#
#
#         sdict_select = int()
#         sdict_res = str()
#
#         print("""
#             --> Choice of Options <--
#
#             1 -> Display Accounts
#             2 -> Add User Information
#             3 -> Update User Information
#             4 -> Delete User Information
#             5 -> Login with Credentials
#
#             """)
#
#         sdict = {
#             1: bf.display,
#             2: bf.add,
#             3: bf.update,
#             4: bf.delete,
#             5: bf.login
#         }
#
#         while True:
#
#             try:
#                 sdict_select = int(input("Enter choice of action: "))
#                 sdict_res = sdict.get(sdict_select, False)()
#                 break
#
#             except:
#                 print("Invalid Selection!!! ")
#                 continue
#     else:
#         print("No Master Password is set. Please set a Master Password!!! ")
#         bf.add_pass()
#
#
# if __name__ == '__main__':
#     while True:
#         try:
#             #main()
#         except KeyboardInterrupt:
#             print('Process is killed by keyboard interrupt')
#             time.sleep(5)
#             sys.exit(0)







#bf = Helper()

# TEST RUN FOR INDIVIDUAL DATABASE FUNCTIONS #
# db.save('whatever u', 'whatever p', 'ggl') # WORKS FINE #
# print(db.read_all()) # WORKS FINE #
# print(db.read_one(1)) # WORKS FINE #
# db.update('what', 'what', 'fb', 1) # WORKS FINE #
# db.remove(3) # WORKS FINE #

# TEST RUN FOR INDIVIDUAL Helper FUNCTIONS #
# bf.add() # WORKS FINE AFTER MODIFICATION #
# bf.update() # WORKS FINE #
# bf.login() # WORKS FINE #
# bf.delete() # WORKS FINE #
# bf.display() # WORKS FINE #
# bf.add_pass()
# bf = Helper() Works Fine


# list_of_id = listall.keys()
# a = bf.check_id(2, list_of_id)
# print(a)