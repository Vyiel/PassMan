# PassMan
A Simple, Local, Single user Password Manager based on Python 3. Windows only.

This is a local password manager that you can keep at your home, upload the database somewhere in the cloud, All you have to do is remember the password,
or even write the password down somewhere safe. This doesn't have any internet permissions, so it's objectively secure.

The methods of usage are pretty simple, Upon first initialization, you have to provide a master password. And that password will be used to
encrypt and decrypt your data, in this case, the passwords. 
Then it You can choose what you want to do whether to add an entry, update or remove one or Login using Clipboard OR Chrome developer API.
For the auto Login (BETA, CHROME and Google AND/OR Facebook only) to work, you have to download the latest chromedriver and put it in the default windows root directory.
Else, you can use the clipboard way to login, where you have to just type in the username and simply paste the password copied to your clipboard. The Login page will automatically be opened on your chosen preffered browser.
To update the master password, you have to run the command 'python PwMan up'. Thus the password would be updated. Also no password recovery has been implemented yet.
If you forget the password, the database is useless. 

Packages you need to Run this application. For all the packages, Just run the following command -> 'pip install package-name'
Following packages:
1) selenium,
2) pycryptodome,
3) clipboard.

Rest of the packages come with Python.

That's it ...

Technical Aspects regarding security: The program uses RFC Complient security reference 2898. Which means Instead of simply hashing the password, Password Based Key Derivation function Version 2 has been used with multiple rounds with the Pseudo random function SHA1. One part of the derived key has been used as a varification during login, and the other half as the Encryption/Decryption key. The Encryption that is used 32 bytes AES with a Cipher Block Chain mode. 
