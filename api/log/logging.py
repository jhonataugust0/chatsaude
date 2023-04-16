import os
import sys
import logging
import datetime
import pytz

class Logging:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'log', 'log.txt'))
        console_handler = logging.StreamHandler()
        handler = logging.FileHandler(log_path)
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def info(self):
      self.logger.info(self.name)

    def warning(self, function, user, error, status, parametros=None):
      current_hour = datetime.datetime.strftime(datetime.datetime.now(pytz.timezone("America/Sao_Paulo")), "%d-%m-%y %H:%M").replace('-','/')
      mensagem = f"""\n####### ERRO #######\nHORA: {current_hour}\nFUNCAO: {function} \nUSUARIO: {user} \nSTATUS: {status}  \nMENSAGEM: {self.name} \nPARAMETROS: {parametros}\nERRO: {error}\n"""
      self.logger.warning(mensagem)
