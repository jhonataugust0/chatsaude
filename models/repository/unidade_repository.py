from fastapi import HTTPException, status, Response

from log.logging import Logging
from ..configs.connection import Connection
from ..entities.unidade_model import Unidade
from sqlalchemy.orm.exc import NoResultFound 

class UnidadeRepository:

  def select_all(self):
    with Connection() as connection:
      try:
        data = connection.session.query(Unidade).order_by(Unidade.id).all()
        data_unity = [u.__dict__ for u in data]

      except NoResultFound:
        message = f"Não foi possível resgatar as unidades"
        log = Logging(message)
        log.info()
        return {}
        
      except Exception as error:
        message = "Erro ao resgatar as unidades"
        log = Logging(message)
        log.warning('select_all', None, error, 500, {'params': None})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )
      return data_unity

  def select_unity_from_id(self, unity_id):
    """
      Busca no banco de dados a linha de dados da unidade do
      id informado

      :params unity_id: int 
    return dict
    """
    with Connection() as connection:
      try:
        data = connection.session.query(Unidade).filter(Unidade.id == unity_id).one()
        unity = Unidade.as_dict(data)
        return unity   

      except NoResultFound:
        message = f"Não foi possível encontrar a unidade {unity_id}"
        log = Logging(message)
        log.info()
        return {}

      except Exception as error:
        message = f"Erro ao resgatar dados da unidade {unity_id}"
        log = Logging(message)
        log.warning('select_unity_from_id', None, error, 500, {'params': {'unity_id': unity_id}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

  def select_unity_from_district(self, district):
    """
      Busca no banco de dados as unidades correspondentes ao
      bairro informado

      :params district: str 
      return dict
    """
    with Connection() as connection:
      try:
        data = connection.session.query(Unidade).filter(Unidade.bairro == district).all()
        
        data_unity = list()
        for i in range(0, len(data)):
          columns = ['id', 'nome', 'endereco', 'bairro', 'cidade', 'estado', 'cep', 'horario_funcionamento', 'contato']
          value = list(str(data[i]))
          data_unity.append({columns[j]: value[j] for j in range(0, len(columns))})

      except NoResultFound:
        message = f"Não foi possível encontrar a unidade do bairro {district}"
        log = Logging(message)
        log.info()
        return {}

      except Exception as error:
        message = f"Erro ao resgatar dados da unidade {district}"
        log = Logging(message)
        log.warning('select_unity_from_district', None, error, 500, {'params': {'unity_id': district}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

  def insert_new_unity(self, name: str):
    """
      Inserta uma nova linha na tabela de unidades  
        :params name: str
      return dict
    """
    with Connection() as connection:
      try:
        data_insert = Unidade(nome = name)
        connection.session.add(data_insert)
        connection.session.commit()
        schedule = str(data_insert).replace(' ', '').split(',')
        schedule = dict(i.split("=") for i in schedule)
        return schedule
      
      except Exception as error:
        message = "Erro ao inserir um novo agendamento no banco de dados"
        log = Logging(message)
        log.warning('insert_new_unity', None, error, 500, {'params': {'user_id': name}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

  def update_unity_from_id(self, unity_id: int, table: str, input_data: int):
    """
      Atualiza uma coluna no banco de dados baseado no id do
      usuário informado

      :params unity_id: int 
      :params table: str
      :params input_data: int
    """
    with Connection() as connection:
      try:
        data_update = connection.session.query(Unidade).filter(Unidade.id == unity_id).update({ table: input_data})
        connection.session.commit()
        return data_update  
      
      except Exception as error:
        message = "Erro ao atualizar os dados da unidade"
        log = Logging(message)
        log.warning('update_unity_from_id', None, error, 500, {'params': {'unity_id':unity_id, 'table': table, 'input_data': input_data}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

  def delete_unity_from_id(self, unity_id: int):
    """
      Delete uma linha da tabela agendamentos baseado no id 
      do usuário informado

      params: unity_id: int
    """
    with Connection() as connection:
      try:
        connection.session.query(Unidade).filter(Unidade.id == unity_id).delete()
        connection.session.commit()
        
      except NoResultFound:
        message = f"Não foi possível encontrar fluxos relacionados ao usuário {unity_id}"
        log = Logging(message)
        log.info()
        return {} 
 
      except Exception as error:
        message = f"Erro ao excluir o agendamento do usuário {unity_id}"
        log = Logging(message)
        log.warning('delete_schedule_from_user_id', None, error, 500, {'params': {'unity_id': unity_id,}})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )



