import os
from typing import Any, Dict, List, Optional, Union
from fastapi import HTTPException, Response, status
from sqlalchemy import (MetaData, and_, delete, desc, select, text, tuple_,
                        update)
from sqlalchemy.orm.exc import NoResultFound

from api.log.logging import Logging

from .....models.configs.connection import Connection
from ..entity.agendamentos_model import Agendamentos
from ....health_unit.models.entity.unidade_model import Unidade
from ....user.models.entity.user_model import Usuario
from ....health_agents.models.entity.especialidade_model import Especialidade
from ....health_agents.models.repository.especialidade_repository import EspecialidadeRepository
from ....health_unit.models.repository.unidade_repository import UnidadeRepository


class AgendamentosRepository:

    async def select_all(self) -> List[Dict[str, Agendamentos]]:
        """
            Método responsável por resgatar todos os agendamentos
            registrados no banco

            :return: list
        """
        async with Connection() as connection:
            try:
                query = select(Agendamentos)
                result = await connection.execute(query)
                rows = result.fetchall()
                return [Agendamentos.as_dict(row) for row in rows]

            except NoResultFound as error:
                message = f"Não foi possível resgatar os agendamentos"
                log = await Logging(f"{message}\n" + f"{error}").info()
                return {}

            except Exception as error:
                message = "Erro ao resgatar dados de agendamento"
                log = Logging(message)
                await log.warning("select_all", None, error, 500, {"params": None})
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
                )

            finally:
                await connection.close()

    async def select_data_schedule_from_user_id(self, user_id: int) -> Dict[str, Agendamentos]:
        """
            Busca no banco de dados a linha de dados do agendamento
            pertencente ao usuário informado

            :params user_id: int
            return dict
        """
        async with Connection() as connection:
            try:
                query = (
                    select(Agendamentos)
                    .where(Agendamentos.id_usuario == user_id, Agendamentos.ativo == 1)
                    .order_by(desc(Agendamentos.id))
                    .limit(1)
                )
                result = await connection.execute(query)
                schedule_dict = Agendamentos.as_dict(result.scalar_one())
                return schedule_dict

            except NoResultFound:
                message = f"Não foi possível encontrar agendamentos relacionados ao usuário {user_id}"
                log = await Logging(message).info()
                return None

            except Exception as error:
                message = (
                    f"Erro ao resgatar dados de agendamento do usuário {user_id['id']}"
                )
                log = Logging(message)
                await log.warning(
                    "select_data_schedule_from_user_id",
                    None,
                    error,
                    500,
                    {"params": {"user_id": user_id}},
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
                )

            finally:
                await connection.close()

    async def select_all_data_from_schedule_with_id(self, id: int) -> Dict[str, Union[Agendamentos, Unidade, Especialidade]]:
        """
            Método responsável por resgatar todos os dados
            referente a um agendamento a fim de informá-los
            ao paciente

            :params id: int
            return dict
        """
        async with Connection() as connection:
            try:
                query = select(Agendamentos).where(Agendamentos.id == id)
                result = await connection.execute(query)
                schedule_data = Agendamentos.as_dict(result.scalar_one())

                unity_entity = UnidadeRepository()
                data_unity = await unity_entity.select_unity_from_id(
                    int(schedule_data["id_unidade"])
                )
                schedule_data["unity_info"] = data_unity

                specialty_entity = EspecialidadeRepository()
                data_specialty = await specialty_entity.select_specialty_from_id(
                    int(schedule_data["id_especialidade"])
                )
                schedule_data["specialty_info"] = data_specialty
                return schedule_data

            except NoResultFound:
                message = f"Não foi possível encontrar agendamentos relacionados ao usuário {id}"
                log = await Logging(message).info()
                return None

            except Exception as error:
                message = f"Erro ao resgatar dados de agendamento do usuário {id['id']}"
                log = Logging(message)
                await log.warning(
                    "select_all_data_from_schedule_with_id",
                    None,
                    error,
                    500,
                    {"params": {"id": id}},
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
                )

            finally:
                await connection.close()

    async def select_data_schedule_from_user_cellphone(self, cellphone: int) -> Dict[str, Agendamentos]:
        """
            Busca no banco de dados a linha de dados do agendamento
            pertencente ao usuário informado

            :params user_id: int
            return dict
        """
        async with Connection() as connection:
            try:
                query = (
                    select(Agendamentos, Usuario)
                    .join(Usuario, Agendamentos.id_usuario == Usuario.id)
                    .where(Usuario.telefone == cellphone)
                    .order_by(Agendamentos.id.desc())
                )
                result = await connection.execute(query)
                row = result.fetchone()
                schedule = Agendamentos.as_dict(row.Agendamentos)
                user_dict = Usuario.as_dict(row.Usuario)
                schedule["usuario_info"] = user_dict
                return schedule

            except NoResultFound:
                message = f"Não foi possível encontrar agendamentos relacionados ao usuário de telefone {cellphone}"
                log = await Logging(message).info()
                return None

            except Exception as error:
                message = f"Erro ao resgatar dados de agendamento do usuário de telefone {cellphone}"
                log = Logging(message)
                await log.warning(
                    "select_data_schedule_from_user_cellphone",
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

    async def insert_new_schedule_consult(self, user_id: int) -> Dict[str, Agendamentos]:
        """
        Inserta uma nova linha na tabela de agendamento
          :params user_id: int - id do usuário
          :params specialty: str - especialidade do agendamento
        """
        async with Connection() as connection:
            try:
                query = Agendamentos(
                    id_usuario=user_id, tipo_agendamento="Consulta", ativo=1
                )
                connection.add(query)
                await connection.commit()
                result_proxy = await connection.execute(
                    select(Agendamentos).where(Agendamentos.id == query.id)
                )
                schedule_dict = Agendamentos.as_dict(result_proxy.scalar_one())

                return schedule_dict

            except Exception as error:
                message = "Erro ao inserir um novo agendamento no banco de dados"
                log = Logging(message)
                await log.warning(
                    "insert_new_schedule_consult",
                    None,
                    error,
                    500,
                    {"params": {"user_id": user_id}},
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
                )

            finally:
                await connection.close()

    async def update_schedule_from_user_id(self, id_usuario: int, table: str, input_data: int) -> Dict[str, Agendamentos]:
        """
            Atualiza uma coluna no banco de dados baseado no id do
            usuário informado

            :params id_usuario: int
            :params table: str
            :params input_data: int
        """
        async with Connection() as connection:
            try:
                query = (
                    update(Agendamentos)
                    .where(
                        Agendamentos.id_usuario == id_usuario, Agendamentos.ativo == 1
                    )
                    .values({table: input_data})
                    .returning(Agendamentos.id)
                )
                result = await connection.execute(query)
                await connection.commit()
                schedule_id = result.scalar_one()
                result_proxy = await connection.execute(
                    select(Agendamentos).where(Agendamentos.id == schedule_id)
                )
                schedule_dict = Agendamentos.as_dict(result_proxy.scalar_one())
                return schedule_dict

            except NoResultFound:
                message = f"Não foi possível resgatar o agendamento do usuário de id {id_usuario}"
                log = await Logging(message).info()
                return None

            except Exception as error:
                message = "Erro ao atualizar os dados do usuário"
                log = Logging(message)
                await log.warning(
                    "update_schedule_from_user_id",
                    None,
                    error,
                    500,
                    {"params": {"id_usuario": id_usuario,"table": table,"input_data": input_data}}
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
                )

            finally:
                await connection.close()

    async def update_schedule_from_id(self, id: int, table: str, input_data: int) -> Dict[str, Agendamentos]:
        """
            Atualiza uma coluna no banco de dados baseado no id do
            usuário informado

            :params id: int
            :params table: str
            :params input_data: int
        """
        async with Connection() as connection:
            try:
                query = (
                    update(Agendamentos)
                    .where(Agendamentos.id == id, Agendamentos.ativo == 1)
                    .values({table: input_data})
                    .returning(Agendamentos.id)
                )
                result = await connection.execute(query)
                await connection.commit()
                schedule_id = result.scalar_one()

                result_proxy = await connection.execute(
                    select(Agendamentos).where(Agendamentos.id == schedule_id)
                )
                schedule_dict = Agendamentos.as_dict(result_proxy.scalar_one())
                return schedule_dict

            except NoResultFound:
                message = (
                    f"Não foi possível resgatar o agendamento do usuário de id {id}"
                )
                log = await Logging(message).info()
                return None

            except Exception as error:
                message = "Erro ao atualizar os dados do usuário"
                log = Logging(message)
                await log.warning(
                    "update_schedule_from_id",
                    None,
                    error,
                    500,
                    {"params": {"id": id, "table": table, "input_data": input_data}},
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
                )

            finally:
                await connection.close()

    async def delete_schedule_from_user_id(self, user_id: int) -> bool:
        """
            Delete uma linha da tabela agendamentos baseado no id
            do usuário informado

            params: user_id: int
        """
        async with Connection() as connection:
            try:
                await connection.execute(Agendamentos.delete()).where(
                    Agendamentos.id == user_id
                )
                await connection.commit()
                return True
            except NoResultFound:
                message = f"Não foi possível encontrar fluxos relacionados ao usuário {user_id}"
                log = await Logging(message).info()
                return None

            except Exception as error:
                message = f"Erro ao excluir o agendamento do usuário {user_id}"
                log = Logging(message)
                await log.warning(
                    "delete_schedule_from_user_id",
                    None,
                    error,
                    500,
                    {"params": {"user_id": user_id}}
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
                )

            finally:
                await connection.close()

    async def get_last_time_scheduele_from_specialty_id(self, specialty_id: int, unity_id: int) -> Dict[str, Agendamentos]:
        """
            Método responsável por consultar o banco a fim de
            retornar a a data e o horário da última consulta
            marcada para a especialidade e unidade que o pa-
            ciente está tentando marcar

            :params specialty_id: int
            :params unity_id: int
            :return: dict
        """
        async with Connection() as connection:
            try:
                columns = [
                    Agendamentos.data_agendamento,
                    Agendamentos.horario_termino_agendamento,
                ]

                query = (
                    select(
                        Agendamentos.data_agendamento,
                        Agendamentos.horario_termino_agendamento,
                    )
                    .where(
                        Agendamentos.id_especialidade == specialty_id,
                        Agendamentos.id_unidade == unity_id,
                        Agendamentos.data_agendamento != None,
                        Agendamentos.horario_termino_agendamento != None,
                    )
                    .order_by(Agendamentos.id.desc())
                )
                result = await connection.execute(query)
                keys = ["data_agendamento", "horario_termino_agendamento"]
                dict_result = [dict(zip(keys, values)) for values in result]
                return dict_result if len(dict_result) > 0 else None

            except NoResultFound:
                message = f"Não foi possível encontrar agendamentos com a especialidade de id {specialty_id} na unidade de id {unity_id}"
                log = await Logging(message).info()
                return None

            except Exception as error:
                message = f"Erro ao resgatar dados de agendamentos com a especialidade de id {specialty_id} na unidade de id {unity_id}"
                log = Logging(message)
                await log.warning(
                    "get_last_time_scheduele_from_specialty_id",
                    None,
                    error,
                    500,
                    {"params": {"specialty_id": specialty_id, "unity_id": unity_id}},
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
                )

            finally:
                await connection.close()

    async def check_conflicting_schedule(
        self,
        id_unity: int,
        id_specialty: int,
        date_schedule: str,
        init_time: str,
        end_time: str,
        id: int,
    ) -> bool:
        """
        Verificação de conflito de horários entre agendamentos
        na mesma unidade e especialidade

          :params id_unity: int
          :params id_specialty: int
          :params date_schedule: str
          :params init_time: str
          :params end_time: str
          :params id: int
          :return: bool
        """
        async with Connection() as connection:
            try:
                query = await connection.execute(
                    text(
                        f"""
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
                                DIA DATE := '{date_schedule}';
                                DT_INICIO TIME := '{init_time}';
                                DT_FINAL TIME := '{end_time}';
                            BEGIN
                                RETURN QUERY SELECT agen.id, agen.id_unidade, agen.id_especialidade, agen.data_agendamento, agen.horario_inicio_agendamento, agen.horario_termino_agendamento
                            FROM AGENDAMENTOS agen
                            WHERE (agen.ID_UNIDADE = {id_unity}) AND (agen.ID_ESPECIALIDADE = {id_specialty}) AND (DIA = agen.DATA_AGENDAMENTO) AND
                            (
                                ( DT_INICIO <= agen.HORARIO_INICIO_AGENDAMENTO AND DT_FINAL >= agen.HORARIO_INICIO_AGENDAMENTO )
                                OR (DT_INICIO >= agen.HORARIO_INICIO_AGENDAMENTO AND DT_FINAL <= agen.HORARIO_TERMINO_AGENDAMENTO)
                                OR (DT_INICIO < agen.HORARIO_TERMINO_AGENDAMENTO AND DT_FINAL >= agen.HORARIO_TERMINO_AGENDAMENTO)
                                OR (DT_INICIO <= agen.HORARIO_INICIO_AGENDAMENTO AND DT_FINAL >= agen.HORARIO_TERMINO_AGENDAMENTO)
                            );
                            END $$ LANGUAGE plpgsql;
                        """
                    )
                )
                query = await connection.execute(
                    text(f"SELECT * FROM busca_agendamentos();")
                )
                conflicts = query.fetchall()

                for conflito in conflicts:
                    message = f"Conflito ID = {conflito.id}"
                    await Logging(message).info()

                if len(conflicts) > 1:
                    return True

                if len(conflicts) == 1:
                    if conflicts[0].id == id:
                        return False
                    else:
                        return True
                else:
                    return False

            except Exception as error:
                message = f"Ao verificar a existência de conflitos"
                log = Logging(message)
                params = {
                    "id_unity": id_unity,
                    "id_specialty": id_specialty,
                    "date_schedule": date_schedule,
                    "init_time": init_time,
                    "end_time": end_time,
                }
                await log.warning(
                    "check_conflicting_schedule",
                    None,
                    error,
                    500,
                    {"params": {"params": params}},
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message
                )

            finally:
                await connection.close()
