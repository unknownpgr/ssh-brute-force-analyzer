import sqlite3

con = sqlite3.connect('out/btmp-log.db')
cur = con.cursor()

cur.execute(
    '''
        SELECT
            datetime(MIN(timestamp), 'unixepoch', 'localtime'),
            datetime(MAX(timestamp), 'unixepoch', 'localtime'),
            (MAX(timestamp) - MIN(timestamp))/(3600*24)
        FROM btmp
    ''')
print('Period:')
print(cur.fetchone())
print()

cur.execute('SELECT COUNT(*) FROM btmp')
print('Total collected log count:')
print(cur.fetchone()[0])
print()

cur.execute(
    'SELECT name, COUNT(name) FROM btmp GROUP BY name ORDER BY COUNT(name) DESC LIMIT 10')
print('Top 10 username:')
print('\n'.join(map(str, cur.fetchall())))
print()

cur.execute(
    'SELECT ip, COUNT(ip) FROM btmp GROUP BY ip ORDER BY COUNT(ip) DESC LIMIT 10')
print('IPs:')
print('\n'.join(map(str, cur.fetchall())))
print()
