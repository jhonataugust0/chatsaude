from fastapi import HTTPException, status, Response
from ..configs.connection import Connection
from ..entities.especialidade_model import Especialidade
from api.log.logging import Logging
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

from sqlalchemy import select, MetaData, update, delete
from typing import List, Optional, Dict, Any

class EspecialidadeRepository:

  async def select_all(self) -> List[Dict[str, Especialidade]] | None:
    async with Connection() as connection:
      try:
        query = select(Especialidade)
        result = await connection.execute(query)
        rows = result.fetchall()
        return [await Especialidade.as_dict(rows) for rows in rows]
      
      except NoResultFound:
        message = f"Não foi possível resgatar as especialidades"
        log = Logging(message)
        log.info()
        return None

      except Exception as error:
        message = "Erro ao resgatar dados das especialidades"
        log = Logging(message)
        log.warning('select_all', None, error, 500, {'params': None})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )
      finally:
          await connection.close()

  async def select_specialty_from_name(self, name: str) -> Dict[str, Especialidade] | None:
    async with Connection() as connection:
      try:
        query = select(Especialidade.id, Especialidade.nome).where(
          Especialidade.nome == name, Especialidade.ativo == 1)
        result = await connection.execute(query)
        specialty_dict = await Especialidade.as_dict(result.scalar_one())
        return specialty_dict
      
      except NoResultFound:
        message = f"Não foi possível resgatar a especialidade de nome {name}"
        log = Logging(message)
        log.info()
        return None 
        
      except Exception as error:
        message = f"Erro ao resgatar dados da especialidade {name}"
        log = Logging(message)
        log.warning('select_specialty_from_name', None, error, 500, {'name': name})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )
      
      finally:
          await connection.close()

  async def select_specialty_from_id(self, id: int) -> Dict[str, Especialidade] | None:
    async with Connection() as connection:
      try:
        query = select(Especialidade.id, Especialidade.nome).where(
          Especialidade.id == id, Especialidade.ativo == 1)
        result = await connection.execute(query)
        specialty_dict = await Especialidade.as_dict(result.scalar_one())
        return specialty_dict
      
      except NoResultFound:
        message = f"Não foi possível resgatar a especialidade de nome {id}"
        log = Logging(message)
        log.info()
        return None
        
      except Exception as error:
        message = f"Erro ao resgatar dados da especialidade {id}"
        log = Logging(message)
        log.warning('select_specialty_from_id', None, error, 500, {'id': id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

      finally:
          await connection.close()

  async def insert_new_specialty(self, name) -> Dict[str, Especialidade] | None:
    async with Connection() as connection:
      try:  
        query = Especialidade(name = name)
        connection.add(query)
        connection.flush()
      
      except Exception as error:
        message = "Erro ao inserir um novo usuário no banco de dados"
        log = Logging(message)
        log.warning('insert_new_specialty', None, error, 500, {'params': {'name': name}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message
        )

      finally:
          await connection.close()
  
  async def update_specialty_data(self, name, table, input_data) -> Dict[str, Especialidade] | None:
    async with Connection() as connection:
      try:  
        query = update(Especialidade).where(Especialidade.name == name).values({ table: input_data })
        result = await connection.execute(query)
        await connection.commit()
        specialty_dict = await Especialidade.as_dict(result.fetchone())
        return specialty_dict

      except NoResultFound:
        message = f"Não foi possível a especialidade de nome {name}"
        log = Logging(message)
        log.info()
        return None
      
      except Exception as error:
        message = "Erro ao atualizar um fluxo existente no banco de dados"
        log = Logging(message)
        log.warning('update_specialty_data', None, error, 500, {'params': {'name':name, 'table': table, 'input_data': input_data}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )
      
      finally:
          await connection.close()
  
  async def delete_specialty(self, name) -> bool | None:
    async with Connection() as connection:
      try:  
        await connection.execute(Especialidade.delete()).where(Especialidade.name == name)
        await connection.session.commit()
        return True
      
      except NoResultFound:
          message = f"Não foi possível encontrar a especialdiade com nome {name}"
          log = Logging(message)
          log.info()
          return None
        
      except Exception as error:
        message = f"Erro ao excluir a especialdiade com nome {name}"
        log = Logging(message)
        log.warning('delete_specialty', None, error, 500, {'params': {'name': name}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )
      
      finally:
          await connection.close()    


