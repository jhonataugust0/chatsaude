from ..configs.connection import Connection
from ..entities.fluxo_etapa_model import FluxoEtapa
from log.logging import Logging
from sqlalchemy.orm.exc import NoResultFound 

class FluxoEtapaRepository:

  def select_all(self):
    """
      Resgata todas as linhas da tabela fluxo_etapa
      return dict
    """
    with Connection() as connection:
      try:
        data = connection.session.query(FluxoEtapa).all()
        stage = str(data).replace(' ', '').split(',')
        stage = dict(i.split("=") for i in stage)
        return stage 
     
      except NoResultFound:
        message = f"Não foi possível resgatar os fluxos"
        log = Logging(message)
        log.info()
        return {} 

  def select_stage_from_user_id(self, user_id: int):
    """
      Busca no banco de dados a linha de fluxo correspondente 
      ao usuário informado

      :params user_id: int 
      return dict
    """

    with Connection() as connection:
     
      try:
        data = connection.session.query(FluxoEtapa).filter(FluxoEtapa.id_usuario == user_id).one()
        stage = str(data).replace(' ', '').split(',')
        stage = dict(i.split("=") for i in stage)
        return stage   
      
      except NoResultFound as error:
        message = f"Não foi possível encontrar fluxos relacionados ao usuário {user_id}"
        log = Logging(f'{message}\n' + f'{error}')
        log.info()
        return {'value': None}
      
      except Exception as error:
        message = "Erro ao resgatar dados do usuário"
        log = Logging(message)
        log.warning('select_stage_from_user_id', None, error, 500, {'params': {'user_id': user_id}})
        return {}
  
  def insert_new_user_flow(self, user_id: int, flow: int, status: int):
    """
      Inserta uma nova linha na tabela de fluxos 
        :params user_id: int - id do usuário
        :params flow: int - estado da coluna 
        :params status: int - valor de etapa da coluna
    """
    with Connection() as connection:
      try:
        data_insert = FluxoEtapa(id_usuario = user_id, fluxo_registro = flow, etapa_registro = status, fluxo_agendamento_consulta = 0, etapa_agendamento_consulta = 0, fluxo_agendamento_exame = 0, etapa_agendamento_exame = 0, lista_unidades = 0, fluxo_denuncia = 0)
        connection.session.add(data_insert)
        connection.session.commit()
        stage = str(data_insert).replace(' ', '').split(',')
        stage = dict(i.split("=") for i in stage)
        return stage
      except Exception as error:
        message = "Erro ao inserir um novo fluxo no banco de dados"
        log = Logging(message)
        log.warning('insert_new_register_flow', None, error, 500, {'params': {'flow': flow, 'status': status}})
      return {}

  # def insert_new_schedule_consult_flow(self, user_id: int, flow: int, status: int):
  #   """
  #     Inserta uma nova linha na tabela de fluxos - agendamento de consulta
  #       :params coluna_fluxo: str - nome da coluna de fluxo
  #       :params flow: int - estado da coluna 
  #       :params status: int - valor de etapa da coluna
  #   """
  #   with Connection() as connection:
  #     try:
  #       data_insert = FluxoEtapa(id_usuario = user_id, fluxo_agendamento_consulta = flow, etapa_agendamento_consulta = status)
  #       connection.session.add(data_insert)
  #       connection.session.commit()
  #       stage = str(data_insert).replace(' ', '').split(',')
  #       stage = dict(i.split("=") for i in stage)
  #       return stage
  #     except Exception as error:
  #       message = "Erro ao inserir um novo fluxo no banco de dados"
  #       log = Logging(message)
  #       log.warning('insert_new_schedule_consult_flow', None, error, 500, {'params': {'flow': flow, 'status': status}})
  #     return {}

  def update_flow_from_user_id(self, id_usuario: int, table: str, input_data: int):
    """
      Atualiza uma coluna no banco de dados baseado no id do
      usuário informado

      :params id_usuario: int 
      :params table: str
      :params input_data: int
    """
    with Connection() as connection:
     
      try:
        connection.session.query(FluxoEtapa).filter(FluxoEtapa.id_usuario == id_usuario).update({ table: input_data})
        connection.session.commit()
        
        stage = connection.session.query(FluxoEtapa).filter(FluxoEtapa.id_usuario == id_usuario).one()
        stage = str(stage).replace(' ', '').split(',')
        data_stage = dict(i.split("=") for i in stage)

        return data_stage  
      
      except Exception as error:
        message = "Erro ao atualizar os dados do usuário"
        log = Logging(message)
        log.warning('update_flow_from_user_id', None, error, 500, {'params': {'id_usuario':id_usuario, 'table': table, 'input_data': input_data}})
        return {}
  
  
  def delete_flow_from_user_id(self, user_id: int):
    """
      Delete uma linha da tabela fluxo_etapa baseado no id 
      informado

      params: user_id: int
    """
    with Connection() as connection:
      try:
        connection.session.query(FluxoEtapa).filter(FluxoEtapa.id == user_id).delete()
        connection.session.commit()
        
      except NoResultFound:
        message = f"Não foi possível encontrar fluxos relacionados ao usuário {user_id}"
        log = Logging(message)
        log.info()
        return {} 
 
      except Exception as error:
        message = f"Erro ao excluir o agendamento do usuário {user_id}"
        log = Logging(message)
        log.warning('delete_flow_from_user_id', None, error, 500, {'params': {'user_id': user_id,}})
        return {}

