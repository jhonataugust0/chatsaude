from fastapi import HTTPException, status, Response
from ..configs.connection import Connection
from ..entities.especialidade_model import Especialidade
from log.logging import Logging
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.exc import MultipleResultsFound

class EspecialidadeRepository:

  def select_all(self):
    with Connection() as connection:
      try:
        data = connection.session.query(Especialidade).all()
        specialty = str(data).replace(' ', '').split(',')
        specialty = dict(i.split("=") for i in specialty)
        return specialty
      
      except NoResultFound:
        message = f"Não foi possível resgatar as especialidades"
        log = Logging(message)
        log.info()
        return {}

      except Exception as error:
        message = "Erro ao resgatar dados das especialidades"
        log = Logging(message)
        log.warning('select_all', None, error, 500, {'params': None})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

  def select_specialty_from_name(self, name: str):
    with Connection() as connection:
      try:
        data = connection.session.query(Especialidade.id, Especialidade.nome).filter(Especialidade.nome == name, Especialidade.ativo == 1).first()
        specialty = str(data).replace(' ', '')
        columns = ['id', 'nome']
        data_specialty = dict(zip(columns, data))
        return data_specialty
      
      except NoResultFound:
        message = f"Não foi possível resgatar a especialidade de nome {name}"
        log = Logging(message)
        log.info()
        return {} 
        
      except Exception as error:
        message = f"Erro ao resgatar dados da especialidade {name}"
        log = Logging(message)
        log.warning('select_specialty_from_name', None, error, 500, {'name': name})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )
  
  def select_specialty_from_id(self, id: int):
    with Connection() as connection:
      try:
        data = connection.session.query(Especialidade.id, Especialidade.nome).filter(Especialidade.id == id, Especialidade.ativo == 1).first()
        specialty = str(data).replace(' ', '')
        columns = ['id', 'nome']
        data_specialty = dict(zip(columns, data))
        return data_specialty
      
      except NoResultFound:
        message = f"Não foi possível resgatar a especialidade de nome {id}"
        log = Logging(message)
        log.info()
        return {}
        
      except Exception as error:
        message = f"Erro ao resgatar dados da especialidade {id}"
        log = Logging(message)
        log.warning('select_specialty_from_id', None, error, 500, {'id': id})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=message
        )

  def insert(self, name):
    with Connection() as connection:
      data_insert = Especialidade(name = name)
      connection.session.add(data_insert)
      connection.session.commit()

  def update(self, name):
    with Connection() as connection:
      connection.session.query(Especialidade).filter(Especialidade.name == name).delete()
      connection.session.commit()

  def delete(self, name):
    with Connection() as connection:
      connection.session.query(Especialidade).filter(Especialidade.name == name).delete()
      connection.session.commit()



