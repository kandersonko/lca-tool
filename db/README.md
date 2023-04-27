# db Folder

Files pertaining only to the Database.<br />

## Individual file information.

schema.sql: Contains the MySQL code to read appon initial startup or reboot of the server and database. <br />

## Setup
Create a `password.txt` file and put a password inside. This file is needed for the MySQL database. After creating the `password.txt` file, delete the MySQL docker volume and restart the containers to program the password change.
