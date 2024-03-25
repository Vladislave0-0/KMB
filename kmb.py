'''
This is a program that implements a simple client-server application:
the client establishes a connection with a server located at a predetermined address, 
to which the server sends him a message informing him of the client's address.
At startup, you need to write the program's operating mode on the command line.

Here is an example of the launch in the most general form:
python3 kmb.py <host> <port> [-s | -c] [-t | -u] [-o | -f <file>]

Parameters:
· <host> - the host (ip address) of the server;
· <port> - server port number;
· -s - running the program in server mode;
· -c - running the program in client mode;
· -t - communication via TCP protocol;
· -u - communication via UDP protocol;
· -o - logging to standard output;
· -f <file> - logging to a file <file>.

If none of the parameters [-t | -u] are specified, [-t] will be used by default.
If none of the parameters [-o | -f <file>] are specified, [-o] will be used by default.

An example of running a program in a special case:
python3 kmb.py 127.0.0.1 13000 -s -f log_output.txt
· running the program in server mode over TCP protocol with logging to the log_output.txt file;
· the program opens a socket at 127.0.0.1:13000.
'''

import argparse
import logging
import socket
from ipaddress import ip_address
from time import sleep


def parse_string():
    '''
    Parsing and analyzing command line arguments.

    Returns:
        An object with parsed command line arguments.
        In case of an error, it terminates the program with the output
        of information to the terminal.
    '''

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

    parsed_args = parser.parse_args()

    return parsed_args


def setting_logs(log_output):
    '''
    Depending on the presence of the [-o] or [-f <file>] flag,
    the basicConfig() function of the logging module performs the basic configuration
    of the system to output logs to the desired location.

    Arg:
        log_output (str): parsed string

    Returns:
        None
    '''

    if log_output.o:
        logging.basicConfig(level=logging.INFO, format='%(levelname)s (%(asctime)s) | '
                            '(Line: %(lineno)d) [%(filename)s] | %(message)s', 
                            datefmt='%d/%m/%Y %I:%M:%S')
    elif log_output.f:
        logging.basicConfig(level=logging.INFO, format='%(levelname)s (%(asctime)s) | '
                            '(Line: %(lineno)d) [%(filename)s] | %(message)s', 
                            datefmt='%d/%m/%Y %I:%M:%S', encoding = 'utf-8', filename=args.f)


def validate_adress(host, port):
    '''
    Checks the correctness of the specified IP address and port.

    Args:
        host (str): The IP address of the server.
        port (str): The port number of the server.

    Returns:
        · 1 - if the address and port are correct,
        · 0 - if there are errors.

    Raises:
        · ValueError - occurs if the IP address is specified incorrectly.
    '''

    if port.isdigit():
        if int(port) < 0 or int(port) > 65536:
            logging.error("Port error\n")
            return 0
    else:
        logging.error("Port error\n")
        return 0

    try:
        ip_address(host)
    except ValueError:
        logging.error("Incorrect IP address\n")
        return 0

    return 1


def server_tcp(host, port):
    '''
    Setting up a TCP server on the specified host and port, waits for a connection, 
    and sends a message to the client.

    Args:
        host (str): The IP address of the server.
        port (int): The port number of the server.

    Returns:
        None
    '''

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    logging.info("The server (%s:%d) is ready to recieve data.", host, port)
    server_socket.listen(1)

    while True:
        connection_socket, cli_addr = server_socket.accept()
        logging.info("The TCP connection to the client (%s:%d) has been established.",
                     cli_addr[0], cli_addr[1])

        message = cli_addr[0] + ':' + str(cli_addr[1])
        connection_socket.send(message.encode('utf-8'))
        logging.info("The server sent a message \"%s\" to the client (%s:%d).",
                     message, cli_addr[0], cli_addr[1])

        sleep(0.05)
        connection_socket.close()
        logging.info("The TCP connection was terminate.\n")


def server_udp(host, port):
    '''
    Setting up a TCP server on the specified host and port,
    waits for a message and sends a message to the client.

    Args:
        host (str): The IP address of the server.
        port (int): The port number of the server.

    Returns:
        None
    '''

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', port))
    logging.info("The server (%s:%d) is ready to recieve data.", host, port)

    while True:
        recv_message = server_socket.recvfrom(1024)
        cli_addr, cli_port = recv_message[1][0], recv_message[1][1]
        logging.info("The server received a message from client (%s:%d).",
                     cli_addr, cli_port)

        message = cli_addr + ':' + str(cli_port)
        server_socket.sendto(message.encode('utf-8'), (cli_addr, cli_port))
        logging.info("The server sent a message \"%s\" to the client (%s:%d).",
                     message, cli_addr, cli_port)


def client_tcp(host, port):
    '''
    Establishes a TCP client connection to the server.
    Receives a message about clients address in the format <client_host>:<client_port>.

    Args:
        host (str): The IP address of the server.
        port (int): The port number of the server.

    Returns:
        None    
    '''

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.info("The client TCP socket was created.")

    client_socket.connect((host, port))
    message = client_socket.recv(1024).decode('utf-8')
    logging.info("The client received a message from the server: \"%s\".", message)
    print(message)

    client_socket.close()
    logging.info("The TCP client socket was closed.")


def client_udp(host, port):
    '''
    Establishes a UDP client connection to the server.
    Receives a message about clients address in the format <client_host>:<client_port>.

    Args:
        host (str): The IP address of the server.
        port (int): The port number of the server.

    Returns:
        None    
    '''

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    logging.info("The client UDP socket was created.")

    client_socket.sendto(''.encode('utf-8'), (host, port))
    logging.info("The client sent a request to the server (%s:%d)", host, port)

    message = client_socket.recv(1024).decode('utf-8')
    logging.info("The client received a message from the server: \"%s\".", message)
    print(message)

    client_socket.close()
    logging.info("The UDP client socket was closed.")


if __name__ == '__main__':
    args = parse_string()
    setting_logs(args)

    port_num = int(args.port)

    if validate_adress(args.host, args.port):
        if args.s:
            if args.u:
                server_udp(args.host, port_num)
            else:
                server_tcp(args.host, port_num)

        elif args.c:
            if args.u:
                client_udp(args.host, port_num)
            else:
                client_tcp(args.host, port_num)
