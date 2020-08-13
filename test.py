from mikatools import crypto

from freedrop.networking import *
import paramiko
import socket
import time

"""
private, public = crypto.generate_keys()
crypto.save_key(private, "id_rsa")
crypto.save_key(public, "id_rsa.pub")
"""



def start_server(keyfile="id_rsa", level='INFO'):
    host, port = 'localhost', 3373
    BACKLOG = 10
    paramiko_level = getattr(paramiko.common, level)
    paramiko.common.logging.basicConfig(level=paramiko_level)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    server_socket.bind((host, port))
    server_socket.listen(BACKLOG)
    print("Yeah!")
    while True:
        conn, addr = server_socket.accept()

        host_key = paramiko.RSAKey.from_private_key_file(keyfile)
        transport = paramiko.Transport(conn)
        transport.add_server_key(host_key)
        transport.set_subsystem_handler(
            'sftp', paramiko.SFTPServer, StubSFTPServer)

        server = StubServer()
        transport.start_server(server=server)

        channel = transport.accept()
        while transport.is_active():
            time.sleep(1)

start_server()
print("server died")