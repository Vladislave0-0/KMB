# INPUT EXAMPLE: python3 kmb.py <host> <port> [-s] [-t | -u] [-o | -f <file>]

# Программа должна логировать следующие события:
# · Открытие (привязка) сокета;
# · Отправка сообщения;
# · Получение сообщения;
# · Закрытие сокета.


import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Программа для работы с хостом и портом')
    
    parser.add_argument('host', type=str, help='Хост (ip адрес) сервера')
    parser.add_argument('port', type=int, help='Номер порта сервера')

    group_mode = parser.add_mutually_exclusive_group()
    group_mode.add_argument('-s', action='store_true', help='Запуск программы в режиме сервера')
    group_mode.add_argument('-c', action='store_true', help='Запуск программы в режиме клиента')

    group_protocol = parser.add_mutually_exclusive_group()
    group_protocol.add_argument('-t', action='store_true', help='Связь по протоколу TCP')
    group_protocol.add_argument('-u', action='store_true', help='Связь по протоколу UDP')
    
    group_log = parser.add_mutually_exclusive_group()
    group_log.add_argument('-o', action='store_true', help='Логирование в стандартный вывод')
    group_log.add_argument('-f', metavar='<file>', type=str, help='Логирование в файл <file>')

    args = parser.parse_args()

    if args.s and args.c:
        parser.error('Нельзя указывать одновременно параметры -s и -c')

    if not args.s and not args.c:
        parser.error('Вы не указали ни один из обязательных параметров -s и -c')

    if args.t and args.u:
        parser.error('Нельзя указывать одновременно параметры -t и -u')


    print('Хост:', args.host)
    print('Порт:', args.port)

    if args.s:
        print('Режим сервера')
    if args.c:
        print('Режим клиента')

    if not args.t and not args.u:  
        print('Используется протокол TCP по умолчанию')
    elif args.u:
        print('Используется протокол UDP')
    elif args.t:
        print('Используется протокол TCP')

    if args.o:
        print('Логирование в стандартный вывод')
    elif not args.f:  
        print('Логирование в стандартный вывод по умолчанию')
    else:
        print('Логирование в файл:', args.f)
