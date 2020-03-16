import paramiko
import time


class FastwebRouter:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.client: paramiko.SSHClient = paramiko.SSHClient()
        self.remote: paramiko.Channel = None

    def __del__(self):
        if self.remote:
            self.remote.close()

    def __getsshoutput(self):
        try:
            print('waiting for output...')
            time.sleep(5)

            print('receiving output...')
            print('-' * 80)
            output = self.remote.recv(1000)
            print(output.decode('utf-8'))
            print('-' * 80)

        except Exception as e:
            print(e)

    def connect(self):
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        print(f'connecting to {self.hostname} as {self.username}/{self.password}...')
        try:
            self.client.connect(
                hostname=self.hostname,
                username=self.username,
                password=self.password,
                # banner_timeout=banner_timeout
            )
            print(f'connected to {self.hostname}')

            print('invoking shell...')
            self.remote = self.client.invoke_shell()
            # print(f'shell invoked: {remote}')
            self.__getsshoutput()

        except Exception as e:
            print(e)

    def sendcommand(self, command):
        try:
            print(f'sending {command}\\n...')
            self.remote.send(f'{command}\n')
            self.__getsshoutput()
        except Exception as e:
            print(e)
