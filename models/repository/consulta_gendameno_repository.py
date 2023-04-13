from fastapi import HTTPException, status, Response

from ..configs.connection import Connection
from ..entities.agendamentos_model import Agendamentos
from ..repository.especialidade_repository import EspecialidadeRepository
from ..repository.unidade_repository import UnidadeRepository
from log.logging import Logging
from sqlalchemy.orm.exc import NoResultFound 


class AgendamentosRepository:

  def select_all(self):
    with Connection() as connection:
      try:
        data = connection.session.query(Agendamentos).all()
        schedule = str(data).replace(' ', '').split(',')
        schedule = dict(i.split("=") for i in schedule)
        return schedule
      
      except NoResultFound as error:
        message = f"Não foi possível resgatar os agendamentos"
        log = Logging(f'{message}\n' + f'{error}')
        log.info()
        return {} 

      except Exception as error:
        message = "Erro ao resgatar dados de agendamento"
        log = Logging(message)
        log.warning('select_all', None, error, 500, {'params': None})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

  def select_data_schedule_from_user_id(self, user_id: int):
    """
      Busca no banco de dados a linha de dados do agendamento 
      pertencente ao usuário informado

        :params user_id: int 
      return dict
    """
    with Connection() as connection:
      try:
        data = connection.session.query(Agendamentos).filter(Agendamentos.id_usuario == user_id).one()
        schedule = str(data).replace(' ', '').split(',')
        schedule = dict(i.split("=") for i in schedule)
        return schedule   

      except NoResultFound:
        message = f"Não foi possível encontrar agendamentos relacionados ao usuário {user_id}"
        log = Logging(message)
        log.info()
        return {} 

      except Exception as error:
        message = f"Erro ao resgatar dados de agendamento do usuário {user_id['id']}"
        log = Logging(message)
        log.warning('select_data_schedule_from_user_id', None, error, 500, {'params': {'user_id': user_id}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

  def select_all_data_from_schedule_with_id(self, id: int):
    with Connection() as connection:
      try:
        data = connection.session.query(Agendamentos).filter(Agendamentos.id_usuario == id).one()
        schedule_data = str(data).replace(' ', '').split(',')
        schedule_data = dict(i.split("=") for i in schedule_data)
        
        unity_entity = UnidadeRepository()
        data_unity = unity_entity.select_unity_from_id(schedule_data['id'])
        schedule_data['unity_info'] = data_unity

        specialty_entity = EspecialidadeRepository()
        data_specialty = specialty_entity.select_specialty_from_id(schedule_data['id_especialidade'])
        schedule_data['specialty_info'] = data_specialty
        return schedule_data   

      except NoResultFound:
        message = f"Não foi possível encontrar agendamentos relacionados ao usuário {id}"
        log = Logging(message)
        log.info()
        return {} 

      except Exception as error:
        message = f"Erro ao resgatar dados de agendamento do usuário {id['id']}"
        log = Logging(message)
        log.warning('select_data_schedule_from_user_id', None, error, 500, {'params': {'id': id}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

  def insert_new_schedule_consult(self, user_id: int):
    """
      Inserta uma nova linha na tabela de agendamento  
        :params user_id: int - id do usuário
        :params specialty: str - especialidade do agendamento 
    """
    with Connection() as connection:
      try:
        data_insert = Agendamentos(id_usuario = user_id, tipo_agendamento = "Consulta", ativo = 1)
        connection.session.add(data_insert)
        connection.session.commit()
        schedule = str(data_insert).replace(' ', '').split(',')
        schedule = dict(i.split("=") for i in schedule)
        return schedule
      
      except Exception as error:
        message = "Erro ao inserir um novo agendamento no banco de dados"
        log = Logging(message)
        log.warning('insert_new_schedule_consult', None, error, 500, {'params': {'user_id': user_id}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )
  
  def update_schedule_from_user_id(self, id_usuario: int, table: str, input_data: int):
    """
      Atualiza uma coluna no banco de dados baseado no id do
      usuário informado

      :params id_usuario: int 
      :params table: str
      :params input_data: int
    """
    with Connection() as connection:
      try:
        connection.session.query(Agendamentos).filter(Agendamentos.id_usuario == id_usuario).update({ table: input_data})
        connection.session.commit()

        schedule = connection.session.query(Agendamentos).filter(Agendamentos.id_usuario == id_usuario).first()
        schedule = str(schedule).replace(' ', '').split(',')
        data_schedule = dict(i.split("=") for i in schedule)
        return data_schedule  
      
      except Exception as error:
        message = "Erro ao atualizar os dados do usuário"
        log = Logging(message)
        log.warning('update_schedule_from_user_id', None, error, 500, {'params': {'id_usuario':id_usuario, 'table': table, 'input_data': input_data}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )
      
  def update_schedule_from_id(self, id_usuario: int, table: str, input_data: int):
    """
      Atualiza uma coluna no banco de dados baseado no id do
      usuário informado

      :params id_usuario: int 
      :params table: str
      :params input_data: int
    """
    with Connection() as connection:
      try:
        connection.session.query(Agendamentos).filter(Agendamentos.id_usuario == id_usuario, Agendamentos.ativo == 1).update({ table: input_data})
        connection.session.commit()

        schedule = connection.session.query(Agendamentos).filter(Agendamentos.id_usuario == id_usuario, Agendamentos.ativo == 1).first()
        schedule = str(schedule).replace(' ', '').split(',')
        data_schedule = dict(i.split("=") for i in schedule)
        return data_schedule  
      
      except Exception as error:
        message = "Erro ao atualizar os dados do usuário"
        log = Logging(message)
        log.warning('update_schedule_from_user_id', None, error, 500, {'params': {'id_usuario':id_usuario, 'table': table, 'input_data': input_data}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

  def delete_schedule_from_user_id(self, user_id: int):
    """
      Delete uma linha da tabela agendamentos baseado no id 
      do usuário informado

      params: user_id: int
    """
    with Connection() as connection:
      try:
        connection.session.query(Agendamentos).filter(Agendamentos.id == user_id).delete()
        connection.session.commit()
        
      except NoResultFound:
        message = f"Não foi possível encontrar fluxos relacionados ao usuário {user_id}"
        log = Logging(message)
        log.info()
        return {} 
 
      except Exception as error:
        message = f"Erro ao excluir o agendamento do usuário {user_id}"
        log = Logging(message)
        log.warning('delete_schedule_from_user_id', None, error, 500, {'params': {'user_id': user_id,}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )
  
  def get_last_time_scheduele_from_specialty_id(self, specialty_id: int, unity_id: int):
    with Connection() as connection:
      try:
        data = connection.session.query(
          Agendamentos.data_agendamento, 
          Agendamentos.horario_termino_agendamento).filter(
          Agendamentos.id_especialidade == specialty_id, 
          Agendamentos.id_unidade == unity_id,
          Agendamentos.data_agendamento != None, 
          Agendamentos.horario_termino_agendamento != None).order_by(
          Agendamentos.id.desc()).first()
        data_schedule = dict(zip(data._fields, data))
        return data_schedule   

      except NoResultFound:
        message = f"Não foi possível encontrar agendamentos com a especialidade de id {specialty_id} na unidade de id {unity_id}"
        log = Logging(message)
        log.info()
        return {} 

      except Exception as error:
        message = f"Erro ao resgatar dados de agendamentos com a especialidade de id {specialty_id} na unidade de id {unity_id}"
        log = Logging(message)
        log.warning('select_data_schedule_from_user_id', None, error, 500, {'params': {'specialty_id': specialty_id, 'unity_id': unity_id}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

  def check_conflicting_schedule(self, id_unity: int, id_specialty: int, date_schedule: str, init_time: str, end_time: str):
    """
      Verificação de conflito de horários entre agendamentos 
      na mesma unidade e especialidade

        :params id_unity: int
        :params id_specialty: int
        :params date_schedule: str
        :params init_time: str
        :params end_time: str
        return -> list
    """
    with Connection() as connection:
      try:
        query = connection.session.execute(f"""
            CREATE OR REPLACE FUNCTION busca_agendamentos()
            RETURNS TABLE (
                id INTEGER,
                id_unidade INTEGER,
                id_especialidade INTEGER,
                data_agendamento DATE,
                horario_inicio_agendamento TIME,
                horario_termino_agendamento TIME
            ) AS $$
            DECLARE
                DIA DATE := '{date_schedule}';
                DT_INICIO TIME := '{init_time}';
                DT_FINAL TIME := '{end_time}';
            BEGIN
                RETURN QUERY SELECT agen.id, agen.id_unidade, agen.id_especialidade, agen.data_agendamento, agen.horario_inicio_agendamento, agen.horario_termino_agendamento 
              FROM AGENDAMENTOS agen
              WHERE (agen.ID_UNIDADE = {id_unity}) AND (agen.ID_ESPECIALIDADE = {id_specialty}) AND (DIA = agen.DATA_AGENDAMENTO) AND
              ( 
                ( DT_INICIO <= agen.HORARIO_INICIO_AGENDAMENTO AND DT_FINAL >= agen.HORARIO_INICIO_AGENDAMENTO )
                OR (DT_INICIO >= agen.HORARIO_INICIO_AGENDAMENTO AND DT_FINAL <= agen.HORARIO_TERMINO_AGENDAMENTO)
                OR (DT_INICIO < agen.HORARIO_TERMINO_AGENDAMENTO AND DT_FINAL >= agen.HORARIO_TERMINO_AGENDAMENTO)
                OR (DT_INICIO <= agen.HORARIO_INICIO_AGENDAMENTO AND DT_FINAL >= agen.HORARIO_TERMINO_AGENDAMENTO)
              );
            END $$ LANGUAGE plpgsql;
            SELECT * FROM busca_agendamentos();
        """);
        result = query.fetchall();
        return result;

      except Exception as error:
        message = f"Ao verificar a existência de conflitos"
        log = Logging(message)
        params = {'id_unity': id_unity, 'id_specialty': id_specialty, 'date_schedule': date_schedule, 'init_time': init_time, 'end_time': end_time}
        log.warning('check_conflicting_schedule', None, error, 500, {'params': {'params': params}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )