# INPUT EXAMPLE: python3 kmb.py <host> <port> [-s] [-t | -u] [-o | -f <file>]

# Программа должна логировать следующие события:
# · Открытие (привязка) сокета;
# · Отправка сообщения;
# · Получение сообщения;
# · Закрытие сокета.


import argparse
import logging
from socket import *
from ipaddress import ip_address
from time import sleep


def parse_string():
    parser = argparse.ArgumentParser(description='A simple client-server application')
    
    parser.add_argument('host', type=str, help='Server host (ip address)')
    parser.add_argument('port', type=str, help='Server port number')

    group_mode = parser.add_mutually_exclusive_group()
    group_mode.add_argument('-s', action='store_true', help='Running the program in server mode')
    group_mode.add_argument('-c', action='store_true', help='Running the program in client mode')

    group_protocol = parser.add_mutually_exclusive_group()
    group_protocol.add_argument('-t', action='store_true', help='Connection via TCP protocol')
    group_protocol.add_argument('-u', action='store_true', help='Connection via UDP protocol')
    
    group_log = parser.add_mutually_exclusive_group()
    group_log.add_argument('-o', action='store_true', help='Logging to standard output')
    group_log.add_argument('-f', metavar='<file>', type=str, help='Logging to a file <file>')

    args = parser.parse_args()

    return args


def setting_logs(args):
    if args.o:
        logging.basicConfig(level=logging.INFO, format='%(levelname)s (%(asctime)s) | (Line: %(lineno)d) [%(filename)s] | %(message)s', 
                            datefmt='%d/%m/%Y %I:%M:%S')
    elif args.f:
        logging.basicConfig(level=logging.INFO, filename=args.f, format='%(levelname)s (%(asctime)s) | (Line: %(lineno)d) [%(filename)s] | %(message)s', 
                            datefmt='%d/%m/%Y %I:%M:%S', encoding = 'utf-8')


def validate_ip_adress(host, port):
    if port.isdigit():
        if int(port) < 0 or int(port) > 65536:
            logging.error("Port error\n")
            return 0
    else:
        logging.error("Port error\n")
        return 0
    
    try:
        ip = ip_address(host)
    except ValueError:
        logging.error("Incorrect IP address\n")
        return 0


    return 1


def server_tcp(host, port):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', port))
    logging.info("The server (%s:%d) is ready to recieve data.", host, port)
    serverSocket.listen(1)

    while True:
        connectionSocket, cliAddr = serverSocket.accept()
        logging.info("The TCP connection to the client (%s:%d) has been established.", cliAddr[0], cliAddr[1])

        message = cliAddr[0] + ':' + str(cliAddr[1])
        connectionSocket.send(message.encode('utf-8'))
        logging.info("The server sent a message \"%s\" to the client (%s:%d).", message, cliAddr[0], cliAddr[1])

        sleep(0.05)
        connectionSocket.close()
        logging.info("The TCP connection was terminate.\n")


def client_tcp(host, port):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    logging.info("Client TCP socket was created.")
    
    clientSocket.connect((host, port))
    message = clientSocket.recv(1024).decode('utf-8')
    logging.info("The client received a message from the server: \"%s\".", message)
    print(message)

    clientSocket.close()
    logging.info("The TCP client socket was closed.")


if __name__ == '__main__':
    args = parse_string()
    setting_logs(args)

    host, port = args.host, int(args.port)

    if validate_ip_adress(args.host, args.port):
        if args.s:
            if args.t:
                server_tcp(host, port)
            # elif args.u:
            #     server_udp(host, port)

        elif args.c:
            if args.t:
                client_tcp(host, port)
            # elif args.u:
            #     client_udp(host, port)
