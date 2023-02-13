import os
import ssl

from flask import redirect, request

YEAR_SECONDS = 365 * 24 * 60 * 60

class SocketSecurityLayer:
    '''
    Secures socket communication.
    '''

    def __init__(self, application=None, expire_in=YEAR_SECONDS):
        self.application = application
        self.expire_in = expire_in

    @property
    def hsts_header(self):
        return "max-age={0}".format(self.expire_in)

    def set_hsts_header(self, response):
        if request.is_secure: 
            response.headers.setdefault("Strict-Transport-Security", self.hsts_header)

        return response

def define_ssl_context(private_key, certificate):
    if certificate and os.path.isfile(certificate) and private_key and os.path.isfile(private_key):
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(certificate, private_key)
        return context

    return None
