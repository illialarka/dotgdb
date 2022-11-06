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

def configure_logger(is_verbose):
    logging_level = logging.DEBUG if is_verbose else logging.INFO 

    handler = logging.StreamHandler() 
    handler.setLevel(logging_level) 

    logger = logging.getLogger()
    logger.setLevel(logging_level)
    logger.addHandler(handler)

