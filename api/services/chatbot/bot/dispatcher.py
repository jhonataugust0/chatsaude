from time import sleep
from ..bot.replies import Replies
from api.log.logging import Logging
from datetime import time as time_type
from datetime import date as date_type
from ..bot.Bot_options import BotOptions
from fastapi import HTTPException, Response, status
from ..bot.flows.register_user_flow import Register_user_flow
from ..bot.flows.schedule_consult_flow import ScheduleConsultFlow

from ...schedules.consult.models.repository.consulta_agendameno_repository import (
    AgendamentoConsultaRepository,
)
from ...schedules.exam.models.repository.exame_gendameno_repository import (
    AgendamentoExameRepository,
)
from api.services.user_flow.models.repository.fluxo_etapa_repository import (
    FluxoEtapaRepository,
)
from api.services.health_unit.models.repository.unidade_repository import (
    UnidadeRepository,
)
from api.services.user.models.repository.user_repository import UserRepository
from ..utils.bot_utils import send_message

from .validators.document_validator import Document_validator
from .validators.input_validator import Input_validator

from ..utils.date import (
    convert_to_datetime,
    format_date_for_user,
    format_time_for_user,
    get_more_forty_five,
)

class BotDispatcher:
    def __init__(self, lang="br") -> None:
        self.lang = lang

    def get_prompt(self, current_step: int, next_step: int) -> str:
        """
        Retorna a mensagem para ser enviada ao usuário.
        :param current_step: Etapa atual da conversa
        :param next_step: Próxima etapa da conversa
        :return: Mensagem a ser enviada ao usuário
        """
        if current_step == 1:
            if next_step == 2:
                return "Digite seu melhor email\nEx:maria.fatima@gmail.com"
        elif current_step == 2:
            if next_step == 3:
                return "Digite sua data de nascimento\nEx:12/12/1997"
        elif current_step == 3:
            if next_step == 4:
                return "Digite seu CEP\nEx:56378-921"
        elif current_step == 4:
            if next_step == 5:
                return "Confirme as informações abaixo:\nNome: {nome}\nEmail: {email}\nData de nascimento: {data_nascimento}\nCEP: {cep}\nPara confirmar, digite 'sim'. Caso deseje corrigir alguma informação, digite 'nao' e siga as instruções."
        return ""

    async def schedule_consult_trigger(self, verify_stage_user, cellphone):
        if "fluxo_agendamento_consulta" in verify_stage_user and (
                verify_stage_user["fluxo_agendamento_consulta"] == None
                or verify_stage_user["fluxo_agendamento_consulta"] < 1
            ):
            await send_message(str(Replies.SCHEDULE_CONSULT), f"whatsapp:{str(cellphone)}")
            return {"schedule_consult_trigger": 1}


    async def schedule_exam_trigger(self, verify_stage_user, cellphone):
        if ("fluxo_agendamento_exame" in verify_stage_user and (
                verify_stage_user["fluxo_agendamento_exame"] == None
                or verify_stage_user["fluxo_agendamento_exame"] < 1
            )
        ):
            await send_message(str(Replies.SCHEDULE_EXAM), f"whatsapp:{str(cellphone)}")
            return {
                "message": str(Replies.SCHEDULE_EXAM),
                "schedule_exam_trigger": 1,
            }


    async def make_report_trigger(self):
        return {"message": str(Replies.REPORT), "make_report_trigger": 1}


    async def register_user_trigger(self, user_dict, cellphone):
        if "id" not in user_dict:
            await send_message(str(Replies.INIT_REGISTER_FLOW), f"whatsapp:{str(cellphone)}")
            return {"register_user_trigger": 1}


    async def default_reply(self, verify_stage_user):
        if (
            (
                verify_stage_user["fluxo_agendamento_consulta"] == None
                or verify_stage_user["fluxo_agendamento_consulta"] == 0
            )
            and (
                verify_stage_user["fluxo_agendamento_exame"] == None
                or verify_stage_user["fluxo_agendamento_exame"] == 0
            )
            and (
                verify_stage_user["fluxo_agendamento_exame"] == None
                or verify_stage_user["fluxo_agendamento_exame"] == 0
            )
        ):
            return {"message": str(Replies.DEFAULT)}


    async def default_new_user_reply(self, user_dict):
        if "id" not in user_dict or user_dict["id"] == None:
            return {"message": str(Replies.DEFAULT_NEW_USER)}
        else:
            return {}

    async def message_processor(self, message: str, cellphone: int, user_dict: dict = None) -> dict[str]:
        """
        Método que processa as inputs do usuário, identificando-as e atribuindo as
        mesmas seus respectivos gatilhos para a continuidade do fluxo da aplicação.
        :params message: str
        :params cellphone: int
        return dict | Response: Response
        """
        try:
            if user_dict is not None and user_dict.get("telefone") is not None:
                flow_entity = FluxoEtapaRepository()
                verify_stage_user = await flow_entity.select_stage_from_user_id(user_dict["id"])

                if message == BotOptions.SCHEDULE_CONSULT:
                    response = await self.schedule_consult_trigger(verify_stage_user, cellphone)

                elif message == BotOptions.SCHEDULE_EXAM:
                    response = await self.schedule_exam_trigger(verify_stage_user, cellphone)

                elif message == BotOptions.MAKE_REPORT:
                    response = await self.make_report_trigger()

                else:
                    response = await self.default_reply(verify_stage_user)

            elif message == BotOptions.REGISTER_USER:
                response = await self.register_user_trigger(user_dict, cellphone)

            else:
                response = await self.default_new_user_reply(user_dict)

            return response

        except Exception as error:
            message_log = f"Erro ao processar a input do usuário {message}"
            log = Logging(message_log)
            await log.warning(
                "message_processor",
                None,
                str(error),
                500,
                {"params": {"message": message, "cellphone": cellphone}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def trigger_processing(
        self, bot_response: dict, number: int, user: dict = None
    ) -> Response:
        try:
            user_entity = UserRepository()
            register_flow = Register_user_flow()
            stage_entity = FluxoEtapaRepository()
            schedule_consult_entity = AgendamentoConsultaRepository()
            schedule_exam_entity = AgendamentoExameRepository()

            trigger_actions = {
                "register_user_trigger": {
                    "action": [
                        lambda: register_flow.insert_user_and_flow(number)
                        ],
                    "message": "Usuário inserido com sucesso",
                },
                "schedule_consult_trigger": {
                    "action": [
                        lambda: stage_entity.update_flow_from_user_id(user["id"], "fluxo_agendamento_consulta", 1),
                        lambda: stage_entity.update_flow_from_user_id(user["id"], "etapa_agendamento_consulta", 0),
                        lambda: schedule_consult_entity.insert_new_schedule_consult(user["id"])
                    ],
                    "message": "Agendamento de consulta iniciado com sucesso",
                },
                "schedule_exam_trigger": {
                    "action": [
                        lambda: stage_entity.update_flow_from_user_id(user["id"], "fluxo_agendamento_exame", 1),
                        lambda: stage_entity.update_flow_from_user_id(user["id"], "etapa_agendamento_exame", 0),
                        lambda: schedule_exam_entity.insert_new_schedule_exam(user["id"])
                    ],
                    "message": "Agendamento de exame iniciado com sucesso",
                },
                # "make_report_trigger": {
                #     "action": lambda: await schedule_consult_entity.make_report(user, report_entity),
                #     "message": "Relatório gerado com sucesso",
                # },
            }

            if bot_response is not None:
                for trigger in bot_response:
                    if trigger in trigger_actions and bot_response[trigger] == 1:
                        for func in trigger_actions[trigger]["action"]:
                            await func()

                        return Response(
                            status_code=status.HTTP_200_OK,
                            content=trigger_actions[trigger]["message"],
                        )

        except Exception as error:
            message_log = f"Erro ao processar os gatilhos {bot_response}"
            log = Logging(message_log)
            await log.warning(
                "trigger_processing",
                None,
                str(error),
                500,
                {"params": {"number": number, "bot_response": bot_response}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def data_users_update_flow(self, user: dict, message: str):
        """
        Método responsável por orquestar os inputs do usuário
        para os métodos corretos das classes de fluxo para a
        execução de uma conversa com o chatbot.
        :params user: dict
        :params message: string
        """
        flow_entity = FluxoEtapaRepository()
        register_flow = Register_user_flow()
        number_formated = f"whatsapp:+" + str(user["telefone"])
        flow_status = None

        try:
            user_flow = await flow_entity.select_stage_from_user_id(int(user["id"]))
            flow_status = user_flow["etapa_registro"] + 1

            flows = {
                1: register_flow.define_user_name,
                2: register_flow.define_user_email,
                3: register_flow.define_user_nascent_date,
                4: register_flow.define_user_cep,
                5: register_flow.define_user_cpf,
                6: register_flow.define_user_rg,
                7: register_flow.define_user_cns,
                8: register_flow.define_user_district,
            }

            validators = {
                2: Input_validator.validate_email,
                3: Input_validator.validate_nascent_date,
                4: Document_validator.validate_cep,
                5: Document_validator.validate_cpf,
                7: Document_validator.validate_cns,
            }

            function = flows.get(user_flow["etapa_registro"])
            validator = validators.get(user_flow["etapa_registro"])

            if validator:
                validated_value = await validator(message)
                if not validated_value:
                    reply = "Por favor, digite um valor válido"
                    await send_message(reply, number_formated)
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=reply
                    )
                else:
                    # Update user data
                    await function(user, validated_value, flow_status)
                    prompt = self.get_prompt(user_flow["etapa_registro"], flow_status)
                    await send_message(prompt, number_formated)

            elif function:
                await function(user, message, flow_status)
                prompt = self.get_prompt(user_flow["etapa_registro"], flow_status)
                await send_message(prompt, number_formated)

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

    async def data_schedule_consult_update_flow(self, user: dict, message: str):
        """
        Método responsável por realizar a atualização de dados
        de agendamento de consulta durante o processo de cadas-
        tro da mesma.
          :params user: dict
          :params message: string
        """
        unities_entity = UnidadeRepository()
        consult_entity = AgendamentoConsultaRepository()
        flow_entity = FluxoEtapaRepository()
        number_formated = f"whatsapp:+" + str(user["telefone"])
        register_consult_flow = ScheduleConsultFlow()
        try:
            user_flow = await flow_entity.select_stage_from_user_id(int(user["id"]))
            flow_status = user_flow["etapa_agendamento_consulta"] + 1
            number_formated = f"whatsapp:+" + str(user["telefone"])
            schedule_data = await consult_entity.select_data_schedule_from_user_id(
                user["id"]
            )

            if user_flow["etapa_agendamento_consulta"] == 1:
                await register_consult_flow.define_specialty_consult(
                    user, message, flow_status
                )

                await send_message(
                    "Escolha a unidade suportada mais próxima de você\nDigite o número correspondente ao da unidade desejada\nEx: 1",
                    number_formated,
                )
                ## Desenvolver microsserviços das unidades para retornar as unidades por chamada de classe
                unities = await unities_entity.select_all()
                sleep(0.4)

                for i in unities:
                    unities_text = f"""Unidade {i['id']}: {i['nome'].split('(')[0]}\nEndereço: {i['endereco'].replace(',','').split('s/n')[0]}\nBairro: {i['bairro']}\nHorario de funcionamento: {i['horario_funcionamento']}"""
                    sleep(0.5)
                    await send_message(unities_text, number_formated)

                return Response(
                    status_code=status.HTTP_200_OK,
                    content="Mensagem enviada com sucesso",
                )

            elif user_flow["etapa_agendamento_consulta"] == 2:
                consult_data = await register_consult_flow.define_unity_consult(
                    user, int(message), flow_status
                )

                last_time = (
                    await consult_entity.get_last_time_scheduele_from_specialty_id(
                        int(consult_data["id_especialidade"]),
                        int(consult_data["id_unidade"]),
                    )
                )
                if consult_data["id_unidade"] != None and last_time != None:
                    data = await format_date_for_user(last_time[-1]["data_agendamento"])
                    hora = await format_time_for_user(
                        last_time[-1]["horario_termino_agendamento"]
                    )
                    await send_message(
                        f"""
                            Digite o dia que você deseja realizar a consulta\nEx: 24/12/2023\n
                            Atenção, para essa especialidade somente temos horários a partir do dia {data}, a partir das {hora}""",
                        number_formated,
                    )
                    return Response(
                        status_code=status.HTTP_200_OK,
                        content="Mensagem enviada com sucesso",
                    )
                else:
                    await send_message(
                        f"""Digite o dia que você deseja realizar a consulta\nEx: 24/12/2023""",
                        number_formated,
                    )
                    return Response(
                        status_code=status.HTTP_200_OK,
                        content="Mensagem enviada com sucesso",
                    )

            elif user_flow["etapa_agendamento_consulta"] == 3:
                date = await Input_validator.validate_date_schedule(message)
                if date["value"]:
                    await register_consult_flow.define_date_consult(
                        user, date["date"], flow_status
                    )
                    await send_message(
                        "Digite o horário que deseja realizar a consulta (atente-se para o horário estar dentro do período de funcionamento da unidade escolhida)\nEx: 08:00",
                        number_formated,
                    )
                    return Response(
                        status_code=status.HTTP_200_OK,
                        content="Mensagem enviada com sucesso",
                    )

                else:
                    reply = "Por favor, digite uma data válida"
                    await send_message(reply, number_formated)
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=reply
                    )

            elif user_flow["etapa_agendamento_consulta"] == 4:
                data_schedule = (
                    await consult_entity.select_data_schedule_from_user_cellphone(
                        int(user["telefone"])
                    )
                )
                conflict = await consult_entity.check_conflicting_schedule(
                    data_schedule["id_unidade"],
                    data_schedule["id_especialidade"],
                    data_schedule["data_agendamento"],
                    str(message) + ":00",  # horario_inicio_agendamento
                    await get_more_forty_five(message),  # horario_termino_agendamento
                    data_schedule["id"],
                )
                if conflict:
                    await send_message(
                        "Desculpe, esse horário está indisponível, por favor, informe um horário no mínimo superior ao informado anteriormente",
                        number_formated,
                    )
                    return Response(
                        status_code=status.HTTP_200_OK,
                        content="Mensagem enviada com sucesso",
                    )
                else:
                    await register_consult_flow.define_time_consult(
                        user, message, flow_status
                    )
                    await send_message(
                        "(Opcional) Digite uma mensagem descrevendo qual a sua necessidade para a especialidade escolhida.\nEx: Exame de rotina\nVocê pode digitar qualquer coisa para ignorar essa etapa)",
                        number_formated,
                    )
                    return Response(
                        status_code=status.HTTP_200_OK,
                        content="Mensagem enviada com sucesso",
                    )

            elif user_flow["etapa_agendamento_consulta"] == 5:
                await register_consult_flow.define_necessity_consult(
                    user, message, flow_status
                )
                all_data = await register_consult_flow.finalize_schedule_flow(
                    user, message, flow_status
                )

                await send_message(
                    f"Que ótimo, você realizou seu agendamento!\nCompareça à unidade {all_data['unity_info']['nome']} no dia {await format_date_for_user(all_data['data_agendamento'])} as {await format_time_for_user(all_data['horario_inicio_agendamento'])} horas para a sua consulta com o {all_data['specialty_info']['nome']}",
                    number_formated,
                )
                return Response(
                    status_code=status.HTTP_200_OK,
                    content="Mensagem enviada com sucesso",
                )

            if (
                user_flow["etapa_agendamento_consulta"] == 0
                or user_flow["etapa_agendamento_consulta"] == 0
            ):
                consult_flow_stage = await flow_entity.update_flow_from_user_id(
                    user["id"], "etapa_agendamento_consulta", 1
                )
                return Response(
                    status_code=status.HTTP_200_OK,
                    content="Fluxo atualizado com sucesso",
                )

        except Exception as error:
            message_log = "Erro ao atualizar os dados do agendamento no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "data_schedule_consult_update_flow",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": user}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )

    async def data_schedule_exam_update_flow(self, user: dict, message: str):
        """
        Método responsável por realizar a atualização de dados
        de agendamento de exame durante o processo de cadas-
        tro do mesmo.
          :params user: dict
          :params message: string
        """
        unities_entity = UnidadeRepository()
        exam_entity = AgendamentoExameRepository()
        flow_entity = FluxoEtapaRepository()
        number_formated = f"whatsapp:+" + str(user["telefone"])
        register_consult_flow = ScheduleConsultFlow()

        try:
            user_flow = await flow_entity.select_stage_from_user_id(int(user["id"]))
            flow_status = user_flow["etapa_agendamento_exame"] + 1
            number_formated = f"whatsapp:+" + str(user["telefone"])
            schedule_data = await exam_entity.select_data_schedule_from_user_id(
                user["id"]
            )

            if user_flow["etapa_agendamento_exame"] == 1:
                await register_consult_flow.define_specialty_consult(
                    user, message, flow_status
                )

                await send_message(
                    "Escolha a unidade suportada mais próxima de você\nDigite o número correspondente ao da unidade desejada\nEx: 1",
                    number_formated,
                )
                ## Desenvolver microsserviços das unidades para retornar as unidades por chamada de classe
                unities = await unities_entity.select_all()
                sleep(0.4)

                for i in unities:
                    unities_text = f"""Unidade {i['id']}: {i['nome'].split('(')[0]}\nEndereço: {i['endereco'].replace(',','').split('s/n')[0]}\nBairro: {i['bairro']}\nHorario de funcionamento: {i['horario_funcionamento']}"""
                    sleep(0.5)
                    await send_message(unities_text, number_formated)

                return Response(
                    status_code=status.HTTP_200_OK,
                    content="Mensagem enviada com sucesso",
                )

            elif user_flow["etapa_agendamento_exame"] == 2:
                consult_data = await register_consult_flow.define_unity_consult(
                    user, int(message), flow_status
                )

                last_time = (
                    await exam_entity.get_last_time_scheduele_from_specialty_id(
                        int(consult_data["id_especialidade"]),
                        int(consult_data["id_unidade"]),
                    )
                )
                if consult_data["id_unidade"] != None and last_time != None:
                    data = await format_date_for_user(last_time[-1]["data_agendamento"])
                    hora = await format_time_for_user(
                        last_time[-1]["horario_termino_agendamento"]
                    )
                    await send_message(
                        f"""
                            Digite o dia que você deseja realizar a consulta\nEx: 24/12/2023\n
                            Atenção, para essa especialidade somente temos horários a partir do dia {data}, a partir das {hora}""",
                        number_formated,
                    )
                    return Response(
                        status_code=status.HTTP_200_OK,
                        content="Mensagem enviada com sucesso",
                    )
                else:
                    await send_message(
                        f"""Digite o dia que você deseja realizar a consulta\nEx: 24/12/2023""",
                        number_formated,
                    )
                    return Response(
                        status_code=status.HTTP_200_OK,
                        content="Mensagem enviada com sucesso",
                    )

            elif user_flow["etapa_agendamento_exame"] == 3:
                date = await Input_validator.validate_date_schedule(message)
                if date["value"]:
                    await register_consult_flow.define_date_consult(
                        user, date["date"], flow_status
                    )
                    await send_message(
                        "Digite o horário que deseja realizar a consulta (atente-se para o horário estar dentro do período de funcionamento da unidade escolhida)\nEx: 08:00",
                        number_formated,
                    )
                    return Response(
                        status_code=status.HTTP_200_OK,
                        content="Mensagem enviada com sucesso",
                    )

                else:
                    reply = "Por favor, digite uma data válida"
                    await send_message(reply, number_formated)
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=reply
                    )

            elif user_flow["etapa_agendamento_exame"] == 4:
                data_schedule = (
                    await exam_entity.select_data_schedule_from_user_cellphone(
                        int(user["telefone"])
                    )
                )
                conflict = await exam_entity.check_conflicting_schedule(
                    data_schedule["id_unidade"],
                    data_schedule["id_especialidade"],
                    data_schedule["data_agendamento"],
                    str(message) + ":00",  # horario_inicio_agendamento
                    await get_more_forty_five(message),  # horario_termino_agendamento
                    data_schedule["id"],
                )
                if conflict:
                    await send_message(
                        "Desculpe, esse horário está indisponível, por favor, informe um horário no mínimo superior ao informado anteriormente",
                        number_formated,
                    )
                    return Response(
                        status_code=status.HTTP_200_OK,
                        content="Mensagem enviada com sucesso",
                    )
                else:
                    await register_consult_flow.define_time_consult(
                        user, message, flow_status
                    )
                    await send_message(
                        "(Opcional) Digite uma mensagem descrevendo qual a sua necessidade para a especialidade escolhida.\nEx: Exame de rotina\nVocê pode digitar qualquer coisa para ignorar essa etapa)",
                        number_formated,
                    )
                    return Response(
                        status_code=status.HTTP_200_OK,
                        content="Mensagem enviada com sucesso",
                    )

            elif user_flow["etapa_agendamento_exame"] == 5:
                await register_consult_flow.define_necessity_consult(
                    user, message, flow_status
                )
                all_data = await register_consult_flow.finalize_schedule_flow(
                    user, message, flow_status
                )

                await send_message(
                    f"Que ótimo, você realizou seu agendamento!\nCompareça à unidade {all_data['unity_info']['nome']} no dia {await format_date_for_user(all_data['data_agendamento'])} as {await format_time_for_user(all_data['horario_inicio_agendamento'])} horas para a sua consulta com o {all_data['specialty_info']['nome']}",
                    number_formated,
                )
                return Response(
                    status_code=status.HTTP_200_OK,
                    content="Mensagem enviada com sucesso",
                )

            if (
                user_flow["etapa_agendamento_exame"] == 0
                or user_flow["etapa_agendamento_exame"] == 0
            ):
                consult_flow_stage = await flow_entity.update_flow_from_user_id(
                    user["id"], "etapa_agendamento_exame", 1
                )
                return Response(
                    status_code=status.HTTP_200_OK,
                    content="Fluxo atualizado com sucesso",
                )

        except Exception as error:
            message_log = "Erro ao atualizar os dados do agendamento no banco de dados"
            log = Logging(message_log)
            await log.warning(
                "data_schedule_consult_update_flow",
                None,
                str(error),
                500,
                {"params": {"message": message, "user": user}},
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
            )
