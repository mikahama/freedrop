import paramiko
from mikatools import crypto

def start_client():
    print("juu")
    pkey = paramiko.RSAKey.from_private_key_file("id_rsa")
    print("oooo")
    transport = paramiko.Transport(('localhost', 3373))
    transport.connect(username='admin',  pkey=pkey)
    print("ok")
    sftp = paramiko.SFTPClient.from_transport(transport)
    print(sftp.listdir('.'))

#private, public = crypto.generate_keys()
#crypto.save_key(private, "id_rsa")
#crypto.save_key(public, "id_rsa.pub")

start_client()
