import socket, sys
from threading import Thread
import math

HOST = '200.239.153.26'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados


# O servidor deve realizar pelo menos 7 cálculos diferentes:
# adição, subtração, multiplicação, divisão, raiz quadrada, log2 e
# cálculo das raízes de uma equação de segundo grau.

def receber_dados(clientsocket):
    while True:
        data = clientsocket.recv(BUFFER_SIZE)
        if data:
            texto_recebido = data.decode()
            return texto_recebido

def somar(n1, n2):
    return str(n1 + n2)

def subtrair(n1, n2):
    return str(n1 - n2)

def multiplicar(n1, n2):
    return str(n1 * n2)

def dividir(n1, n2):
    return str(n1 / n2)

def raiz_quadrada(n1):
    return str(math.sqrt(n1))

def log2(n1):
    return str(math.log2(n1))

def raizes(a,b,c):
    delta = b*b - 4*a*c
    x1 = (-b + float(raiz_quadrada(delta)))/(2*a)
    x2 = (-b - float(raiz_quadrada(delta)))/(2*a)
    return x1, x2


def on_new_client(clientsocket, addr):
    while True:
        try:
            data = clientsocket.recv(BUFFER_SIZE)
            if not data:
                break
            texto_recebido = data.decode()
            if texto_recebido.startswith("/somar"):
                numeros = texto_recebido.split(" ", 2)
                n1 = float(numeros[1])
                n2 = float(numeros[2])
                resultado = somar(n1, n2)
                clientsocket.send(resultado.encode())
            if texto_recebido.startswith("/subtrair"):
                numeros = texto_recebido.split(" ", 2)
                n1 = float(numeros[1])
                n2 = float(numeros[2])
                resultado = subtrair(n1, n2)
                clientsocket.send(resultado.encode())
            if texto_recebido.startswith("/multiplicar"):
                numeros = texto_recebido.split(" ", 2)
                n1 = float(numeros[1])
                n2 = float(numeros[2])
                resultado = multiplicar(n1, n2)
                clientsocket.send(resultado.encode())
            if texto_recebido.startswith("/dividir"):
                numeros = texto_recebido.split(" ", 2)
                n1 = float(numeros[1])
                n2 = float(numeros[2])
                resultado = dividir(n1, n2)
                clientsocket.send(resultado.encode())
            if texto_recebido.startswith("/raiz_quadrada"):
                n1 = texto_recebido.split(" ", 1)[1]
                resultado = raiz_quadrada(n1)
                clientsocket.send(resultado.encode())
            if texto_recebido.startswith("/log2"):
                n1 = texto_recebido.split(" ", 1)[1]
                resultado = log2(n1)
                clientsocket.send(resultado.encode())
            
            if texto_recebido.startswith("/raizes"):
                clientsocket.send("Informe o valor de a: ".encode())
                a = float(receber_dados(clientsocket))
                clientsocket.send("Informe o valor de b: ".encode())
                b = float(receber_dados(clientsocket))
                clientsocket.send("Informe o valor de c: ".encode())
                c = float(receber_dados(clientsocket))

                clientsocket.send("Fim".encode())

                x1, x2 = raizes(a, b, c)
                clientsocket.send(f'{x1}, {x2}'.encode())
                

            


            if (texto_recebido == 'sair'):
                print('\tvai encerrar o socket do cliente {} !'.format(addr[0]))
                clientsocket.close() 
                return 
        except Exception as error:
            print("\tErro na conexão com o cliente!!")
            print(error)
            return


def main(argv):
    try:
        # AF_INET: indica o protocolo IPv4. SOCK_STREAM: tipo de socket para TCP,
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            print('Vai iniciar servidor.')
            print(f'Servidor registrou a porta {PORT} no Sistema Operacional.')
            while True:
                server_socket.listen()
                print('Servidor está aguardando conexões...')
                clientsocket, addr = server_socket.accept()
                print('\tServidor recebeu conexão do cliente ao cliente no endereço:', addr)
                print('\tThread para tratar conexão será iniciada')
                t = Thread(target=on_new_client, args=(clientsocket,addr))
                t.start()   
    except Exception as error:
        print("\tErro na execução do servidor!!")
        print(error)        
        return             



if __name__ == "__main__":   
    main(sys.argv[1:])
