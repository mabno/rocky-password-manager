# Rocky Password Manager
Rocky Password Manager is a little project in Python 3 for practice. It's a console program in which you will be able save, update, read and delete your passwords (and username if you want) of all services on what you are registered. The data is saved in an encrypted database.
This program gives authentication option to protect your passwords of an unwanted reader.
## Features

 - Python3
 - SQLite3 (pysqlcipher3)
 - Encrypted authentication and database
 - Search passwords option
 - View details options (last update, created at, etc.)

### Configuration (Ubuntu)

 1. Clone repository

> git clone https://github.com/mabno/rocky-password-manager.git

2. The project has 2 importants files

> .keypath
> .user

3. No edit ***.user***, just edit ***.keypath*** with the path where you want save the ***.key*** file. The ***.key*** file will contain the cryptographic key for you authentication (must be secret) 

5. Install required modules
> sudo apt install sqlcipher libsqlcipher0 libsqlcipher-dev && pip3 install cryptography pysqlcipher3 termcolor

6. Run index.py

> python3 index.py

#### Additional info

 - .keypath is by default:

> ./.rpmkey

- Only tested in Ubuntu