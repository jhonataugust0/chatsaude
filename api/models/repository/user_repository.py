from fastapi import HTTPException, status, Response

from ..configs.connection import Connection
from ..entities.user_model import Usuario
from api.log.logging import Logging
from api.models.entities.user_model import Usuario
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import select, MetaData, update, delete

from typing import List, Optional, Dict, Any


class UserRepository:
          
  async def select_all(self) -> List[Dict[str, Any]]:
    async with Connection() as connection:
      try:
        query = select(Usuario)
        result = await connection.execute(query)
        rows = result.fetchall()
        return [await Usuario.as_dict(row) for row in rows]
      
      except NoResultFound:
        message = f"Não foi possível resgatar os usuários"
        log = Logging(message)
        log.info()
        return {}
      
      except Exception as error:
        message = "Erro ao resgatar os dados dos usuários"
        log = Logging(message)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )
      
      finally:
        await connection.close()

  async def select_user_from_cellphone(self, cellphone) -> Dict[str, Usuario]:
    """
      Busca no banco a linha de dados do usuário informado
        :params cellphone: int 
    """
    async with Connection() as connection:
      try:
        query = select(Usuario).where(Usuario.telefone == cellphone)
        result = await connection.execute(query)
        user_dict = await Usuario.as_dict(result.scalar_one())
        return user_dict
 
      except NoResultFound:
        message = f"Não foi possível resgatar o usuário de telefone {cellphone}"
        log = Logging(message)
        log.info()
        return None

      except Exception as error:
        message = "Erro ao resgatar os dados do usuário"
        log = Logging(message)
        log.warning('select_user_from_cellphone', None, error, 500, {'params': {'cellphone': cellphone}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message
        )
      
      finally:
        await connection.close()

  async def insert_new_user(self, telefone: int) -> Dict[str, Usuario]:
    """
      Inserta uma nova linha na tabela de usuarios 
        :params telefone: int 
    """
    async with Connection() as connection:
      try:
        query = Usuario(telefone=telefone)
        connection.add(query)
        await connection.commit()
        user_dict = await Usuario.as_dict(query)
        return user_dict
        
      except Exception as error:
        message = "Erro ao inserir um novo usuário no banco de dados"
        log = Logging(message)
        log.warning('insert_new_user', None, error, 500, {'params': {'telefone': telefone}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message
        )
      
      finally:
          await connection.close()
  
  async def update_user_data(self, telefone, table, input_data) -> Dict[str, Usuario]:
    """
      Atualiza uma coluna no banco de dados baseado no id do
      usuário informado

      :params id_usuario: int 
      :params table: str
      :params input_data: int
    """
    async with Connection() as connection:
      try:
        query = update(Usuario).where(Usuario.telefone == telefone).values({ table: input_data })
        result = await connection.execute(query)
        await connection.commit()
        user_dict = await Usuario.as_dict(result.fetchone())
        return user_dict
      
      except NoResultFound:
        message = f"Não foi possível resgatar o usuário de telefone {telefone}"
        log = Logging(message)
        log.info()
        return None
      
      except Exception as error:
        message = "Erro ao atualizar um fluxo existente no banco de dados"
        log = Logging(message)
        log.warning('update_user_data', None, error, 500, {'params': {'telefone':telefone, 'table': table, 'input_data': input_data}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )
      
      finally:
          await connection.close()

  async def delete(self, cellphone):
    async with Connection() as connection:
        try:
          await connection.execute(Usuario.delete().where(Usuario.telefone == cellphone))
          await connection.commit()
        
        except NoResultFound:
          message = f"Não foi possível encontrar o usuário com nome {cellphone}"
          log = Logging(message)
          log.info()
          return {'message': message, 'value': None}
        
        except Exception as error:
          message = f"Erro ao excluir o usuário com nome {cellphone}"
          log = Logging(message)
          log.warning('delete', None, error, 500, {'params': {'cellphone': cellphone}})
          raise HTTPException(
              status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
              detail=message
          )
        
        finally:
          await connection.close()



