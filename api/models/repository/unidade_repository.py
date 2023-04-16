from fastapi import HTTPException, status, Response

from api.log.logging import Logging
from api.models.entities.unidade_model import Unidade
from ..configs.connection import Connection
from ..entities.unidade_model import Unidade
from sqlalchemy.orm.exc import NoResultFound 

from sqlalchemy import select, MetaData, update, delete

from typing import List, Optional, Dict, Any

class UnidadeRepository:

  async def select_all(self) -> List[Dict[str, Unidade]] | None:
    async with Connection() as connection:
      try:
        query = select(Unidade)
        result = await connection.execute(query)
        rows = result.fetchall()
        return [await Unidade.as_dict(row) for row in rows]
      
      except NoResultFound:
        message = f"Não foi possível resgatar as unidades"
        log = Logging(message)
        log.info()
        return None
        
      except Exception as error:
        message = "Erro ao resgatar as unidades"
        log = Logging(message)
        log.warning('select_all', None, error, 500, {'params': None})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )
      
      finally:
        await connection.close()

  async def select_unity_from_id(self, unity_id) -> Dict[str, Unidade] | None:
    """
      Busca no banco de dados a linha de dados da unidade do
      id informado

      :params unity_id: int 
    """
    async with Connection() as connection:
      try:
        query = select(Unidade).where(Unidade.id == unity_id)
        result = await connection.execute(query)
        user_dict = await Unidade.as_dict(result.scalar_one())
        return user_dict   

      except NoResultFound:
        message = f"Não foi possível encontrar a unidade {unity_id}"
        log = Logging(message)
        log.info()
        return None

      except Exception as error:
        message = f"Erro ao resgatar dados da unidade {unity_id}"
        log = Logging(message)
        log.warning('select_unity_from_id', None, error, 500, {'params': {'unity_id': unity_id}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )
      
      finally:
        await connection.close()

  async def select_unity_from_district(self, district) -> Dict[str, Unidade] | None:
    """
      Busca no banco de dados as unidades correspondentes ao
      bairro informado

      :params district: str 
      return dict
    """
    async with Connection() as connection:
      try:
        query = select(Unidade).where(Unidade.bairro == district)
        result = await connection.execute(query)
        user_dict = await Unidade.as_dict(result.scalar_one())
        return user_dict    
       
      except NoResultFound:
        message = f"Não foi possível encontrar a unidade do bairro {district}"
        log = Logging(message)
        log.info()
        return None

      except Exception as error:
        message = f"Erro ao resgatar dados da unidade {district}"
        log = Logging(message)
        log.warning('select_unity_from_district', None, error, 500, {'params': {'unity_id': district}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )
      
      finally:
        await connection.close()

  async def insert_new_unity(self, name: str) -> Dict[str, Unidade] | None:
    """
      Inserta uma nova linha na tabela de unidades  
        :params name: str
      return dict
    """
    async with Connection() as connection:
      try:
        query = Unidade(nome = name)
        connection.add(query)
        await connection.flush()
        unity_dict = await connection.execute(select(Unidade).where(Unidade.id == query.id)).first()
        user_dict = Unidade.as_dict(user_dict)
        return user_dict
      
      except Exception as error:
        message = "Erro ao inserir um novo agendamento no banco de dados"
        log = Logging(message)
        log.warning('insert_new_unity', None, error, 500, {'params': {'user_id': name}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

      finally:
          await connection.close()

  async def update_unity_from_id(self, unity_id: int, table: str, input_data: int) -> Dict[str, Unidade] | None:
    """
      Atualiza uma coluna no banco de dados baseado no id do
      usuário informado

      :params unity_id: int 
      :params table: str
      :params input_data: int
    """
    async with Connection() as connection:
      try:
        query = update(Unidade).where(Unidade.id == unity_id).values({ table: input_data})
        result = await connection.execute(query)
        await connection.commit()
        unity_dict = await Unidade.as_dict(result.fetchone())
        return unity_dict 
      
      except NoResultFound:
        message = f"Não foi possível resgatar a unidade de id {unity_id}"
        log = Logging(message)
        log.info()
        return None
      
      except Exception as error:
        message = "Erro ao atualizar os dados da unidade"
        log = Logging(message)
        log.warning('update_unity_from_id', None, error, 500, {'params': {'unity_id':unity_id, 'table': table, 'input_data': input_data}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

      finally:
          await connection.close()

  async def delete_unity_from_id(self, unity_id: int) -> bool | None:
    """
      Delete uma linha da tabela agendamentos baseado no id 
      do usuário informado

      params: unity_id: int
    """
    async with Connection() as connection:
      try:
        await connection.execute(Unidade.delete().where(Unidade.id == unity_id))
        await connection.commit()
        return True

      except NoResultFound:
        message = f"Não foi possível encontrar fluxos relacionados ao usuário {unity_id}"
        log = Logging(message)
        log.info()
        return None 
 
      except Exception as error:
        message = f"Erro ao excluir o agendamento do usuário {unity_id}"
        log = Logging(message)
        log.warning('delete_schedule_from_user_id', None, error, 500, {'params': {'unity_id': unity_id,}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

      finally:
          await connection.close()