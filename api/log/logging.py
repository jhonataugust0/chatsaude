import sys
import logging
import datetime
import pytz

class Logging():
  filename = './log/log.txt'
  filemode = "a"
  format = """####### %(levelname)s ####### \nDATA: %(asctime)s \n%(message)s\n"""
  datefmt = '%d/%m/%y %H:%M:%S'

  def __init__(self, message):
    self.message = message

  def config(self):
    logging.basicConfig(
      filename=Logging.filename,
      filemode=Logging.filemode,
      format=Logging.format,
      datefmt=Logging.datefmt,
      level=logging.INFO
    )

  def info(self):
    self.config()
    logger = logging.getLogger()
    
    if (logger.hasHandlers()):
        logger.handlers.clear()
    logger.addHandler(logging.StreamHandler(sys.stdout))
    
    mensagem = f""" \nINFO: {self.message}"""
    logger.info(mensagem) 

  def warning(self, function, user, error, status, parametros=None):
    self.config()
    logger = logging.getLogger()
    
    if (logger.hasHandlers()):
        logger.handlers.clear()
    logger.addHandler(logging.StreamHandler(sys.stdout))
    
    current_hour = datetime.datetime.strftime(datetime.datetime.now(pytz.timezone("America/Sao_Paulo")), "%d-%m-%y %H:%M").replace('-','/')
    mensagem = f"""\n####### ERRO #######\nHORA: {current_hour}\nFUNCAO: {function} \nUSUARIO: {user} \nSTATUS: {status}  \nMENSAGEM: {self.message} \nPARAMETROS: {parametros}\nERRO: {error}"""
    logger.warning(mensagem)
