from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from time import sleep

class Bagre:
    def __init__(self, server, nick, name, mail, channel):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect((server,6667))
        sleep(0.5)
        self.s.recv(4096)
        self.nick = nick
        self.name = name
        self.mail = mail
        self.data = ''
        self.channel = channel
        self.command = None
        self.close = False

    def sendCommand(self, cmd):
        cmd = cmd + '\r\n'
        self.s.send(cmd)

    def sendPingResponse(self):
        if self.data.find('PING') != -1:
            self.sendCommand('PONG ' + self.data.split()[1])
            sleep(15)
    
    def Parse(self, cmd):
        tp = cmd.split(' ')
        numargs = len(tp)
        fmt = []

        if numargs == 0:
            self.sendCommand(cmd)
        else:
            for i in range(numargs):
                fmt.append(tp[i] + ' ')
            fmt = ' '.join(fmt)
            self.sendCommand(fmt)

    def ctcpVersion(self):
        if ":VERSION" in self.data:
            self.sendCommand('RPL_VERSION OpenBSD-BR 1.0.1')

        if ":!version" in self.data:
            cmd = "NOTICE {} :VERSION OpenBSD-BR 1.0.1 \r\n".format(self.channel)
            self.s.send(cmd)
        if ":!teste" in self.data:
            self.sendCommand('PRIVMSG ' + self.channel + ' comando de teste recebido')
    
    def run(self):
        self.sendCommand('NICK ' + self.nick)
        self.sendCommand('USER ' + self.nick + ' ' + self.name + ' ' + self.mail + ' : OpenBSD-BR')
        self.sendCommand('JOIN ' + self.channel)

        while self.close == False:
            self.data = self.s.recv(4096)
            self.sendPingResponse()
            sleep(0.5)

            #Commandos...
            #Responde ctcp version
            self.ctcpVersion()
            print("FROM SERVER -> " + self.data) # imprive tudo que vier do servidor
            if ":!teste" in self.data:
                self.sendCommand('PRIVMSG ' + self.channel + ' comando de teste recebido')
    
if __name__ == '__main__':
    server = 'irc.freenode.net'
    nick = 'bagre'
    name = 'openbsd-br'
    mail =  'shazaum@gmail.com'
    channel = '#openbsd-sh'

    bot = Bagre(server, nick , name , mail, channel)
    bot.run()