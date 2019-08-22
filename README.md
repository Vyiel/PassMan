# PassMan
A Simple, Local, Single user Password Manager based on Python. Windows only.

This is a local password manager that you can keep at your home, upload the database somewhere in the cloud, All you have to do is remember the password,
or even write the password down somewhere safe. This doesn't have any internet permissions, so it's objectively secure.

The methods of usage are pretty simple, Upon first initialization, you have to provide a master password. And that password will be used to
encrypt and decrypt your data, in this case, the passwords. 
Then it You can choose what you want to do whether to add an entry, update or remove one or Login using Clipboard OR Chrome developer API.
For the auto Login (BETA, CHROME and Google AND/OR Facebook only) to work, you have to download the latest chromedriver and put it in the default windows root directory.
Else, you can use the clipboard way to login, where you have to just type in the username and simply paste the password copied to your clipboard. The Login page will automatically be opened on your chosen preffered browser.
To update the master password, you have to run the command 'python PwMan up'. Thus the password would be updated. Also no password recovery has been implemented yet.
If you forget the password, the database is useless. 

That's it ...
