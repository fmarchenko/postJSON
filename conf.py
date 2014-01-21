DATABASE = None
USER = None
PASSWORD = None
HOST = None
PORT = None

URL = ''

SERVICE_TIMEOUT = 900000 #Pause between the execution of the main loop service in milliseconds

queries = {
	'Schedule': 'select * from schedule;',
	'Children': 'select * from child inner join child_coursetype on id=child_id;',
	'Coursetype': 'select * from coursetype;',
	'Family': 'select * from family;'
}

try:
    from conf_local import *
except: pass
