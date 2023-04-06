from fastapi import HTTPException, status, Response

from ..configs.connection import Connection
from ..entities.user_model import Usuario
from log.logging import Logging
from sqlalchemy.orm.exc import NoResultFound 

class UserRepository:

  def select_all(self):
    with Connection() as connection:
      try:
        data = connection.session.query(Usuario).all()
        user_dict = str(data).replace(' ', '').split(',')
        user_dict = dict(i.split("=") for i in user_dict)
        return user_dict  
      
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

  def select_user_from_cellphone(self, cellphone):
    """
      Busca no banco de dados a linha de dados do usuário
      informado

        :params cellphone: int 
      return dict
    """
    with Connection() as connection:
      try:
        data = connection.session.query(Usuario).filter(Usuario.telefone == cellphone).one()
        user_dict = str(data).replace(' ', '').split(',')
        user_dict = dict(i.split("=") for i in user_dict)
        return user_dict
 
      except NoResultFound:
        message = f"Não foi possível resgatar o usuário de telefone {cellphone}"
        log = Logging(message)
        log.info()
        return {}
 
      except Exception as error:
        message = "Erro ao resgatar os dados do usuário"
        log = Logging(message)
        log.warning('select_user_from_cellphone', None, error, 500, {'params': {'cellphone': cellphone}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )
      

  def insert_new_user(self, telefone: int):
    """
      Inserta uma nova linha na tabela de usuarios 
        :params telefone: int 
      return dict
    """
    with Connection() as connection:
      try:
        data_insert = Usuario(telefone=telefone)
        connection.session.add(data_insert)
        connection.session.commit()
        user_dict = str(data_insert).replace(' ', '').split(',')
        user_dict = dict(i.split("=") for i in user_dict)
        return user_dict
        
      except Exception as error:
        message = "Erro ao inserir um novo usuário no banco de dados"
        log = Logging(message)
        log.warning('insert_new_user', None, error, 500, {'params': {'telefone': telefone}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message
        )

  def update_user_data(self, telefone, table, input_data):
    """
      Atualiza uma coluna no banco de dados baseado no id do
      usuário informado

      :params id_usuario: int 
      :params table: str
      :params input_data: int
    """
    with Connection() as connection:
      try:
        data_update = connection.session.query(Usuario).filter(Usuario.telefone == telefone).update({ table: input_data})
        connection.session.commit()
        return data_update  
      
      except Exception as error:
        message = "Erro ao atualizar um fluxo existente no banco de dados"
        log = Logging(message)
        log.warning('update_user_data', None, error, 500, {'params': {'telefone':telefone, 'table': table, 'input_data': input_data}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

  def delete(self, name):
    with Connection() as connection:
      connection.session.query(Usuario).filter(Usuario.name == name).delete()
      connection.session.commit()



