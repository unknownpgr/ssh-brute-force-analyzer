import sqlite3

con = sqlite3.connect("out/btmp-log.db")
cur = con.cursor()


def indent(text):
    return "  {}".format(text)


cur.execute(
    """
        SELECT
            datetime(MIN(timestamp), 'unixepoch', 'localtime'),
            datetime(MAX(timestamp), 'unixepoch', 'localtime'),
            (MAX(timestamp) - MIN(timestamp))/(3600*24)
        FROM btmp
    """
)
print("BTMP crawling period:")
start, end, days = cur.fetchone()
print("  Start: {}".format(start))
print("  End: {}".format(end))
print("  Days: {}".format(days))
print()

cur.execute("SELECT COUNT(*) FROM btmp")
print("Total collected log count:")
print(indent(cur.fetchone()[0]))
print()

cur.execute(
    "SELECT name, COUNT(name) FROM btmp GROUP BY name ORDER BY COUNT(name) DESC LIMIT 10"
)
print("Top 10 username:")
print("\n".join(map(indent, cur.fetchall())))
print()

cur.execute(
    "SELECT ip, COUNT(ip) FROM btmp GROUP BY ip ORDER BY COUNT(ip) DESC LIMIT 10"
)
print("Top 10 IPs:")
print("\n".join(map(indent, cur.fetchall())))
print()

con.close()

con = sqlite3.connect("out/ssh-log.db")
cur = con.cursor()

cur.execute(
    """
        SELECT
            datetime(MIN(timestamp/1000), 'unixepoch', 'localtime'),
            datetime(MAX(timestamp/1000), 'unixepoch', 'localtime'),
            (MAX(timestamp) - MIN(timestamp))/(3600*24*1000)
        FROM ssh
    """
)
print("SSH crawling period:")
start, end, days = cur.fetchone()
print("  Start: {}".format(start))
print("  End: {}".format(end))
print("  Days: {}".format(days))
print()

cur.execute("SELECT COUNT(*) FROM ssh")
print("Total collected log count:")
print(indent(cur.fetchone()[0]))
print()

cur.execute(
    "SELECT password, COUNT(password) FROM ssh GROUP BY password ORDER BY COUNT(password) DESC LIMIT 10"
)
print("Top 10 passwords:")
print("\n".join(map(indent, cur.fetchall())))
print()

cur.execute(
    "SELECT name, COUNT(name) FROM ssh GROUP BY name ORDER BY COUNT(name) DESC LIMIT 10"
)
print("Top 10 usernames:")
print("\n".join(map(indent, cur.fetchall())))
print()

# Most common username and password combination
cur.execute(
    """
        SELECT
            name,
            password,
            COUNT(*) AS count
        FROM ssh
        GROUP BY name, password
        ORDER BY count DESC
        LIMIT 10
    """
)
print("Top 10 username and password combination:")
print("\n".join(map(indent, cur.fetchall())))
print()
