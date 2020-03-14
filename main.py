import paramiko
import time


def getsshoutput(remote: paramiko.Channel):
    print('waiting for output...')
    time.sleep(5)

    print('receiving output...')
    output = remote.recv(1000)
    print(output.decode('utf-8'))


sshclient = paramiko.SSHClient()
sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

hostname = '192.168.1.254'
username = 'admin'
password = 'p0rc0d10.router.fastweb'
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
    remote.send('?\n')

    getsshoutput(remote)

    print('sending exit\\n...')
    remote.send('exit\n')

    getsshoutput(remote)


except Exception as e:
    print(e)

# sshsession = sshclient.get_transport().open_session()
# print(sshsession)
#
# if sshsession.active:
#     print('active')


# stdin, stdout, stderr = sshclient.exec_command('\n\n\n\nhelp')
# print(stdout.readlines())

print(f'disconnecting from {hostname}...')
sshclient.close()
print(f'disconnected from {hostname}')
