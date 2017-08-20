import xml.etree.ElementTree as ET
from os.path import isfile
from config import (
    DATABASE_NAME,
    config_ssh, config_smtp, config_db,
    ssh_auth_exceptions, ssh_conn_exceptions
)
from helpers import parse_response, is_win, save_to_database, email_alert
from database import main as create_database
# from tests import run_tests


def upload_and_run(ssh, isWin, pasw):
    """
    This function will use SFTP from the paramiko module to upload the client
    After that the client will be executed on the remote machine
    Path to upload to and command to execute are relative to the remote
    machine's operating system
    After that, parse_response() will be called to properly parse the response
    """

    sftp = ssh.open_sftp()
    path = '/tmp/client.py'
    command = 'sudo python3 /tmp/client.py'
    if isWin:
        path = 'C:\\Windows\\Temp\\client.py'
        command = 'python.exe C:\\Windows\\Temp\\client.py'
    sftp.put('client.py', path)
    sftp.close()

    stdin, stdout, stderr = ssh.exec_command(command)
    if not isWin:
        stdin.write(pasw + '\n')
        stdin.flush()
    stdin.close()
    return parse_response(stdout.read())


def parse_xml():
    """
    Main program function, will parse the XML file
    and call all the needed functions for each one
    """

    try:
        tree = ET.parse('config.xml')
    except ET.ParseError:
        print('Error at parsing the config.xml file. Please check the file')
        exit()

    root = tree.getroot()

    for child in root:
        user = child.attrib['username']
        host = child.attrib['ip']
        pasw = child.attrib['password']
        mail = child.attrib['mail']

        ssh = config_ssh()

        try:
            ssh.connect(host, username=user, password=pasw)
        except ssh_auth_exceptions:
            print('SSH authentication problem on', host)
            continue
        except ssh_conn_exceptions:
            print('Connection problem to host', host)
            continue

        isWin = is_win(ssh)

        data = upload_and_run(ssh, isWin, pasw)

        insertValues = [host]
        for i in range(0, 3):
            insertValues.append(float(data[i]))

        query = 'INSERT INTO systems (ip, memory_usage, cpu_usage, uptime) '
        query += 'VALUES (?, ?, ?, ?)'

        if isWin:
            query = 'INSERT INTO systems'
            query += '(ip, memory_usage, cpu_usage, uptime, events)'
            query += 'VALUES (?, ?, ?, ?, ?)'

            events = ''
            for i in range(3, len(data)):
                events += data[i] + ', '
            insertValues.append(events)

        save_to_database(query, insertValues, cursor)

        for alert in child:
            email_alert(host, alert, data, smtpObj, mail)

        ssh.close()

# SMTP and database connections
smtpObj = config_smtp()
# Database should already be created using database.py
if not isfile(DATABASE_NAME):
    create_database()
dbConn, cursor = config_db()

# Run tests
# run_tests(dbConn, cursor)

# Parsing the XML and program main execution
parse_xml()

# Closing DB connection
dbConn.commit()
dbConn.close()

print('Everything finished successfully')
