'''
Parse btmp file and write it on sqlite3 database file.
'''

import sqlite3
import time
import os
import datetime

def get_btmp():
    '''
    Return list of btmp entities
    '''
    stream = os.popen('lastb --time-format iso')
    output = stream.readlines()
    result = []
    for line in output:
        parts = line.strip().split(' ')
        parts = list(filter(lambda x: len(x)>0, parts))
        if len(parts) != 7:
            continue
        parts = parts[:4]
        timestmap = int(datetime.datetime.fromisoformat(parts[3]).timestamp())
        parts[3] = timestmap
        result.append(parts)
    return result

con = sqlite3.connect('/out/btmp-log.db')
cur = con.cursor()

try:
    cur.execute('CREATE TABLE btmp (name text,shell text, ip text, timestamp int)')
    cur.execute('CREATE UNIQUE INDEX btmp_index ON btmp (name, ip, timestamp)')
    con.commit()
    print('Table created.')
except:
    print("Skip table creation")

while True:
    entries = get_btmp()
    cur.executemany(
        'INSERT OR IGNORE INTO btmp VALUES(?,?,?,?)', entries)
    con.commit()
    cur.execute('SELECT COUNT(*) FROM btmp')
    count = cur.fetchall()[0][0]
    print('Number of entities:', count)
    # Run for every 10 min
    time.sleep(10 * 60)
