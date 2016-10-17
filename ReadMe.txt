1. Prequisites
    .  smtplib
    .  python 2.7
    .  pywin32
    .  paramiko 1.8.0
    .  pycrypto-2.6.1
    .  psutils
    .  Diffiehellman 0.13.3
    .  mysql-connector-python-2.1.4-py2.7-winx64.msi
    .  mysql
2. Please configure the SMTP, DB variables in Properties.py file
3. Connect to MySql instance and run CreateTables.sql
4. Change directory to root directory of this project and execute the application using following command in CLI.
	python -m Server.ServerMain 
5. Requirements not Covered:
    Windows security event logs (in case of windows OS).