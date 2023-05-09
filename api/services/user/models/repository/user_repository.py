import os
from typing import Any, Dict, List, Optional
from fastapi import HTTPException, Response, status
from sqlalchemy import MetaData, delete, insert, select, update
from sqlalchemy.orm.exc import NoResultFound

from api.log.logging import Logging
from api.services.user.models.entity.user_model import Usuario

from .....models.configs.connection import Connection
from ..entity.user_model import Usuario


class UserRepository:
    def __init__(self):
        self.connection_url = os.environ.get('CONNECTION_URL')

    async def select_all(self) -> List[Dict[str, Usuario]]:
        """
            Método que retorna todos os usuários do banco de
            dados
        """
        async with Connection(connection_url=self.connection_url) as connection:
            try:
                query = select(Usuario)
                result = await connection.execute(query)
                rows = result.fetchall()
                return [Usuario.as_dict(row) for row in rows]

            except NoResultFound:
                message = f"Não foi possível resgatar os usuários"
                log = await Logging(message).info()
                return {}

            except Exception as error:
                message = "Erro ao resgatar os dados dos usuários"
                log = Logging(message)
                await log.warning(
                    "select_all",
                    None,
                    error,
                    500,
                    None
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
                )

            finally:
                await connection.close()

    async def select_user_from_cellphone(self, cellphone) -> Dict[str, Usuario]:
        """
        Busca no banco a linha de dados do usuário informado
          :params cellphone: int
        """
        async with Connection(connection_url=self.connection_url) as connection:
            try:
                query = select(Usuario).where(Usuario.telefone == cellphone)
                result = await connection.execute(query)
                user_dict = Usuario.as_dict(result.scalar_one())
                return user_dict

            except NoResultFound:
                message = f"Não foi possível resgatar o usuário de telefone {cellphone}"
                await Logging(message).info()
                return {}

            except Exception as error:
                message = "Erro ao resgatar os dados do usuário"
                log = Logging(message)
                await log.warning(
                    "select_user_from_cellphone",
                    None,
                    error,
                    500,
                    {"params": {"cellphone": cellphone}},
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
                )

            finally:
                await connection.close()

    async def insert_new_user(self, telefone: int) -> Dict[str, Usuario]:
        """
        Inserta uma nova linha na tabela de usuarios
          :params telefone: int
        """
        async with Connection(connection_url=self.connection_url) as connection:
            try:
                query = Usuario(telefone=telefone)
                connection.add(query)
                await connection.commit()

                result_proxy = await connection.execute(
                    select(Usuario).where(Usuario.id == query.id)
                )
                user_dict = Usuario.as_dict(result_proxy.scalar_one())

                return user_dict

            except Exception as error:
                message = "Erro ao inserir um novo usuário no banco de dados"
                log = Logging(message)
                await log.warning(
                    "insert_new_user",
                    None,
                    error,
                    500,
                    {"params": {"telefone": telefone}},
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
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
        async with Connection(connection_url=self.connection_url) as connection:
            try:
                query = (
                    update(Usuario)
                    .where(Usuario.telefone == telefone)
                    .values({table: input_data})
                    .returning(Usuario.id)
                )
                result = await connection.execute(query)
                await connection.commit()
                user_id = result.scalar_one()

                result_proxy = await connection.execute(
                    select(Usuario).where(Usuario.id == user_id)
                )
                user_dict = Usuario.as_dict(result_proxy.scalar_one())
                return user_dict

            except NoResultFound:
                message = f"Não foi possível resgatar o usuário de telefone {telefone}"
                log = await Logging(message).info()
                return {}

            except Exception as error:
                message = "Erro ao atualizar um fluxo existente no banco de dados"
                log = Logging(message)
                await log.warning(
                    "update_user_data",
                    None,
                    error,
                    500,
                    {"params": {"telefone": telefone,"table": table, "input_data": input_data}}
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
                )

            finally:
                await connection.close()

    async def delete(self, cellphone) -> bool:
        async with Connection(connection_url=self.connection_url) as connection:
            try:
                await connection.execute(
                    Usuario.delete().where(Usuario.telefone == cellphone)
                )
                await connection.commit()
                return True

            except NoResultFound:
                message = f"Não foi possível encontrar o usuário com nome {cellphone}"
                log = await Logging(message).info()
                return {}

            except Exception as error:
                message = f"Erro ao excluir o usuário com nome {cellphone}"
                log = Logging(message)
                await log.warning(
                    "delete", None, error, 500, {"params": {"cellphone": cellphone}}
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
                )

            finally:
                await connection.close()
