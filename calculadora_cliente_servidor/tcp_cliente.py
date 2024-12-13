# -*- coding: utf-8 -*-
__author__ = "Alvaro Braz e Diego Sanches"

import socket, sys


HOST = '200.239.153.26'  # endereço IP
PORT = 20000        # Porta utilizada pelo servidor
BUFFER_SIZE = 1024  # tamanho do buffer para recepção dos dados


def main(argv): 
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print("Aplicação cliente executando!")
            while(True):       
                texto = input("Digite o texto a ser enviado ao servidor:\n")
                s.send(texto.encode()) #texto.encode - converte a string para bytes

                if texto.startswith('/raizes'):
                    while True:
                        data = s.recv(BUFFER_SIZE)
                        texto_recebido = data.decode('utf-8') # converte os bytes em string
                        
                        if texto_recebido.lower() == 'fim':
                            break

                        print(texto_recebido)
                        texto = input(" ")
                        s.send(texto.encode()) #texto.encode - converte a string para bytes


                data = s.recv(BUFFER_SIZE)
                texto_recebido = data.decode('utf-8') # converte os bytes em string

                if (texto == 'sair'):
                    print('vai encerrar o socket cliente!')
                    s.close()
                    break

                print(f'Resultado da operação: {texto_recebido}')

    except Exception as error:
        print("Exceção - Programa será encerrado!")
        print(error)
        return


if __name__ == "__main__":   
    main(sys.argv[1:])
