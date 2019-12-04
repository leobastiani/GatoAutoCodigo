#!python3
#encoding=utf-8

import sys
import time
import re
import pyperclip


DEBUG = sys.flags.debug or False
def debug(*args):
    '''funciona como print, mas só é executada se sys.flags.debug == 1'''
    if not DEBUG:
        return ;
    print(*args)


def sleep(sec):
    if DEBUG:
        if sec >= 1:
            print('Sleep '+str(sec))
    else:
        time.sleep(sec)


# função que retorna login e senha
def getLoginPwd(clip):
    m = re.search(r'Login:\s+(\w+)\s*Senha:\s+(\w+)', clip)
    res = m.groups() if m else False
    return res


if DEBUG:
    pyperclip.copy('Login: asd123\nSenha: 123')

while True:
    loginPwd = getLoginPwd(pyperclip.paste())
    if loginPwd:
        break
    sleep(1)

print('Login e senha: '+str(loginPwd))

# envia por TCP


import socket

buttons = {
    'OK': '0E06D90E11',
    'CIMA': 'C4CC13C4C4',
    'BAIXO': 'D1D906D1D0',
    'ESQ': '0109D60102',
    'DIR': '525A855250',
    'PREV': '949C439EA6',
    'REC': 'CAC21DCAEA',
    'PAUSE': '878F5087BE',
    'STOP': '7078A77048',
    'PLAY': 'C4CC13C4F7',
    'NEXT': '868E518CD6',
    'REW': 'FCF42BFCCE',
    'RED': '555D82554E',
    'GREEN': '2820FF2827',
    'YELLOW': '3B33EC3B79',
    'BLUE': '8F87588F89',
    'FORW': '434B944313',
    'BACK': 'AAA27DAAAF',
    'MENU': 'F5FD22F5F2',
    'EXIT': 'DDD50ADDC0',
    '0': '5D558A5D4D',
    '1': '4F47984F5E',
    '2': '050DD20517',
    '3': '525A855241',
    '4': '6068B76074',
    '5': '7D75AA7D68',
    '6': 'B1B966B1A7',
    '7': '1E16C91E09',
    '8': 'DBD30CDBC3',
    '9': '1018C71009',
    'A': 'AAA27DABAB',
}


class XY:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def __sub__(self, xy):
        return XY(self.x-xy.x, self.y-xy.y)

    def toCmd(self):
        commands = []
        if self.x > 0:
            commands += ['DIR'] * self.x
        elif self.x < 0:
            commands += ['ESQ'] * -self.x

        if self.y > 0:
            commands += ['BAIXO'] * self.y
        elif self.y < 0:
            commands += ['CIMA'] * -self.y

        return commands

screen = XY(0, 0)

letras = {
    'q': XY(0, 0),
    'w': XY(1, 0),
    'e': XY(2, 0),
    'r': XY(3, 0),
    't': XY(4, 0),
    'y': XY(5, 0),
    'u': XY(6, 0),
    'i': XY(7, 0),
    'o': XY(8, 0),
    'p': XY(9, 0),
    'a': XY(0, 1),
    's': XY(1, 1),
    'd': XY(2, 1),
    'f': XY(3, 1),
    'g': XY(4, 1),
    'h': XY(5, 1),
    'j': XY(6, 1),
    'k': XY(7, 1),
    'l': XY(8, 1),
    'z': XY(0, 2),
    'x': XY(1, 2),
    'c': XY(2, 2),
    'v': XY(3, 2),
    'b': XY(4, 2),
    'n': XY(5, 2),
    'm': XY(6, 2),
}

def sequence(commands, interval=0.5):
    for cmd in commands:
        if not DEBUG:
            s.sendall(buttons[cmd].encode('utf-8'))
        print(cmd)
        sleep(interval)

def channelToCodigo():
    sequence(['MENU', 'BAIXO', 'BAIXO', 'OK'])
    sleep(3)
    sequence(['BAIXO', 'BAIXO', 'OK'])
    sleep(3)
    sequence(['BAIXO', 'OK'])
    sleep(3)
    sequence(['BAIXO', 'BAIXO', 'BAIXO', 'BAIXO', 'BAIXO', 'BAIXO', 'OK'])
    sleep(3)

def write(chars):
    debug('Write: "%s"' % chars)
    global screen
    chars = chars.lower()
    commands = []
    for c in chars:
        if c >= '0' and c <= '9':
            commands += [c]
            continue
        if c == ' ':
            toV = write('v')
            toV.pop()
            commands += toV + ['BAIXO', 'OK', 'CIMA']
            screen = letras['m']
            continue
        if c == '\x08':
            toL = write('l')
            toL.pop()
            commands += toL + ['BAIXO', 'BAIXO', 'OK', 'CIMA', 'CIMA']
            screen = letras['l']
            continue
        path = letras[c] - screen
        screen = letras[c]
        commands += path.toCmd() + ['OK']
    # tenho q fazer isso, pq qndo vou digitar de novo
    # volto pra Q
    screen = letras['q']
    return commands

def apagaTudo():
    debug('apagaTudo()')
    toL = write('l')
    toL.pop()
    res = toL + ['BAIXO']*2 + ['OK']*7 + ['CIMA']*2

    global screen
    screen = letras['l']
    return toL

def connect():
    if DEBUG:
        return
    while True:
        try:
            s.connect((HOST, PORT))
            break
        except Exception as e:
            pass




HOST = '192.168.0.163'    # The remote host
PORT = 51234              # The same port as used by the server
print('Aguardando conexão...')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    startTime = time.clock()
    s.settimeout(30)
    connect()
    endTime = time.clock()
    print('Conectado')
    if endTime > 10:
        # qr dizer q eu estou ligado o aparelho
        # espero ele iniciar
        print('O aparelho estava desligado...')
        sleep(30)
    sleep(1)
    channelToCodigo()
    apagaTudo()
    sleep(1)
    sequence(write(loginPwd[0]), 0.1)
    sequence(['YELLOW'])
    sequence(['BAIXO', 'OK'])
    apagaTudo()
    sequence(write(loginPwd[1]), 0.05)
    sequence(['YELLOW'])
    sequence(['CIMA', 'CIMA', 'CIMA', 'CIMA', 'CIMA', 'CIMA'])
