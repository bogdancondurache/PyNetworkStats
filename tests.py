from helpers import parse_response, save_to_database
from base64 import b64encode
from Crypto.Cipher import AES


def test_parse_response():
    """
    Function to test decryption and data parsing
    """

    encrypter = AES.new('32byte SecretKey used forencrypt',
                        AES.MODE_CFB, 'IVfor encryption')
    data = b64encode(encrypter.encrypt(b'test'))
    data = 'b"' + str(data) + '\\n"'
    response = parse_response(data)
    assert(response[0] == 'test')


def test_database_save(dbConn, cursor):
    """
    Function to test the save_to_database() functionality
    Dummy data added to the database and removed after
    """

    query = 'INSERT INTO systems (ip, memory_usage, cpu_usage, uptime) '
    query += 'VALUES (?, ?, ?, ?)'
    insertValues = ['256.256.256.256', 23.5, 11.1, 123.12]
    save_to_database(query, insertValues, cursor)
    query = "SELECT ip, memory_usage, cpu_usage, uptime FROM systems "
    query += "WHERE ip = '256.256.256.256'"
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.execute("DELETE FROM systems WHERE ip = '256.256.256.256'")
    dbConn.commit()
    assert result == ('256.256.256.256', 23.5, 11.1, 123.12)


def run_tests(dbConn, cursor):
    """
    Function used to call all the other tests
    :param dbConn: sqlite3 connection
    :param cursor: current database cursor
    :return: 
    """