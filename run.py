# -*- coding: utf-8 -*-
#!/usr/bin/env python

__author__ = "Fedor Marchenko"
__copyright__ = "Copyright 2014, The PostJSONFromPostgreSQL Project"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Fedor Marchenko"
__email__ = "me@fmarchenko.ru"
__status__ = "Production"

import sys
import conf
import psycopg2
import json
import time, logging, datetime
import urllib2


dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime)  or isinstance(obj, datetime.date) else None

DATABASE = getattr(conf, 'DATABASE', None)
USER = getattr(conf, 'USER', None)
PASSWORD = getattr(conf, 'PASSWORD', None)
HOST = getattr(conf, 'HOST', None)
PORT = getattr(conf, 'PORT', None)
URL = getattr(conf, 'URL', None)
queries = getattr(conf, 'queries', None)
        

def main(args):
    start_script = time.time()
    conn = psycopg2.connect(database=DATABASE, user=USER, 
        password=PASSWORD, host=HOST, port=PORT)
    cur = conn.cursor()
    res = []
    
    for key, query in queries.items():
        start = time.time()
        cur.execute(query)
        res.append({key: cur.fetchall()})
        end = time.time()
        logging.info(u'Total time: %0.3f for %s' % ((end - start, query)))
        
    json_result = json.dumps(res, default=dthandler)

    request = urllib2.Request(URL, json_result, {'Content-Type': 'application/json'})
    f = urllib2.urlopen(request)
#    response = f.read()
#    f.close()

    logging.info(u'Total time script: %0.3f' % (time.time() - start_script))
    cur.close()
    conn.close()


if __name__ == '__main__':
    main(sys.argv[1:])