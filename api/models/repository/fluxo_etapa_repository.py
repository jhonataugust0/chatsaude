from fastapi import HTTPException, status, Response

from ..configs.connection import Connection
from ..entities.fluxo_etapa_model import FluxoEtapa
from api.log.logging import Logging
from sqlalchemy.orm.exc import NoResultFound 

from sqlalchemy import select, MetaData, update, delete

from typing import List, Optional, Dict, Any

class FluxoEtapaRepository:

  async def select_all(self) -> List[Dict[str, FluxoEtapa]]:
    """
      Resgata todas as linhas da tabela fluxo_etapa
      return dict
    """
    async with Connection() as connection:
      try:
        query = select(FluxoEtapa)
        result = await connection.execute(query)
        rows = result.fetchall()
        return [await FluxoEtapa.as_dict(row) for row in rows]
     
      except NoResultFound:
        message = f"Não foi possível resgatar os fluxos"
        log = Logging(message)
        log.info()
        return None
      
      except Exception as error:
        message = "Erro ao resgatar todos os fluxos"
        log = Logging(message)
        log.warning('select_stage_from_user_id', None, error, 500, {'params': None})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )
      
      finally:
        await connection.close()

  async def select_stage_from_user_id(self, user_id: int) -> Dict[str, FluxoEtapa]:
    """
      Busca no banco de dados a linha de fluxo correspondente 
      ao usuário informado

      :params user_id: int 
    """

    async with Connection() as connection:
     
      try:
        query = select(FluxoEtapa).where(FluxoEtapa.id_usuario == user_id)
        result = await connection.execute(query)
        stage_dict = await FluxoEtapa.as_dict(result.scalar_one())
        return stage_dict   
      
      except NoResultFound as error:
        message = f"Não foi possível encontrar fluxos relacionados ao usuário {user_id}"
        log = Logging(f'{message}\n' + f'{error}')
        log.info()
        return {}
      
      except Exception as error:
        message = "Erro ao resgatar dados do usuário"
        log = Logging(message)
        log.warning('select_stage_from_user_id', None, error, 500, {'params': {'user_id': user_id}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )
      
      finally:
        await connection.close()

  async def insert_new_user_flow(self, user_id: int, flow: int, status: int) -> Dict[str, FluxoEtapa]:
    """
      Inserta uma nova linha na tabela de fluxos 
        :params user_id: int - id do usuário
        :params flow: int - estado da coluna 
        :params status: int - valor de etapa da coluna
    """
    async with Connection() as connection:
      try:
        query = FluxoEtapa(id_usuario = user_id, fluxo_registro = flow, etapa_registro = status, fluxo_agendamento_consulta = 0, etapa_agendamento_consulta = 0, fluxo_agendamento_exame = 0, etapa_agendamento_exame = 0, lista_unidades = 0, fluxo_denuncia = 0)
        connection.add(query)
        await connection.flush()
        flow_dict = await connection.execute(select(FluxoEtapa).where(FluxoEtapa.id == query.id)).first()
        flow_dict = FluxoEtapa.as_dict(flow_dict)
        return flow_dict
      
      except Exception as error:
        message = "Erro ao inserir um novo fluxo no banco de dados"
        log = Logging(message)
        log.warning('insert_new_register_flow', None, error, 500, {'params': {'flow': flow, 'status': status}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

      finally:
        await connection.close()

  async def update_flow_from_user_id(self, id_usuario: int, table: str, input_data: int) -> Dict[str, FluxoEtapa]:
    """
      Atualiza uma coluna no banco de dados baseado no id do
      usuário informado

      :params id_usuario: int 
      :params table: str
      :params input_data: int
    """
    async with Connection() as connection:
     
      try:
        query = update(FluxoEtapa).where(FluxoEtapa.id_usuario == id_usuario).values({ table: input_data})
        connection.session.commit()
        
        query = connection.session.query(FluxoEtapa).filter(FluxoEtapa.id_usuario == id_usuario).one()
        result = await connection.execute(query)
        await connection.commit()
        flow_dict = await FluxoEtapa.as_dict(result.fetchone())
        return flow_dict 
      
      except Exception as error:
        message = "Erro ao atualizar os dados do usuário"
        log = Logging(message)
        log.warning('update_flow_from_user_id', None, error, 500, {'params': {'id_usuario':id_usuario, 'table': table, 'input_data': input_data}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

      finally:
        await connection.close()
  
  async def delete_flow_from_user_id(self, user_id: int) -> bool | None:
    """
      Delete uma linha da tabela fluxo_etapa baseado no id 
      informado

      params: user_id: int
    """
    async with Connection() as connection:
      try:
        await connection.execute(FluxoEtapa.delete()).where(FluxoEtapa.id == user_id)
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
        log.warning('delete_flow_from_user_id', None, error, 500, {'params': {'user_id': user_id,}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

      finally:
        await connection.close()
