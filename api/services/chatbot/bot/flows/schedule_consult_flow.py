from fastapi import HTTPException, Response, status
from api.services.chatbot.bot.replies import Replies
from api.services.chatbot.bot.validators.input_validator import Input_validator
from api.services.chatbot.utils.date import convert_to_datetime, format_date_for_user, format_time_for_user, get_more_forty_five

from api.services.health_unit.models.repository.unidade_repository import UnidadeRepository
from api.services.schedules.consult.models.repository.consulta_agendameno_repository import AgendamentoConsultaRepository

from .....log.logging import Logging
from ...utils.bot_utils import send_message
from api.services.user.models.repository.user_repository import UserRepository
from api.services.user_flow.models.repository.fluxo_etapa_repository import FluxoEtapaRepository
from api.services.health_agents.models.repository.especialidade_repository import EspecialidadeRepository



class ScheduleConsultFlow:
    def __init__(self, lang="br") -> None:
        self.lang = lang

    async def init_schedule_flow(self, user, message, flow_status):
        flow_entity = FluxoEtapaRepository()
        consult_flow_stage = await flow_entity.update_flow_from_user_id(
            user["id"], "etapa_agendamento_consulta", 1
        )
        return Response(
            status_code=status.HTTP_200_OK,
            content="Fluxo atualizado com sucesso",
        )

    async def load_unities(self, user, number_formated, message, flow_status):
        send_message("Escolha a unidade suportada mais próxima de você\nDigite o número correspondente ao da unidade desejada\nEx: 1", number_formated)
        unities_entity = UnidadeRepository()
        unities = await unities_entity.select_all()
        for i in unities:
            unities_text = f"""Unidade {i['id']}: {i['nome'].split('(')[0]}\nEndereço: {i['endereco'].replace(',','').split('s/n')[0]}\nBairro: {i['bairro']}\nHorario de funcionamento: {i['horario_funcionamento']}"""
            #await send_message(unities_text, number_formated)

        return Response(
            status_code=status.HTTP_200_OK,
            content="Mensagem enviada com sucesso",
        )

    async def get_last_time_schedule(self, user, number_formated, message, flow_status):
        consult_entity = AgendamentoConsultaRepository()
        data_schedule = (
            await consult_entity.select_data_schedule_from_user_cellphone(
                int(user["telefone"])
            )
        )
        last_time = (
            await consult_entity.get_last_time_scheduele_from_specialty_id(
                int(data_schedule["id_especialidade"]),
                int(data_schedule["id_unidade"]),
            )
        )
        if data_schedule["id_unidade"] and last_time:
            data = await format_date_for_user(last_time[-1]["data_agendamento"])
            hora = await format_time_for_user(
                last_time[-1]["horario_termino_agendamento"]
            )
            #await send_message(
            #     f"""Digite o dia que você deseja realizar a consulta\nEx: 24/12/2023\nAtenção, para essa especialidade somente temos horários a partir do dia {data}, a partir das {hora}""",
            #     number_formated,
            # )
        # else:
            #await send_message(
            #     f"""Digite o dia que você deseja realizar a consulta\nEx: 24/12/2023""",
            #     number_formated,
            # )

        return Response(
            status_code=status.HTTP_200_OK,
            content="Mensagem enviada com sucesso",
        )

    async def send_request_time_schedule(self, user, number_formated, message, flow_status):
        # await send_message(
        #     "Digite o horário que deseja realizar a consulta (atente-se para o horário estar dentro do período de funcionamento da unidade escolhida)\nEx: 08:00",
        #     number_formated,
        # )
        pass
    async def send_request_necessity(self, user, number_formated, message, flow_status):
        # await send_message(
        #     "Opcional: Digite o que está sentindo ou a necessidade da consulta.\nDigite qualquer coisa para ignorar e concluir o agendamento",
        #     number_formated,
        # )
        pass
    async def check_conflict(self, message, user, number_formated, flow_status):
        consult_entity = AgendamentoConsultaRepository()
        data_schedule = (
            await consult_entity.select_data_schedule_from_user_cellphone(
                int(user["telefone"])
            )
        )
        if data_schedule['horario_inicio_agendamento'] != None:
            conflict = await consult_entity.check_conflicting_schedule(
                data_schedule["id_unidade"],
                data_schedule["id_especialidade"],
                data_schedule["data_agendamento"],
                str(message) + ":00",
                await get_more_forty_five(message),
                data_schedule["id"],
            )
            if conflict == False:
                return {'value': True, 'content': message}
            else:
                #await send_message(
                #     "Desculpe, esse horário está indisponível, por favor, informe um horário no mínimo superior ao informado anteriormente",
                #     number_formated,
                # )
                return {'value': False, 'content': None}
        return {'value': True, 'content': message}

    async def data_schedule_consult_update_flow(self, user: dict, message: str):
        """
        Método responsável por orquestrar os inputs do usuário
        para os métodos corretos das classes de fluxo para a
        execução de uma conversa com o chatbot.
        :params user: dict
        :params message: string
        """
        flow_entity = FluxoEtapaRepository()
        number_formated = f"whatsapp:+" + str(user["telefone"])
        flow_status = None

        try:
            user_flow = await flow_entity.select_stage_from_user_id(int(user["id"]))
            flow_status = user_flow["etapa_agendamento_consulta"] + 1

            functions = {
                0: ScheduleConsultFlow.init_schedule_flow,
                1: ScheduleConsultFlow.define_specialty_consult,
                2: ScheduleConsultFlow.define_unity_consult,
                3: ScheduleConsultFlow.define_date_consult,
                4: ScheduleConsultFlow.define_time_consult,
                5: ScheduleConsultFlow.define_necessity_consult,
            }

            validator = {
                3: Input_validator.validate_date_schedule,
                4: ScheduleConsultFlow.check_conflict
            }

            replies = {
                1: ScheduleConsultFlow.load_unities,
                2: ScheduleConsultFlow.get_last_time_schedule,
                3: ScheduleConsultFlow.send_request_time_schedule,
                4: ScheduleConsultFlow.send_request_necessity
            }

            function = functions.get(user_flow["etapa_agendamento_consulta"])
            response_function = replies.get(user_flow["etapa_agendamento_consulta"])
            validator = validator.get(user_flow["etapa_agendamento_consulta"])

            if validator:
                validated_value = await validator(self, message, user, number_formated, flow_status)
                if not validated_value['value']:
                    reply = "Por favor, digite um valor válido"
                    #await send_message(reply, number_formated)
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=reply
                    )
                else:
                    # Update user data
                    result = await function(self, user, validated_value['content'], flow_status)

            elif function:
                result = await function(self, user, message, flow_status)

            if response_function is not None:
                response = await response_function(self, user, number_formated, message, flow_status)

        except Exception as error:
            message_log = "Erro ao atualizar os dados do usuário no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "flow_registration",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": user}},
            )



    async def define_specialty_consult(self, user: dict, message: str, flow_status: int) -> Response | HTTPException:
        """
        Método responsável por definir a especialidade da con-
        sulta do usuário
          :params user: dict
          :params message: string
          :params flow_status: int
        """
        consult_entity = AgendamentoConsultaRepository()
        flow_entity = FluxoEtapaRepository()
        specialty_entity = EspecialidadeRepository()

        try:
            schedule_data = await consult_entity.select_data_schedule_from_user_id(user["id"])
            specialty_user_request = (
                await specialty_entity.select_specialty_from_name(message)
            )
            await flow_entity.update_flow_from_user_id(
                user["id"], "etapa_agendamento_consulta", flow_status
            )
            consult_data = await consult_entity.update_schedule_from_id(
                schedule_data["id"],
                "id_especialidade",
                specialty_user_request["id"],
            )
            return consult_data

        except Exception as error:
            message_log = "Erro ao registrar a especialidade da consulta no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "define_specialty_consult",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": user, 'flow_status': flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def define_unity_consult(self, user: dict, message: str, flow_status: int) -> Response | HTTPException:
        """
        Método responsável por definir unidade da consulta do
        usuário no banco de dados
          :params user: dict
          :params message: string
          :params flow_status: int
        """
        consult_entity = AgendamentoConsultaRepository()
        flow_entity = FluxoEtapaRepository()
        specialty_entity = EspecialidadeRepository()

        try:
            schedule_data = await consult_entity.select_data_schedule_from_user_id(user["id"])
            user_flow = await flow_entity.update_flow_from_user_id(
                user["id"], "etapa_agendamento_consulta", flow_status
            )
            consult_data = await consult_entity.update_schedule_from_id(
                schedule_data["id"], "id_unidade", int(message)
            )
            return consult_data

        except Exception as error:
            message_log = "Erro ao registrar a unidade da consulta no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "define_unity_consult",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": user, 'flow_status': flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def define_date_consult(self, user: dict, date: str, flow_status: int) -> Response | HTTPException:
        """
        Método responsável por definir a data da consulta do
        usuário no banco de dados
          :params user: dict
          :params message: string
          :params flow_status: int
        """
        consult_entity = AgendamentoConsultaRepository()
        flow_entity = FluxoEtapaRepository()
        specialty_entity = EspecialidadeRepository()

        try:
            schedule_data = await consult_entity.select_data_schedule_from_user_id(user["id"])
            user_flow = await flow_entity.update_flow_from_user_id(
                user["id"], "etapa_agendamento_consulta", flow_status
            )
            await consult_entity.update_schedule_from_id(
                schedule_data["id"], "data_agendamento", date
            )
            return Response(
                status_code=status.HTTP_200_OK,
                content="Data registrada com sucesso",
            )

        except Exception as error:
            message_log = "Erro ao registrar a data da consulta no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "define_date_consult",
                None,
                str(error),
                500,
                {"params": {"date": date, "user": user, 'flow_status': flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def define_time_consult(self, user: dict, message: str, flow_status: int) -> Response | HTTPException:
        """
        Método responsável por definir hora da consulta do
        usuário no banco de dados
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        consult_entity = AgendamentoConsultaRepository()
        flow_entity = FluxoEtapaRepository()
        specialty_entity = EspecialidadeRepository()
        try:
            schedule_data = await consult_entity.select_data_schedule_from_user_id(user["id"])
            user_flow = await flow_entity.update_flow_from_user_id(
                user["id"], "etapa_agendamento_consulta", flow_status
            )
            final_schedule = await get_more_forty_five(str(message))
            consult_data = await consult_entity.update_schedule_from_id(
                schedule_data["id"],
                "horario_inicio_agendamento",
                await convert_to_datetime(str(message) + ":00"),
            )
            consult_data = await consult_entity.update_schedule_from_id(
                schedule_data["id"],
                "horario_termino_agendamento",
                await convert_to_datetime(final_schedule),
            )
            return consult_data

        except Exception as error:
            message_log = "Erro ao registrar a hora da consulta no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "define_time_consult",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": user, 'flow_status': flow_status}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def define_necessity_consult(self, user: dict, message: str, flow_status: int) -> Response | HTTPException:
        """
        Método responsável por definir a necessidade da
        consulta do usuário no banco de dados
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        consult_entity = AgendamentoConsultaRepository()
        flow_entity = FluxoEtapaRepository()
        try:
            schedule_data = await consult_entity.select_data_schedule_from_user_id(user["id"])
            consult_data = await consult_entity.update_schedule_from_id(
                schedule_data["id"], "descricao_necessidade", str(message)
            )
            await ScheduleConsultFlow.finalize_schedule_flow(self, user, message, flow_status)
            return consult_data

        except Exception as error:
            message_log = "Erro ao registrar a necessidade do usuário no banco de dados!"
            log = Logging(message_log)
            await log.warning(
                "define_necessity_consult",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": user}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def finalize_schedule_flow(self, user: dict, message: str, flow_status: int) -> Response | HTTPException:
        """
        Método responsável por finalizar o fluxo de agendamento
            :params user: dict
            :params message: string
            :params flow_status: int
        """
        consult_entity = AgendamentoConsultaRepository()
        flow_entity = FluxoEtapaRepository()
        try:
            schedule_data = await consult_entity.select_data_schedule_from_user_id(user["id"])
            await flow_entity.update_flow_from_user_id(
                user["id"], "etapa_agendamento_consulta", 0
            )
            await flow_entity.update_flow_from_user_id(
                user["id"], "fluxo_agendamento_consulta", 0
            )
            all_data = await consult_entity.select_all_data_from_schedule_with_id(
                schedule_data["id"]
            )
            content = f"Que ótimo, você realizou seu agendamento!\nCompareça à unidade {all_data['unity_info']['nome']} no dia {await format_date_for_user(all_data['data_agendamento'])} as {await format_time_for_user(all_data['horario_inicio_agendamento'])} horas para a sua consulta com o {all_data['specialty_info']['nome']}"
            return #await send_message(content, f"whatsapp:+{user['telefone']}")
            return all_data

        except Exception as error:
            message_log = "Erro ao finalizar o fluxo de agendamento de consulta"
            log = Logging(message_log)
            await log.warning(
                "finalize_schedule_flow",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": user}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )
