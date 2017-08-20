# PyNetworkStats

PyNetworkStats is a network based machine statistics collection system.
Add SSH credentials in the config.xml file.
When the main.py script gets executed the client script will be send to the remote servers and executed there.

The main script will save memory usage, CPU usage, total uptime and windows security event logs (in case of Windows OS)
in a database.
For security reasons, all data sent from the client script to the main one are encrypted (I am not sure about how
secure the key transmission is).

Also, there is the possibility to add custom alerts in config.xml for each client. So, when a certain value for the
monitored values is exceeded and email alert will be sent.



## DEPENDENCIES

1. pip

   Install pip from [https://pip.pypa.io/en/stable/installing/#installing-with-get-pip-py]

2. Installable via `pip install -r requirements.txt`

    1. psutil (only for client)
    2. pycrypto (both client and server)
    3. paramiko (only for server)

## CONFIG

All configurations are done in config.py and config.xml

Firstly the SMTP server has to be configured. Please put the SMTP host in
SMTP_SERVER, the port in SMTP_PORT and the authentication details in
SMTP_EMAIL and SMTP_PASS

Please complete a database name in DATABASE_NAME. The default value is
'demo.sqlite'

The config.xml contains a sample for how to add a client and set alerts for it.

## DATABASE

Run the database.py script after putting the name in DATABASE_NAME and the database
and table will be created or if database file not existing, database.py will be called by main.py

## ASSUMTIONS

The client will have Python 3 installed, which will be called using the "python3"
command. Also the client will have psutil installed. The client will have all the
dependencies installed. On the client side administration rights will be needed.
On Windows the user will need an Administrator account, on Linux it will need
sudo installed and to be in the sudoers file. All the SSH connections are done
using user/password, so no security key authentication possible.
