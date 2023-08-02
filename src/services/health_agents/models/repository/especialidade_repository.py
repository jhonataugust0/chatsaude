import os
from typing import Any, Dict, List, Optional
from fastapi import HTTPException, Response, status
from sqlalchemy import MetaData, delete, select, update
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from log.logging import Logging

from models.configs.connection import Connection
from services.health_agents.models.entity.especialidade_model import Especialidade

class EspecialidadeRepository:
    def __init__(self):
        self.connection_url = os.environ.get('CONNECTION_URL')

    async def select_all(self) -> List[Dict[str, Especialidade]]:
        """
            Método que resgata todas as especialidades regis-
            tradas no banco

            :return: list
        """
        async with Connection(connection_url=self.connection_url) as connection:
            try:
                query = select(Especialidade)
                result = await connection.execute(query)
                rows = result.fetchall()
                return [Especialidade.as_dict(rows) for rows in rows]

            except NoResultFound:
                message = f"Não foi possível resgatar as especialidades"
                log = await Logging(message).info()
                return None

            except Exception as error:
                message = "Erro ao resgatar dados das especialidades"
                log = Logging(message)
                await log.warning("select_all", None, error, 500, {"params": None})
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
                )

            finally:
                await connection.close()


    async def select_specialty_from_name(self, name: str) -> Dict[str, Especialidade]:
        """
            Método responsável por resgatar os dados de uma
            especialidade através do seu nome

            :param name: str
            :return: dict
        """
        async with Connection(connection_url=self.connection_url) as connection:
            try:
                query = (
                    select(Especialidade)
                    .where(Especialidade.nome == name, Especialidade.ativo == 1)
                    .limit(1)
                )
                result = await connection.execute(query)
                specialty = result.scalar_one()
                specialty_dict = Especialidade.as_dict(specialty)
                return specialty_dict

            except NoResultFound as error:
                message = f"Não foi possível resgatar a especialidade de nome {name}"
                log = await Logging(message).info()
                return None

            except MultipleResultsFound as error:
                raise HTTPException(
                    status_code=500, detail="Mais de uma especialidade encontrada."
                )

            except Exception as error:
                message = f"Erro ao resgatar dados da especialidade {name}"
                log = Logging(message)
                await log.warning(
                    "select_specialty_from_name", None, error, 500, {"name": name}
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
                )
            finally:
                await connection.close()


    async def select_specialty_from_id(self, id: int) -> Dict[str, Especialidade]:
        async with Connection(connection_url=self.connection_url) as connection:
            """
                Método responsável por resgatar os dados de
                uma especialidade através do seu id

                :params id: int
                :return: dict
            """
            try:
                query = select(Especialidade).where(
                    Especialidade.id == id, Especialidade.ativo == 1
                )
                result = await connection.execute(query)
                specialty_dict = Especialidade.as_dict(result.scalar_one())
                return specialty_dict

            except NoResultFound:
                message = f"Não foi possível resgatar a especialidade de nome {id}"
                log = await Logging(message).info()
                return None

            except Exception as error:
                message = f"Erro ao resgatar dados da especialidade {id}"
                log = Logging(message)
                await log.warning("select_specialty_from_id", None, error, 500, {"id": id})
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
                )
            finally:
                await connection.close()


    async def insert_new_specialty(self, name) -> Dict[str, Especialidade]:
        """
            Método responsável por insertar uma nova especialidade

            :params name: str
            :return: dict
        """
        async with Connection(connection_url=self.connection_url) as connection:
            try:
                query = Especialidade(name=name)
                connection.add(query)
                connection.commit()

                result_proxy = await connection.execute(
                    select(Especialidade).where(Especialidade.id == query.id)
                )
                specialty_dict = Especialidade.as_dict(result_proxy.scalar_one())

                return specialty_dict

            except Exception as error:
                message = "Erro ao inserir um novo usuário no banco de dados"
                log = Logging(message)
                await log.warning(
                    "insert_new_specialty", None, error, 500, {"params": {"name": name}}
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
                )
            finally:
                await connection.close()


    async def update_specialty_data(self, name, table, input_data) -> Dict[str, Especialidade]:
        """
            Método responsável por atualizar os dados de uma
            especialidade através do seu nome

            :param name: str
            :param table: str
            :param input_data: str
            :return: dict
        """
        async with Connection(connection_url=self.connection_url) as connection:
            try:
                query = (
                    update(Especialidade)
                    .where(Especialidade.name == name)
                    .values({table: input_data})
                    .returning(Especialidade.id)
                )
                result = await connection.execute(query)
                await connection.commit()
                specialty_id = result.scalar_one()

                result_proxy = await connection.execute(
                    select(Especialidade).where(Especialidade.id == specialty_id)
                )
                specialty_dict = Especialidade.as_dict(result_proxy.scalar_one())
                return specialty_dict

            except NoResultFound:
                message = f"Não foi possível a especialidade de nome {name}"
                log = await Logging(message).info()
                return None

            except Exception as error:
                message = "Erro ao atualizar um fluxo existente no banco de dados"
                log = Logging(message)
                await log.warning(
                    "update_specialty_data",
                    None,
                    error,
                    500,
                    {"params": {"name": name, "table": table, "input_data": input_data}}
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
                )
            finally:
                await connection.close()


    async def delete_specialty(self, name) -> bool:
        """
            Método responsável por excluir uma especialidade pelo seu nome

            :params name: str
            :return: bool
        """
        async with Connection(connection_url=self.connection_url) as connection:
            try:
                await connection.execute(Especialidade.delete()).where(
                    Especialidade.name == name
                )
                await connection.session.commit()
                return True

            except NoResultFound:
                message = f"Não foi possível encontrar a especialdiade com nome {name}"
                log = await Logging(message).info()
                return None

            except Exception as error:
                message = f"Erro ao excluir a especialdiade com nome {name}"
                log = Logging(message)
                await log.warning(
                    "delete_specialty", None, error, 500, {"params": {"name": name}}
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
                )
            finally:
                await connection.close()

