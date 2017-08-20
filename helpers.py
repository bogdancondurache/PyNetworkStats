from Crypto.Cipher import AES
from base64 import b64decode
from config import db_exceptions


def is_win(ssh):
    """
    Function used to determine whether remote system is running
    Windows or Unix; Hack, echo on Windows will return the quotes from string
    """

    stdin, stdout, stderr = ssh.exec_command('echo "test"')
    stdin.close()
    response = str(stdout.read())
    returnedQuotation = response.find('"')
    if returnedQuotation == -1:
        return False
    else:
        return True


def send_email(smtp, email, alert, host):
    """
    Function to send the email alert
    Receives all the needed data, including host IP and receiver email
    """

    sender = 'bcondurache@gmail.com'
    receivers = [email]
    message = '''Subject: Alert on network computer

    System with IP: %s triggered the %s alarm''' % (host, alert)
    smtp.sendmail(sender, receivers, message)


def email_alert(host, alert, data, smtp, email):
    """
    Function used to determine whether an email alert will be triggered or not
    If yes, it will send the needed data and the alert type and call the
    send_email() function
    """

    alertType = alert.attrib['type']
    alertValue = alert.attrib['limit'][:-1]
    toCompareDict = {'memory': 0, 'cpu': 1, 'uptime': 2}
    toCompare = toCompareDict[alertType]
    if data[toCompare] >= alertValue:
        send_email(smtp, email, alertType, host)


def save_to_database(query, insertValues, cursor):
    try:
        cursor.execute(query, insertValues)
    except db_exceptions:
        print('Database error. Aborting...')
        print('Try to run the database.py script')
        exit()


def parse_response(response):
    """
    Function used to remove the extra chars from the respone (bytes type)
    after it was converted to string, Base64 decode it and decrypt it
    The function will return an array, the first 3 elements will be
    memory, cpu usage and uptime. All elements after that will have the
    Events log system stored
    """

    response = str(response)[4:-4]
    response = bytes(response, 'UTF-8')
    decrypter = AES.new('32byte SecretKey used forencrypt',
                        AES.MODE_CFB, 'IVfor encryption')
    data = decrypter.decrypt(b64decode(response))
    data = str(data.decode('unicode_escape')).splitlines()
    return data
