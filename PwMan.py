import sqlite3
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto import Random
from binascii import unhexlify
from selenium import webdriver
import sys
import os
import time
from threading import Thread
from clipboard import copy
from webbrowser import open as browser_open


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

        self.conn = sqlite3.connect('db')
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS vector
                (
                    ID INTEGER PRIMARY KEY,
                    IV NONE
                )
                """)
        self.conn.commit()

        self.conn = sqlite3.connect('db')
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS salt
                        (
                            ID INTEGER PRIMARY KEY,
                            salt NONE
                        )
                        """)
        self.conn.commit()

    def save(self, uname, passw, service):

        try:
            self.c.execute("INSERT INTO userinfo (uname, passw, service) VALUES (?, ?, ?)",
                           (uname, passw, service))
            self.conn.commit()
            print("Information for " + uname + " Saved to Database successfully")
        except:
            "Couldn't save to Database!!!"
            self.conn.rollback()


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
            self.conn.commit()
        except:
            "Couldn't Update Database!!!"
            self.conn.rollback()

    def remove(self, id):
        try:
            self.c.execute("DELETE FROM userinfo WHERE ID = ?", [id])
            self.conn.commit()
            print("Credentials successfully removed")
        except:
            print("Couldn't delete information from Database!!!")
            self.conn.rollback()

    def save_pass(self, master_pass):
        id = 1
        try:
            self.c.execute("INSERT INTO secret (id, master_pass) VALUES (?, ?)", (id, master_pass))
            self.conn.commit()
            print("Master Password Successfully being saved!!! ")
        except:
            print("Couldn't save to Database!!!")
            self.conn.rollback()


    def update_pass(self, master_pass):
        id = 1
        try:
            self.c.execute("UPDATE secret SET master_pass=? WHERE ID=?", (master_pass, id))
            self.conn.commit()
            print("Master Password successfully updated!!! ")

        except:
            print("Couldn't update password to Database")
            self.conn.rollback()



    def retrieve_pass(self):
        id = 1
        self.c.execute("SELECT master_pass FROM secret WHERE ID = ?", [id])
        return self.c.fetchone()


    def remove_pass(self):
        id = 1
        try:
            self.c.execute("DELETE FROM secret WHERE ID = ?", [id])
            print("Password successfully removed")
            self.conn.commit()
        except:
            print("Couldn't remove password from Database!!!")
            self.conn.rollback()

    def save_vector(self, IV):
        id = 1
        try:
            self.c.execute("INSERT INTO vector (ID, IV) VALUES (?, ?)", (id, IV))
            self.conn.commit()
        except:
            print("Couldn't write vector to DB")
            self.conn.rollback()

    def update_vector(self, IV):
        id = 1
        try:
            self.c.execute("UPDATE vector SET IV=? WHERE ID=?", (IV, id))
            self.conn.commit()
        except:
            print("Couldn't update vector to DB")
            self.conn.rollback()

    def retrieve_vector(self):
        id = 1
        try:
            self.c.execute("SELECT IV FROM vector WHERE ID = ?", [id])
            return self.c.fetchone()
        except:
            print("Couldn't retrieve vector")

    def remove_vector(self):
        id = 1
        try:
            self.c.execute("DELETE FROM vector WHERE ID = ?", [id])
            self.conn.commit()
        except:
            print("Couldn't remove vector from Database!!!")
            self.conn.rollback()

    def save_salt(self, salt):
        id = 1
        try:
            self.c.execute("INSERT INTO salt (ID, salt) VALUES (?, ?)", (id, salt))
            self.conn.commit()
        except:
            print("Couldn't write salt to DB")
            self.conn.rollback()

    def update_salt(self, salt):
        id = 1
        try:
            self.c.execute("UPDATE salt SET salt=? WHERE ID=?", (salt, id))
            self.conn.commit()
        except:
            print("Couldn't update salt to DB")
            self.conn.rollback()

    def remove_salt(self):
        id = 1
        try:
            self.c.execute("DELETE FROM salt WHERE ID = ?", [id])
            self.conn.commit()
        except:
            print("Couldn't remove salt from Database!!!")
            self.conn.rollback()

    def retrieve_salt(self):
        id = 1
        try:
            self.c.execute("SELECT salt FROM salt WHERE ID = ?", [id])
            return self.c.fetchone()
        except:
            print("Couldn't retrieve salt")


class Login:

    windows_location = str(os.environ['windir'])
    rootdir = windows_location[:2]
    driver_loc = rootdir+"\chromedriver"

    def google(self, uname, passw):
        self.uname = uname
        self.passw = passw
        try:
            driver = webdriver.Chrome(executable_path=self.driver_loc)

        except Exception:
            print("""Probably The chrome driver is not matched with your current Google Chrome version.
            Please update chrome to the latest version, and download and save the latest
            stable version of chromedriver on to the root of your Windows Installation!!! """)
            main()
        try:
            target = 'https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin'
            driver.get(target)

            driver.find_element_by_id("identifierId").send_keys(self.uname)
            driver.find_element_by_class_name('CwaK9').click()
            time.sleep(2)
            driver.find_element_by_name("password").send_keys(passw)
            driver.find_element_by_class_name("CwaK9").click()
            main()
        except:
            print("Error during login. Try again!!! ")
            main()


    def facebook(self, uname, passw):
        self.uname = uname
        self.passw = passw
        driver = webdriver.Chrome(self.driver_loc)
        target = 'https://www.facebook.com'
        driver.get(target)
        time.sleep(2)
        driver.find_element_by_id('email').send_keys(self.uname)
        driver.find_element_by_id('pass').send_keys(self.passw)
        driver.find_element_by_id('login_form').submit()
        main()

class NoLogin():

    def clip(self, uname, passw, service):
        self.uname = uname
        self.passw = passw
        self.service = service

        print("The User Name or Email is: "+str(self.uname))
        print("""
        Wait for page to load, Type in the username. 
        Password is copied in the clipboard. Just paste within the password box!!!
        """)
        time.sleep(3)
        browser_open(service)
        copy(self.passw)
        time.sleep(1)
        program()


class Helper:
    listall = {}
    list_of_id = []
    global user_password
    global _session

    def __init__(self):
        listall.clear()
        self.db = Db_methods()
        self.lg = Login()
        self.sec = Security()
        self.clipboard = NoLogin()


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
            user_name = listall[items][0]
            try:
                service_name = str(listall[items][1]).split('.')[1]
            except:
                service_name = "Unknown"
            print(str(items) + "     " + "User Name: " + user_name + "     " + "Service: " + service_name)
        program()

    @staticmethod
    def display2():

        print("--> All Accounts <--")

        for items in listall:
            user_name = listall[items][0]
            try:
                service_name = str(listall[items][1]).split('.')[1]
            except:
                service_name = "Unknown"
            print(str(items) + "     " + "User Name: " + user_name + "     " + "Service: " + service_name)

    def check_pass(self):
        try:
            return self.db.retrieve_pass()[0]
        except:
            return None

    def add(self):
        global user_password
        while True:
            uname = input('Enter Username: ')
            passw = input('Enter Password: ')
            service = input('Enter Service -> Copy and Paste The exact login page URL: ')
            enc_pass = self.sec.Encrypt(passw, self.key_derivation(user_password, self.salt())[1], self.IV())
            self.db.save(uname, enc_pass, service)
            program()
            break

    def update(self):
        self.display2()

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
                service = input("Update Service -> Copy and Paste The exact login page URL: ")
                enc_pass = self.sec.Encrypt(passw, self.key_derivation(user_password, self.salt())[1], self.IV())
                self.db.update(uname, enc_pass, service, select)
                program()
                break
        else:
            print("User information for this ID not found in the Database")
            program()

    def delete(self):
        print("--> Remove Accounts <--")
        self.display2()

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
            program()
        else:
            print("User information for this ID not found in the Database")
            program()

    def login(self):
        print("--> Login <--")
        self.display2()

        while True:
            try:
                select = int(input("Enter choice of ID from before the User Names to Login: "))
                break
            except:
                print("selection type for Login not integer!!! ")
                continue

        list_of_id = listall.keys()
        opt = self.check_id(select, list_of_id)
        if opt is True:
            creds = self.db.read_one(select)
            uname = creds[1]
            passw = creds[2]
            dec_pass = self.sec.Decrypt(passw, self.key_derivation(user_password, self.salt())[1], self.IV())
            service = creds[3]
            while True:
                if service.find("google") > 0:
                    self.lg.google(uname, dec_pass)
                    break
                elif service.find("facebook") > 0:
                    self.lg.facebook(uname, dec_pass)
                    break
                else:
                    print("Invalid Service Credentials !!! Login (BETA) only works for Google OR/AND Facebook")
                    program()
        else:
            print("User information for this ID not found in the Database")
            program()

    def clip(self):
        print("--> Clipboard Login <--")
        self.display2()

        while True:
            try:
                select = int(input("Enter choice of ID from before the User Names for Clipboard: "))
                break
            except:
                print("selection type for Clipboard not integer!!! ")
                continue

        list_of_id = listall.keys()
        opt = self.check_id(select, list_of_id)
        if opt is True:
            creds = self.db.read_one(select)
            uname = creds[1]
            passw = creds[2]
            dec_pass = self.sec.Decrypt(passw, self.key_derivation(user_password, self.salt())[1], self.IV())
            service = creds[3]
            self.clipboard.clip(uname, dec_pass, service)
        else:
            print("User information for this ID not found in the Database")
            program()

    def export(self):

        export = {}
        all = self.db.read_all()
        for i in all:
            id = i[0]
            uname = i[1]
            passw = self.sec.Decrypt(i[2], self.key_derivation(user_password, self.salt())[1], self.IV())
            try:
                service = str(i[3]).split('.')[1]
            except:
                service = "Unknown"
            export[id] = [uname, passw, service]

        file = open("User information.txt", "w")
        file.write("Exported Username and Passwords")
        file.write("\n\n\n")
        for i in export.values():
            text = "User Name: " + i[0] + ", " + "Password: " + i[1] + ", " + "Service: " + i[2]
            file.write(text + '\n\n')
        file.close()
        program()


    def add_pass(self):
        while True:
            try:
                passw1 = input('Enter Master Password: ')
                passw2 = input('Re-Enter Master Password ')
                if passw1 == passw2:
                    salt = self.salt()
                    hashed_pass = self.key_derivation(passw=passw1, salt=salt)[0]
                    self.db.save_pass(hashed_pass)
                    program()
                    break
                else:
                    print("The Password's didn't match!!!")
                    continue
            except:
                print("Error adding Password!!!")
                program()

    def update_pass(self):
        while True:
            try:
                cpassw = input('Enter Current Password: ')
                hashed_cpassw = self.key_derivation(passw=cpassw, salt=self.salt())[0]
                retcpass = self.db.retrieve_pass()[0]
                if hashed_cpassw == retcpass:
                    current_enc_pass = cpassw
                    new_passw1 = input('Enter New Master Password: ')
                    new_passw2 = input('Re-Enter New Master Password ')
                    if new_passw1 == new_passw2:
                        new_enc_pass = new_passw1
                        self.change_key_for_all(old_pass=current_enc_pass, new_pass=new_enc_pass)
                        time.sleep(1)
                        os._exit(0)
                    else:
                        print("The Password's didn't match!!! ")
                        continue
                else:
                    print("The current password didn't match!!! ")
                    continue
            except:
                print("Error Updating Password!!! ")



    def remove_pass(self):
        while True:
            cpassw = input('Enter Current Password: ')
            hashed_cpassw = self.key_derivation(passw=cpassw, salt=self.salt())[0]
            retcpass = self.db.retrieve_pass()
            if hashed_cpassw == retcpass:
                self.db.remove_pass()
                main()
                break
            else:
                print("Please Enter the correct current password!!!")
                continue

    def change_key_for_all(self, old_pass, new_pass):

        old_salt = self.salt()
        old_hkey_key, old_enc_key = self.key_derivation(passw=old_pass, salt=old_salt)
        new_salt = self.sec.salt()
        new_hkey_key, new_enc_key = self.key_derivation(passw=new_pass, salt=new_salt)
        old_IV = self.IV()
        new_IV = self.sec.init_Vector()
        ids = []
        all_items = self.db.read_all()

        re_encrypted_ids = []
        error_stat_UPDATE = 0
        for all_ids in all_items:
            ids.append(all_ids[0])

        for i in ids:
            upass = self.db.read_one(i)[2]
            decrypt = self.sec.Decrypt(passw=upass, KEY=old_enc_key, IV=old_IV)
            re_encrypt = self.sec.Encrypt(passw=decrypt, KEY=new_enc_key, IV=new_IV)

            try:
                self.conn = sqlite3.connect('db')
                self.c = self.conn.cursor()
                self.c.execute("UPDATE userinfo SET passw=? WHERE ID = ?", (re_encrypt, i))
                self.conn.commit()
                re_encrypted_ids.append(i)
            except:
                self.conn.rollback()
                error_stat_UPDATE = 1
                break

        if error_stat_UPDATE == 0:
            self.db.update_pass(new_hkey_key)
            self.update_iv(new_IV)
            self.update_salt(new_salt)

        else:
            print("Error Updating Master Password. Rolling back changes!!! ")
            for j in re_encrypted_ids:
                re_upass = self.db.read_one(j)[2]
                re_decrypt = self.sec.Decrypt(passw=re_upass, KEY=new_enc_key, IV=new_IV)
                r_encrypt = self.sec.Encrypt(passw=re_decrypt, KEY=old_enc_key, IV=old_IV)
                try:
                    self.c.execute("UPDATE userinfo SET passw=? WHERE ID = ?", (r_encrypt, j))
                    self.conn.commit()
                except:
                    self.conn.rollback()

            self.db.update_pass(old_hkey_key)
            self.update_iv(old_IV)
            self.update_salt(old_salt)


    def key_derivation(self, passw, salt):
        global user_password
        dk = []
        hk = []
        hasher = PBKDF2(password=passw, count=5000, salt=salt, dkLen=64).hex()
        for i in range(64):
            hk.append(hasher[i])
        for j in range(64, 128):
            dk.append(hasher[j])

        hk = "".join(hk)
        dk = unhexlify("".join(dk))

        return (hk, dk)


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

    def update_iv(self, iv):
        self.db.update_vector(iv)

    def del_iv(self):
        self.db.remove_vector()


    def make_salt(self):
        salt = self.sec.salt()
        self.save_salt(salt)

    def save_salt(self, salt):
        self.db.save_salt(salt)

    def salt(self):
        try:
            salt = self.db.retrieve_salt()[0]
            return salt
        except:
            return False

    def update_salt(self, salt):
        self.db.update_salt(salt)

    def del_salt(self):
        self.db.remove_salt()

    def this_login(self):
        userpass = input("Enter Login Password: ")
        return userpass

    def make_session(self, user_pass):
        global user_password, _session
        salt = self.salt()
        userhash = self.key_derivation(passw=user_pass, salt=salt)[0]
        stored_pass = self.check_pass()
        if userhash == stored_pass:
            user_password = user_pass
            _session = True
            program()
        else:
            user_password = ""
            _session = ""
            print("Wrong Login Password. Check and Try again!!!")
            program()

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

    def salt(self):
        global BLOCK_SIZE
        BLOCK_SIZE = 16
        salt = Random.new().read(BLOCK_SIZE)
        return salt

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


def program():

    def false_select():
        print("Invalid Selection!!!")
        select()
        return False

    def quit():
        print("Thanks for using the program!!! ")
        time.sleep(1)
        os._exit(0)

    def select():
        sdict_select = int()
        sdict_select = ""
        sdict_res = str()
        print("""
                            --> Choice of Options <--

                            1 -> Display Accounts
                            2 -> Add User Information
                            3 -> Update User Information
                            4 -> Delete User Information
                            5 -> Login with Credentials (BETA)
                            6 -> Clipboard Login
                            7 -> Export all
                            8 -> Quit!!!

                            """)

        sdict = {
            1: bf.display,
            2: bf.add,
            3: bf.update,
            4: bf.delete,
            5: bf.login,
            6: bf.clip,
            7: bf.export,
            8: quit
        }

        while True:
            try:
                sdict_select = int(input("Enter choice of action: "))
                sdict.get(sdict_select, false_select)()
                break
            except:
                print("Invalid Selection!!!")
                select()

    bf = Helper()
    check = bf.check_pass()
    IV = bf.IV()
    if IV is False:
        bf.make_IV()

    salt = bf.salt()
    if salt is False:
        bf.make_salt()

    if len(sys.argv) > 1:
        if sys.argv[1] == "up":
            bf.update_pass()
            system = 1
        else:
            system = 0
    else:
        system = 0

    if system == 0:

        if check is None:
            print("No Master Password is set. Please set a Master Password!!! ")
            bf.add_pass()
        else:
            if bf.check_session() is False:
                login = bf.this_login()
                bf.make_session(login)
            else:
                select()


def auto_quit():
    print("Auto Quitting in 3 Minutes")
    time.sleep(60*3)
    os._exit(0)


def main():
    global _session
    _session = False
    main_thread = Thread(target=program, daemon=True)
    main_thread.start()
    s_kill = Thread(target=auto_quit(), daemon=True)
    s_kill.start()
    main_thread.join()
    s_kill.join()


if __name__ == '__main__':
    main()

