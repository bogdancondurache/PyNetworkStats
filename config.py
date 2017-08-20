"""
This module is used for general configurations of the project, like STMP and SQL data
and it is also used for defining general exceptions for SSH, DB and SMTP
"""

import paramiko

from smtplib import SMTP, SMTPException, SMTPConnectError, SMTPHeloError, SMTPAuthenticationError
from sqlite3 import connect, OperationalError, Error, DatabaseError
from socket import timeout

# Lists of specific exceptions
ssh_auth_exceptions = (paramiko.ssh_exception.AuthenticationException,
                       paramiko.ssh_exception.BadAuthenticationType)

ssh_conn_exceptions = (paramiko.ssh_exception.BadHostKeyException,
                       paramiko.ssh_exception.ChannelException,
                       paramiko.ssh_exception.NoValidConnectionsError,
                       paramiko.ssh_exception.SSHException)

db_exceptions = (OperationalError, Error, DatabaseError)
smtp_exceptions = (SMTPException, SMTPConnectError,
                   timeout, SMTPHeloError)

# Add here SMTP host, port and authentication
SMTP_SERVER = ''
SMTP_PORT = 587
SMTP_EMAIL = ''
SMTP_PASS = ''

# If the database is not created yet, it will be created with this name
# if you already have a database with the proper structure, please put here the file name with extension
DATABASE_NAME = 'demo.sqlite'


def config_smtp():
    """
    This method attempts to create a SMTP object
    In case of failure it will exit
    :return: SMTP Object
    """
    try:
        smtpObj = SMTP(SMTP_SERVER, SMTP_PORT)
        smtpObj.ehlo_or_helo_if_needed()
        smtpObj.starttls()
        smtpObj.login(SMTP_EMAIL, SMTP_PASS)
        return smtpObj
    except smtp_exceptions:
        print('Can not connect to the SMTP server. Aborting...')
        # exit()
    except SMTPAuthenticationError:
        print('Wrong SMTP authentication details. Aborting...')
        # exit()
    finally:
        return None

def config_db():
    """
    This method attempts to connect to the database DATABASE_NAME
    If it does not exist, it will create one
    :return: tuple with sqlite3 connection and cursor
    """
    try:
        connection = connect(DATABASE_NAME)
        cursor = connection.cursor()
        return (connection, cursor)
    except db_exceptions:
        print('Can not connect to the database. Aborting...')
        exit()


def config_ssh():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    return ssh
