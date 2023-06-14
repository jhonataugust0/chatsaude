import sys
import logging
import datetime
import pytz
import os

class Logging:
    filename = '.\log\log.txt'
    filemode = "a"
    format = """####### %(levelname)s ####### \nDATA: %(asctime)s \n%(message)s\n"""
    datefmt = '%d/%m/%y %H:%M:%S'

    def __init__(self, message):
        self.message = message

    async def config(self):
        """
            Método de configuração do Log
        """
        logging.basicConfig(
            filename=Logging.filename,
            filemode=Logging.filemode,
            format=Logging.format,
            datefmt=Logging.datefmt,
            level=logging.INFO
        )

    async def info(self):
        """
            Método informativo do Log
        """
        self.config()
        logger = logging.getLogger("python_log")

        if (logger.hasHandlers()):
            logger.handlers.clear()
        logger.addHandler(logging.StreamHandler(sys.stdout))

        mensagem = f""" \nINFO: {self.message}"""
        logger.info(mensagem)

    async def warning(self, function, user, error, status, parametros=None):
        """
            Método exibidor dos erros da aplicação
        """
        self.config()
        logger = logging.getLogger("python_log")

        if (logger.hasHandlers()):
            logger.handlers.clear()

        logger.addHandler(logging.StreamHandler(sys.stdout))

        current_hour = datetime.datetime.strftime(datetime.datetime.now(pytz.timezone("America/Sao_Paulo")), "%d-%m-%y %H:%M").replace('-','/')
        mensagem = f"""
            \n####### ERRO #######\nDATA: {current_hour}\nFUNCAO: {function}\nUSUARIO: {user}\nSTATUS: {status}\nMENSAGEM: {self.message}\nPARAMETROS: {parametros}\nERRO: {error}
        """
        logger.warning(mensagem)




