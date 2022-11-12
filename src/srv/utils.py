import socket
import logging

def find_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]
    except Exception:
        return None
    finally:
        sock.close()

def configure_logger(arguments):
    logging_level = logging.DEBUG if arguments.verbose else logging.INFO

    handler = logging.StreamHandler()
    handler.setLevel(logging_level)

    if arguments.logFile is not None:
        logging.basicConfig(filename=arguments.logFile)

    logger = logging.getLogger()
    logger.setLevel(logging_level)
    logger.addHandler(handler)

