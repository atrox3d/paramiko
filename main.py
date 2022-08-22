import paramiko
import time

import private.credentials as credentials

def getsshoutput(remote: paramiko.Channel):
    print('waiting for output...')
    time.sleep(5)

    print('receiving output...')
    print('-' * 80)
    output = remote.recv(1000)
    print(output.decode('utf-8'))
    print('-' * 80)


sshclient = paramiko.SSHClient()
sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

hostname = credentials.HOSTNAME
username = credentials.USERNAME
password = credentials.PASSWORD
banner_timeout = 10

print(f'connecting to {hostname} as {username}/{password}...')
try:
    sshclient.connect(
        hostname=hostname,
        username=username,
        password=password,
        # banner_timeout=banner_timeout
    )

    print(f'connected to {hostname}')

    print('invoking shell...')
    remote = sshclient.invoke_shell()
    print(f'shell invoked: {remote}')

    getsshoutput(remote)

    print('sending ?\\n...')
    remote.send('?\n'.encode())

    getsshoutput(remote)

    print('sending exit\\n...')
    remote.send('exit\n'.encode())

    getsshoutput(remote)


except Exception as e:
    print(e)

print(f'disconnecting from {hostname}...')
sshclient.close()
print(f'disconnected from {hostname}')
