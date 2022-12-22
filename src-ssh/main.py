#!/usr/bin/env python
import queue
import socket
import sqlite3
import threading
from datetime import datetime

import paramiko


class Server(paramiko.ServerInterface):
    def __init__(self, addr, log_queue):
        self.event = threading.Event()
        self.addr = addr
        self.log_queue = log_queue

    def _log(self, username, password):
        ip, port = self.addr
        timestamp = int(datetime.now().timestamp()*1000)
        self.log_queue.put((username, password, ip, port, timestamp))

    def check_auth_password(self, username: str, password: str) -> int:
        print(username, password)
        return super().check_auth_password(username, password)


def listener(client, log_queue, addr):
    print(addr)
    transport = paramiko.Transport(client)
    transport.set_gss_host(socket.getfqdn(""))
    transport.load_server_moduli()
    transport.add_server_key(paramiko.RSAKey(filename='./id_rsa'))
    server = Server(addr, log_queue)
    transport.start_server(server=server)
    server.event.wait(30)
    transport.close()


def logger(log_queue: queue.Queue):
    con = sqlite3.connect('/out/ssh-log.db')
    cur = con.cursor()
    try:
        cur.execute(
            'CREATE TABLE ssh (name text, password text, ip text, port int, timestamp int)')
        con.commit()
        print('Table created.')
    except:
        print("Skip table creation")

    while True:
        (username, password, ip, port, timestamp) = log_queue.get()
        cur.execute('INSERT INTO ssh VALUES (?,?,?,?,?)',
                    (username, password, ip, port, timestamp))
        con.commit()


def main():
    log_queue = queue.Queue()

    logger_thread = threading.Thread(target=logger, args=[log_queue])
    logger_thread.start()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 22))
    sock.listen(100)

    while True:
        client, addr = sock.accept()
        listener_thread = threading.Thread(
            target=listener, args=[client, addr])
        listener_thread.start()


main()
