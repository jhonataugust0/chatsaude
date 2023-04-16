from fastapi import HTTPException, status, Response

from ..configs.connection import Connection
from ..entities.agendamentos_model import Agendamentos
from ..entities.user_model import Usuario
from ..entities.unidade_model import Unidade
from ..entities.especialidade_model import Especialidade
from ..repository.especialidade_repository import EspecialidadeRepository
from ..repository.unidade_repository import UnidadeRepository
from api.log.logging import Logging
from sqlalchemy.orm.exc import NoResultFound 
from sqlalchemy import select, MetaData, update, delete, text

from typing import List, Optional, Dict, Any, Union

class AgendamentosRepository:

  async def select_all(self) -> List[Dict[str, Agendamentos]] | None:
    async with Connection() as connection:
      try:
        query = select(Agendamentos)
        result = await connection.execute(query)
        rows = result.fetchall()
        return [await Agendamentos.as_dict(row) for row in rows]
      
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
      
      finally:
        await connection.close()
    
  async def select_data_schedule_from_user_id(self, user_id: int) -> Dict[str, Agendamentos] | None:
    """
      Busca no banco de dados a linha de dados do agendamento 
      pertencente ao usuário informado

        :params user_id: int 
      return dict
    """
    async with Connection() as connection:
      try:
        query = select(Agendamentos).where(Agendamentos.id_usuario == user_id)
        result = await connection.query(query)
        schedule_dict = await Agendamentos.as_dict(result.scalar_one())
        return schedule_dict   

      except NoResultFound:
        message = f"Não foi possível encontrar agendamentos relacionados ao usuário {user_id}"
        log = Logging(message)
        log.info()
        return None 

      except Exception as error:
        message = f"Erro ao resgatar dados de agendamento do usuário {user_id['id']}"
        log = Logging(message)
        log.warning('select_data_schedule_from_user_id', None, error, 500, {'params': {'user_id': user_id}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )
      
      finally:
        await connection.close()

  async def select_all_data_from_schedule_with_id(self, id: int) -> Dict[str, Union[Agendamentos, Unidade, Especialidade]]:
    async with Connection() as connection:
      try:
        query = select(Agendamentos).where(Agendamentos.id == id)
        result = await connection.execute(query)
        schedule_data = await Agendamentos.as_dict(result.scalar_one())
        
        unity_entity = UnidadeRepository()
        data_unity = await unity_entity.select_unity_from_id(int(schedule_data['id_unidade']))
        schedule_data['unity_info'] = data_unity

        specialty_entity = EspecialidadeRepository()
        data_specialty = await specialty_entity.select_specialty_from_id(schedule_data['id_especialidade'])
        schedule_data['specialty_info'] = data_specialty
        return schedule_data   

      except NoResultFound:
        message = f"Não foi possível encontrar agendamentos relacionados ao usuário {id}"
        log = Logging(message)
        log.info()
        return None 

      except Exception as error:
        message = f"Erro ao resgatar dados de agendamento do usuário {id['id']}"
        log = Logging(message)
        log.warning('select_data_schedule_from_user_id', None, error, 500, {'params': {'id': id}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

      finally:
        await connection.close()

  async def select_data_schedule_from_user_cellphone(self, cellphone: int) -> Dict[str, Agendamentos] | None:
    """
      Busca no banco de dados a linha de dados do agendamento 
      pertencente ao usuário informado

        :params user_id: int 
      return dict
    """
    async with Connection() as connection:
      try:
        query = select(Agendamentos, Usuario).join(
          Usuario, Agendamentos.id_usuario == Usuario.id).where(
            Usuario.telefone == cellphone).order_by(
            Agendamentos.id.desc()
            ).first()
        result = query._asdict()
        schedule = result['Agendamentos']._asdict()
        user_dict = result['Usuario']._asdict()
        schedule['usuario_info'] = user_dict
        return schedule

      except NoResultFound:
        message = f"Não foi possível encontrar agendamentos relacionados ao usuário de telefone {cellphone}"
        log = Logging(message)
        log.info()
        return None 

      except Exception as error:
        message = f"Erro ao resgatar dados de agendamento do usuário de telefone {cellphone}"
        log = Logging(message)
        log.warning('select_data_schedule_from_user_id', None, error, 500, {'params': {'cellphone': cellphone}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

      finally:
        await connection.close()

  async def insert_new_schedule_consult(self, user_id: int) -> Dict[str, Agendamentos] | None:
    """
      Inserta uma nova linha na tabela de agendamento  
        :params user_id: int - id do usuário
        :params specialty: str - especialidade do agendamento 
    """
    async with Connection() as connection:
      try:
        query = Agendamentos(id_usuario = user_id, tipo_agendamento = "Consulta", ativo = 1)
        connection.add(query)
        await connection.flush()
        schedule_dict = await connection.execute(select(Agendamentos).where(Agendamentos.id == query.id)).first()
        schedule_dict = Agendamentos.as_dict(schedule_dict)
        return schedule_dict
      
      except Exception as error:
        message = "Erro ao inserir um novo agendamento no banco de dados"
        log = Logging(message)
        log.warning('insert_new_schedule_consult', None, error, 500, {'params': {'user_id': user_id}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

      finally:
          await connection.close()
  
  async def update_schedule_from_user_id(self, id_usuario: int, table: str, input_data: int) -> Dict[str, Agendamentos] | None:
    """
      Atualiza uma coluna no banco de dados baseado no id do
      usuário informado

      :params id_usuario: int 
      :params table: str
      :params input_data: int
    """
    async with Connection() as connection:
      try:
        query = update(Agendamentos).where(Agendamentos.id_usuario == id_usuario).values({ table: input_data})
        result = await connection.execute(query)
        await connection.commit()
        schedule_dict = await Agendamentos.as_dict(result.fetchone())  
        return schedule_dict
      
      except NoResultFound:
        message = f"Não foi possível resgatar o agendamento do usuário de id {id_usuario}"
        log = Logging(message)
        log.info()
        return None
      
      except Exception as error:
        message = "Erro ao atualizar os dados do usuário"
        log = Logging(message)
        log.warning('update_schedule_from_user_id', None, error, 500, {'params': {'id_usuario':id_usuario, 'table': table, 'input_data': input_data}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        ) 

      finally:
          await connection.close()
      
  async def update_schedule_from_id(self, id_usuario: int, table: str, input_data: int) -> Dict[str, Agendamentos] | None:
    """
      Atualiza uma coluna no banco de dados baseado no id do
      usuário informado

      :params id_usuario: int 
      :params table: str
      :params input_data: int
    """
    async with Connection() as connection:
      try:
        query = update(Agendamentos).where(Agendamentos.id_usuario == id_usuario, Agendamentos.ativo == 1).values({ table: input_data})
        result = await connection.execute(query)
        await connection.commit()
        schedule_dict = await Agendamentos.as_dict(result.fetchone())  
        return schedule_dict 

      except NoResultFound:
        message = f"Não foi possível resgatar o agendamento do usuário de id {id_usuario}"
        log = Logging(message)
        log.info()
        return None
      
      except Exception as error:
        message = "Erro ao atualizar os dados do usuário"
        log = Logging(message)
        log.warning('update_schedule_from_user_id', None, error, 500, {'params': {'id_usuario':id_usuario, 'table': table, 'input_data': input_data}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )
      
      finally:
          await connection.close()
          
  async def delete_schedule_from_user_id(self, user_id: int) -> bool | None:
    """
      Delete uma linha da tabela agendamentos baseado no id 
      do usuário informado

      params: user_id: int
    """
    async with Connection() as connection:
      try:
        await connection.execute(Agendamentos.delete()).where(Agendamentos.id == user_id)
        await connection.commit()
        return True
      except NoResultFound:
        message = f"Não foi possível encontrar fluxos relacionados ao usuário {user_id}"
        log = Logging(message)
        log.info()
        return None 
 
      except Exception as error:
        message = f"Erro ao excluir o agendamento do usuário {user_id}"
        log = Logging(message)
        log.warning('delete_schedule_from_user_id', None, error, 500, {'params': {'user_id': user_id,}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

      finally:
          await connection.close()

  async def get_last_time_scheduele_from_specialty_id(self, specialty_id: int, unity_id: int) -> Dict[str, Agendamentos] | None:
    async with Connection() as connection:
      try:
        query = select(Agendamentos.data_agendamento, Agendamentos.horario_termino_agendamento).where(
          Agendamentos.id_especialidade == specialty_id, 
          Agendamentos.id_unidade == unity_id,
          Agendamentos.data_agendamento != None, 
          Agendamentos.horario_termino_agendamento != None
        ).order_by(Agendamentos.id.desc()).first()
        data_schedule = await Agendamentos.as_dict(query)
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

  async def check_conflicting_schedule(self, id_unity: int, id_specialty: int, date_schedule: str, init_time: str, end_time: str) -> List[Any] | None:
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
    async with Connection() as connection:
      try:
        query = await connection.execute(
          text("""
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
                  DIA DATE := :date_schedule;
                  DT_INICIO TIME := :init_time;
                  DT_FINAL TIME := :end_time;
              BEGIN
                  RETURN QUERY SELECT agen.id, agen.id_unidade, agen.id_especialidade, agen.data_agendamento, agen.horario_inicio_agendamento, agen.horario_termino_agendamento 
                  FROM AGENDAMENTOS agen
                  WHERE (agen.ID_UNIDADE = :id_unity) AND (agen.ID_ESPECIALIDADE = :id_specialty) AND (DIA = agen.DATA_AGENDAMENTO) AND
                  ( 
                      ( DT_INICIO <= agen.HORARIO_INICIO_AGENDAMENTO AND DT_FINAL >= agen.HORARIO_INICIO_AGENDAMENTO )
                      OR (DT_INICIO >= agen.HORARIO_INICIO_AGENDAMENTO AND DT_FINAL <= agen.HORARIO_TERMINO_AGENDAMENTO)
                      OR (DT_INICIO < agen.HORARIO_TERMINO_AGENDAMENTO AND DT_FINAL >= agen.HORARIO_TERMINO_AGENDAMENTO)
                      OR (DT_INICIO <= agen.HORARIO_INICIO_AGENDAMENTO AND DT_FINAL >= agen.HORARIO_TERMINO_AGENDAMENTO)
                  );
              END $$ LANGUAGE plpgsql;
              SELECT * FROM busca_agendamentos();
          """),
          {
            "id_unity": id_unity,
            "id_specialty": id_specialty,
            "date_schedule": date_schedule,
            "init_time": init_time,
            "end_time": end_time,
          },
      );
        result = query.fetchall()
        return result

      except Exception as error:
        message = f"Ao verificar a existência de conflitos"
        log = Logging(message)
        params = {'id_unity': id_unity, 'id_specialty': id_specialty, 'date_schedule': date_schedule, 'init_time': init_time, 'end_time': end_time}
        log.warning('check_conflicting_schedule', None, error, 500, {'params': {'params': params}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

      finally:
          await connection.close()

  # async def check_conflicting_schedule(self, id_unity: int, id_specialty: int, date_schedule: str, init_time: str, end_time: str) -> List[Any] | None:
  #   """
  #   Verificação de conflito de horários entre agendamentos na mesma unidade e especialidade

  #   :params id_unity: int
  #   :params id_specialty: int
  #   :params date_schedule: str
  #   :params init_time: str
  #   :params end_time: str
  #   return -> list
  #   """
  #   async with Connection() as connection:
  #     try:
  #       async with connection.session() as session:
  #         conflicting_schedules = await session.query(Agendamentos).filter(
  #           Agendamentos.id_unidade == id_unity,
  #           Agendamentos.id_especialidade == id_specialty,
  #           Agendamentos.data_agendamento == date_schedule,
  #           (
  #               (Agendamentos.horario_inicio_agendamento <= init_time) &
  #               (Agendamentos.horario_termino_agendamento >= init_time)
  #           ) | (
  #               (Agendamentos.horario_inicio_agendamento >= init_time) &
  #               (Agendamentos.horario_termino_agendamento <= end_time)
  #           ) | (
  #               (Agendamentos.horario_inicio_agendamento < end_time) &
  #               (Agendamentos.horario_termino_agendamento >= end_time)
  #           ) | (
  #               (Agendamentos.horario_inicio_agendamento <= init_time) &
  #               (Agendamentos.horario_termino_agendamento >= end_time)
  #           )
  #       ).all()
            
  #       return conflicting_schedules

  #     except Exception as error:
  #       message = f"Ao verificar a existência de conflitos"
  #       log = Logging(message)
  #       params = {'id_unity': id_unity, 'id_specialty': id_specialty, 'date_schedule': date_schedule, 'init_time': init_time, 'end_time': end_time}
  #       log.warning('check_conflicting_schedule', None, error, 500, {'params': {'params': params}})
  #       raise HTTPException(
  #           status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
  #           detail=message
  #       )

  #     finally:
  #         await connection.close()