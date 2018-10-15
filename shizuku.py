import paramiko
import sys
from threading import Thread
from interactive import windows_shell
import urllib.request
import urllib.parse
url = 'http://192.168.99.1/newifi/ifiwen_hss.html'
f = urllib.request.urlopen(url)
#print(f.read().decode('utf-8'))
#from base64 import b85decode
#from gzip import decompress

class SSH():
    def __init__(self, hostname, passwd):

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=hostname, username='root', password=passwd)
        self.channel = self.ssh.get_transport().open_channel("session")
        self.channel.get_pty(term='linux')
        self.channel.invoke_shell()
        #windows_shell(self.channel)
        printer = screen(self.channel)
        printer.start()

    def do_command(self, command):
        self.channel.send_ready()
        self.channel.send(command.encode("utf-8"))

    def shell(self):
        try:
            while True:
                d = sys.stdin.read(1)
                if not d:
                    break
                self.channel.send(d)
        except EOFError:
            # user hit ^Z or F6
            sys.exit(0)


class screen(Thread):
    def __init__(self,channel):
        self.channel = channel
        Thread.__init__(self)
    def run(self):
        while True:
            data = self.channel.recv(256)
            if not data:
                sys.stdout.write("\r\n*** EOF ***\r\n\r\n")
                sys.stdout.flush()
                break
            sys.stdout.write(data.decode())
            sys.stdout.flush()

def link(ip: str, passwd: str):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip, username='root', password=passwd)
    channel = ssh.get_transport().open_channel("session")
    channel.set_combine_stderr(True)
    channel.get_pty(term='linux')
    channel.recv_ready()
    channel.invoke_shell()
    #windows_shell(channel)
    #stdin, stdout, stderr = channel.exec_command("wget --no-check-certificate https://gitee.com/zy143l/OpenWRT/raw/master/shizuku.ko")
    #result = stdout.read()

    #if not result:
       # result = stderr.read()

   # print(result.decode())



#client = SSH("192.168.99.1", "1234567890")
#ssh.connect(hostname=input("IP:"),port=22, username='root', password=input("Password:"))

client = SSH("192.168.99.1", input("Password:"))

#link(input("IP:"), input("Password:"))

#script_blob = b'ABzY88$82X0{<(`OUzAG&`sn`PApN-FDS}S)=w@d&CE;7=LG;LT=*{=0000'
#script_blob = decompress(b85decode(script_blob)).decode('utf-8')
#ssh.exec_command("touch 999")
script_blob = 'wget --no-check-certificate https://gitee.com/zy143l/OpenWRT/raw/master/shizuku;sh shizuku\r'
client.do_command(script_blob)
client.shell()
