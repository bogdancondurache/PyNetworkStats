import psutil
from time import time
from Crypto.Cipher import AES
from base64 import b64encode

memory = str(psutil.virtual_memory().percent)
cpu = str(psutil.cpu_percent())
uptime = str(time() - psutil.boot_time())

result = "\n" .join([memory, cpu, uptime])

if psutil.WINDOWS:
    import win32evtlog  # requires pywin32 pre-installed
    server = 'localhost'
    logtype = 'Security'
    hand = win32evtlog.OpenEventLog(server, logtype)
    backwards_read = win32evtlog.EVENTLOG_BACKWARDS_READ
    sequential_read = win32evtlog.EVENTLOG_SEQUENTIAL_READ
    flags = backwards_read | sequential_read
    total = win32evtlog.GetNumberOfEventLogRecords(hand)
    events = win32evtlog.ReadEventLog(hand, flags, 0)
    if events:
        formatedEvents = ''
        for event in events:
            formatedEvents += 'Event Category: ' + str(event.EventCategory)
            formatedEvents += '\nTime Generated: ' + str(event.TimeGenerated)
            formatedEvents += '\nSource Name: ' + event.SourceName
            formatedEvents += '\nEvent ID: ' + str(event.EventID)
            formatedEvents += '\nEvent Type:' + str(event.EventType) + '\n'
        result += "\n" + str(formatedEvents)

crypter = AES.new('32byte SecretKey used forencrypt',
                  AES.MODE_CFB, 'IVfor encryption')
ciphertext = crypter.encrypt(result)
ciphertext = b64encode(ciphertext)
print(ciphertext)
