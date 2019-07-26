import sqlite3
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from selenium import webdriver
import sys
import os
import time
from threading import Thread

listall = {}
id = []
name = []
global _session
_session = False

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

        self.conn = sqlite3.connect('db')
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS vector
                (
                    ID INTEGER PRIMARY KEY,
                    IV NONE
                )
                """)
        self.conn.commit()

    def save(self, uname, passw, service):

        try:
            self.c.execute("INSERT INTO userinfo (uname, passw, service) VALUES (?, ?, ?)",
                           (uname, passw, service))
            self.conn.commit()
            print("Information for " + uname + " Saved to Database successfully")
            main()
        except:
            "Couldn't save to Database!!!"
            main()

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
            main()
        except:
            "Couldn't Update Database!!!"
            main()

    def remove(self, id):
        try:
            self.c.execute("DELETE FROM userinfo WHERE ID = ?", [id])
            self.conn.commit()
            print("Credentials successfully removed")
            main()
        except:
            print("Couldn't delete information from Database!!!")
            main()

    def save_pass(self, master_pass):
        id = 1
        try:
            self.c.execute("INSERT INTO secret (id, master_pass) VALUES (?, ?)", (id, master_pass))
            self.conn.commit()
            print("Master Password Successfully being saved!!! ")
            main()
        except:
            print("Couldn't save to Database!!!")
            main()


    def update_pass(self, master_pass):
        id = 1
        try:
            self.c.execute("UPDATE secret SET passw=? WHERE ID=?", (master_pass, id))
            self.conn.commit()
            print("Password successfully updated!!! ")
            main()
        except:
            print("Couldn't update to Database")
            main()

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
            main()
        except:
            print("Couldn't remove password from Database!!!")
            main()

    def save_vector(self, IV):
        id = 1
        try:
            self.c.execute("INSERT INTO vector (ID, IV) VALUES (?, ?)", (id, IV))
            self.conn.commit()
            print("IV saved to database")
        except sqlite3.Error as e:
            print(e)
            print("Couldn't write vector to DB")

    def update_vector(self, IV):
        id = 1
        try:
            self.c.execute("UPDATE vector SET IV=? WHERE ID=?", (IV, id))
            self.conn.commit()
        except:
            print("Couldn't update vector to DB")

    def retrieve_vector(self):
        id = 1
        try:
            self.c.execute("SELECT IV FROM vector WHERE ID = ?", [id])
            return self.c.fetchone()
        except sqlite3.Error as e:
            print(e)

    def remove_vector(self):
        id = 1
        try:
            self.c.execute("DELETE FROM vector WHERE ID = ?", [id])
            self.conn.commit()
        except:
            print("Couldn't remove vector from Database!!!")


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
        driver.find_element_by_id('login_form').submit()
        driver.close()
        main()


class Helper:
    listall = {}
    list_of_id = []

    def __init__(self):
        listall.clear()
        self.db = Db_methods()
        self.lg = Login()
        self.sec = Security()
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
                enc_pass = self.sec.Encrypt(passw, self.check_pass(), self.IV())
                self.db.save(uname, enc_pass, service)
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
                    enc_pass = self.sec.Encrypt(passw, self.check_pass(), self.IV())
                    self.db.update(uname, enc_pass, service, select)
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
                print(select)
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
            dec_pass = self.sec.Decrypt(passw, self.check_pass(), self.IV())
            service = creds[3]
            if service == "ggl":
                self.lg.google(uname, dec_pass)
            elif service == "fb":
                self.lg.facebook(uname, dec_pass)
            else:
                print("Invalid Service!!!")
        else:
            print("User information for this ID not found in the Database")
            main()

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
            except Exception as e:
                print(e)

    def update_pass(self):
        while True:
            try:
                hash_obj = SHA256.new()
                cpassw = input('Enter Current Password: ')
                hashed_cpassw = hash_obj.update(cpassw.encode('utf-8')).digest
                retcpass = self.db.retrieve_pass()
                if hashed_cpassw == retcpass:
                    passw1 = input('Enter New Master Password: ')
                    passw2 = input('Re-Enter New Master Password ')
                    if passw1 == passw2:
                        hashed_pass = hash_obj.update(passw1.encode('utf-8')).digest()
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
            hash_obj = SHA256.new()
            cpassw = input('Enter Current Password: ')
            hashed_cpassw = hash_obj.update(cpassw.encode('utf-8')).digest()
            retcpass = self.db.retrieve_pass()
            if hashed_cpassw == retcpass:
                self.db.remove_pass()
                break
            else:
                print("Please Enter the correct current password!!!")
                continue

    def check_pass(self):
        try:
            master_pass = self.db.retrieve_pass()[0]
            return master_pass
        except:
            return None

    def make_IV(self):
        IV = self.sec.init_Vector()
        self.save_iv(IV)

    def save_iv(self, iv):
        self.db.save_vector(iv)

    def IV(self):
        try:
            IV = self.db.retrieve_vector()[0]
            return IV
        except:
            return False

    def update_iv(self):
        iv = self.sec.init_Vector()
        self.db.update_vector(iv)

    def del_iv(self):
        self.db.remove_vector()

    def this_login(self):
        userpass = input("Enter Login Password: ")
        return userpass

    def make_session(self, user_pass):
        global _session
        self.user_pass = user_pass
        userhash = SHA256.new(self.user_pass.encode('utf-8')).digest()
        stored_pass = self.check_pass()
        if userhash == stored_pass:
            _session = True
            return True
        else:
            return False

    def check_session(self):
        global _session
        if _session is True:
            return True
        else:
            return False

class Security:

    global BLOCK_SIZE

    def init_Vector(self):
        global BLOCK_SIZE
        BLOCK_SIZE = 16
        IV = Random.new().read(BLOCK_SIZE)
        return IV

    def Encrypt(self, passw, KEY, IV):
        BLOCK_SIZE = 16
        self.passw = passw
        PAD = "{"
        cipher = AES.new(KEY, AES.MODE_CBC, IV=IV)
        padding = lambda msg: msg + (BLOCK_SIZE - len(msg) % BLOCK_SIZE) * PAD
        return cipher.encrypt(padding(self.passw).encode('utf-8'))

    def Decrypt(self, passw, KEY, IV):
        self.passw = passw
        PAD = "{"
        decipher = AES.new(KEY, AES.MODE_CBC, IV=IV)
        plaintext = decipher.decrypt(self.passw).decode('utf-8')
        pad_index = plaintext.find(PAD)
        return plaintext[:pad_index]


def main():

    sdict_select = int()
    sdict_res = str()
    bf = Helper()
    db = Db_methods()
    check = bf.check_pass()
    IV = bf.IV()
    if IV is False:
        bf.make_IV()
    else:
        IV = bf.IV()
        print(IV)

    if check is None:
        print("No Master Password is set. Please set a Master Password!!! ")
        bf.add_pass()
    else:
        while True:
            if bf.check_session() is False:
                while True:
                    login = bf.this_login()
                    if bf.make_session(login) is True:
                        break
                    else:
                        print("Wrong Password. Check and try again!!!")
                        continue

            else:

                print("""
                    --> Choice of Options <--

                    1 -> Display Accounts
                    2 -> Add User Information
                    3 -> Update User Information
                    4 -> Delete User Information
                    5 -> Login with Credentials

                    """)

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
                        print("Invalid Selection!!! ")
                        continue


def kill_session():
    # while True:
    #     print("started")
    #     time.sleep(30)
    #     global _session
    #     _session = False
    #     print("Session has expired. Please Login Again!!! ")
    a = 1


if __name__ == '__main__':

    main_thread = Thread(target=main)
    main_thread.start()
    s_kill = Thread(target=kill_session, daemon=True)
    s_kill.start()
    main_thread.join()
    s_kill.join()

# bf = Helper()
# bf.make_IV()
# print(bf.IV())

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