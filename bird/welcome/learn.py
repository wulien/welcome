# import sqlite3

# connect = sqlite3.connect('d:/sqlite3db.db3')
# cur = connect.cursor()
import logging

logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')