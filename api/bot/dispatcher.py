from datetime import date as date_type
from datetime import time as time_type
from time import sleep

from fastapi import HTTPException, Response, status

from api.bot.replies import Replies
from api.log.logging import Logging
from api.models.repository.consulta_gendameno_repository import \
    AgendamentosRepository
from api.models.repository.especialidade_repository import \
    EspecialidadeRepository
from api.models.repository.fluxo_etapa_repository import FluxoEtapaRepository
from api.models.repository.unidade_repository import UnidadeRepository
from api.models.repository.user_repository import UserRepository
from api.utils.bot_utils import send_message
from api.utils.date import (convert_to_datetime, format_date_for_user,
                            format_time_for_user, get_more_forty_five)
from api.utils.validators.validate_c_sus import validate_cns
from api.utils.validators.validate_cpf import validate_cpf
from api.utils.validators.validate_email import validate_email
from api.utils.validators.validate_times import (validate_date_schedule,
                                                 validate_nascent_date)


class BotOptions:
    REGISTER_USER = "1"
    SCHEDULE_CONSULT = "2"
    SCHEDULE_EXAM = "3"
    LIST_UNITIES = "4"
    MAKE_REPORT = "5"


class BotDispatcher:
    def __init__(self, lang="br") -> None:
        self.lang = lang

    async def message_processor(self, message: str, cellphone: int, user_dict: dict = None) -> dict[str]:
        """
            Método que processa as inputs do usuário, identificando-as e atribuindo as
            mesmas seus respectivos gatilhos para a continuidade do fluxo da aplicação.
            :params message: str
            :params cellphone: int
            return dict | Response: Response
        """
        try:
            if "telefone" in user_dict and user_dict["telefone"] != None:
                if "id" in user_dict and user_dict["id"] != None:
                    flow_entity = FluxoEtapaRepository()
                    verify_stage_user = await flow_entity.select_stage_from_user_id(user_dict["id"])

                if message == BotOptions.SCHEDULE_CONSULT:
                    if "fluxo_agendamento_consulta" in verify_stage_user and (
                        verify_stage_user["fluxo_agendamento_consulta"] == None
                        or verify_stage_user["fluxo_agendamento_consulta"] < 1
                    ):
                        await send_message(
                            str(Replies.SCHEDULE_CONSULT), f"whatsapp:{str(cellphone)}"
                        ),
                        return {"schedule_consult_trigger": 1}

                elif message == BotOptions.SCHEDULE_EXAM:
                    if ("fluxo_agendamento_exame" in verify_stage_user and (
                            verify_stage_user["fluxo_agendamento_exame"] == None
                            or verify_stage_user["fluxo_agendamento_exame"] == 0
                        ) and (
                            verify_stage_user["fluxo_agendamento_consulta"] == None
                            or verify_stage_user["fluxo_agendamento_consulta"] == 0
                        )
                    ):
                        return {
                            "message": str(Replies.SCHEDULE_EXAM),
                            "schedule_exam_trigger": 1,
                        }

                elif message == BotOptions.MAKE_REPORT:
                    return {"message": str(Replies.REPORT), "make_report_trigger": 1}

                else:
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

            if message == BotOptions.REGISTER_USER:
                if "id" not in user_dict:
                    await send_message(
                        str(Replies.INIT_REGISTER_FLOW), f"whatsapp:{str(cellphone)}"
                    )
                    return {"register_user_trigger": 1}

            else:
                user_entity = FluxoEtapaRepository()
                if "id" in user_dict and user_dict["id"] != None:
                    return {}
                else:
                    return {"message": str(Replies.DEFAULT_NEW_USER)}

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

    async def trigger_processing(self, bot_response: dict, number: int, user: dict = None) -> Response:
        try:
            stage_entity = FluxoEtapaRepository()
            user_entity = UserRepository()

            if ("register_user_trigger" in bot_response
                and bot_response["register_user_trigger"] == 1
            ):
                new_user = await user_entity.insert_new_user(number)
                await stage_entity.insert_new_user_flow(new_user["id"], 1, 1)
                return Response(
                    status_code=status.HTTP_200_OK,
                    content="Usuário inserido com sucesso",
                )

            elif (
                "schedule_consult_trigger" in bot_response
                and bot_response["schedule_consult_trigger"] == 1
            ):
                consult_entity = AgendamentosRepository()
                verify_exists_flow = await stage_entity.select_stage_from_user_id(user["id"])

                if "fluxo_agendamento_consulta" in verify_exists_flow and (
                    verify_exists_flow["fluxo_agendamento_consulta"] == 0
                    or verify_exists_flow["fluxo_agendamento_consulta"] == None
                ):
                    await stage_entity.update_flow_from_user_id(
                        user["id"], "fluxo_agendamento_consulta", 1
                    )
                    await stage_entity.update_flow_from_user_id(
                        user["id"], "etapa_agendamento_consulta", 0
                    )
                    await consult_entity.insert_new_schedule_consult(user["id"])
                    return Response(
                        status_code=status.HTTP_200_OK,
                        content="Agendamento de consulta iniciado com sucesso",
                    )

            elif (
                "register_user_trigger" in bot_response
                and bot_response["register_user_trigger"] == 1
            ):
                pass

            elif (
                "register_user_trigger" in bot_response
                and bot_response["register_user_trigger"] == 1
            ):
                pass

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
        Método responsável por realizar a atualização de dados
        de um usuário durante o processo de cadastro do mesmo.
          :params user: dict
          :params message: string
        """
        user_entity = UserRepository()
        flow_entity = FluxoEtapaRepository()
        try:
            number_formated = f"whatsapp:+" + str(user["telefone"])
            user_flow = await flow_entity.select_stage_from_user_id(int(user["id"]))
            flow_status = user_flow["etapa_registro"] + 1

            if user_flow["etapa_registro"] == 1:
                await user_entity.update_user_data(
                    user["telefone"], "nome", str(message)
                )
                await flow_entity.update_flow_from_user_id(
                    user["id"], "etapa_registro", flow_status
                )
                await send_message(
                    "Digite seu melhor email\nEx:maria.fatima@gmail.com",
                    number_formated,
                )
                return Response(
                    status_code=status.HTTP_200_OK,
                    content="Mensagem enviada com sucesso",
                )

            elif user_flow["etapa_registro"] == 2:
                if await validate_email(message):
                    await user_entity.update_user_data(
                        user["telefone"], "email", str(message)
                    )
                    await flow_entity.update_flow_from_user_id(
                        user["id"], "etapa_registro", flow_status
                    )
                    await send_message(
                        "Digite sua data de nascimento\nEx:12/12/1997", number_formated
                    )
                    return Response(
                        status_code=status.HTTP_200_OK,
                        content="Mensagem enviada com sucesso",
                    )

                else:
                    reply = "Por favor, digite um email válido"
                    await send_message(reply, number_formated)
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=reply
                    )

            elif user_flow["etapa_registro"] == 3:
                nescient_date = await validate_nascent_date(message)

                if nescient_date["value"]:
                    await user_entity.update_user_data(
                        user["telefone"], "data_nascimento", nescient_date["date"]
                    )
                    await flow_entity.update_flow_from_user_id(
                        user["id"], "etapa_registro", flow_status
                    )
                    await send_message("Digite seu CEP\nEx:56378-921", number_formated)

                else:
                    reply = "Por favor, digite uma data válida"
                    await send_message(reply, number_formated)
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=reply
                    )

            elif user_flow["etapa_registro"] == 4:
                await user_entity.update_user_data(
                    user["telefone"], "cep", int(message.replace("-", ""))
                )
                await flow_entity.update_flow_from_user_id(
                    user["id"], "etapa_registro", flow_status
                )
                await send_message("Digite seu CPF\nEx:157.934.724-28", number_formated)
                return Response(
                    status_code=status.HTTP_200_OK,
                    content="Mensagem enviada com sucesso",
                )

            elif user_flow["etapa_registro"] == 5:
                if await validate_cpf(message):
                    await user_entity.update_user_data(
                        user["telefone"],
                        "cpf",
                        int(message.replace(".", "").replace("-", "")),
                    )
                    await flow_entity.update_flow_from_user_id(
                        user["id"], "etapa_registro", flow_status
                    )
                    await send_message(
                        "Digite o número do seu RG\nEx:4563912-9", number_formated
                    )
                    return Response(
                        status_code=status.HTTP_200_OK,
                        content="Mensagem enviada com sucesso",
                    )

                else:
                    reply = "Por favor, digite um cpf válido"
                    await send_message(reply, number_formated)
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=reply
                    )

            elif user_flow["etapa_registro"] == 6:
                await user_entity.update_user_data(
                    user["telefone"], "rg", int(message.replace("-", ""))
                )
                await flow_entity.update_flow_from_user_id(
                    user["id"], "etapa_registro", flow_status
                )
                await send_message(
                    "Digite o número do seu cartão do SUS\nEx:145.000.875.165.186",
                    number_formated,
                )
                return Response(
                    status_code=status.HTTP_200_OK,
                    content="Mensagem enviada com sucesso",
                )

            elif user_flow["etapa_registro"] == 7:
                if await validate_cns(str(message).replace(".", "").replace("-", "")):
                    await user_entity.update_user_data(
                        user["telefone"],
                        "c_sus",
                        float(str(message).replace(".", "").replace("-", "")),
                    )
                    await flow_entity.update_flow_from_user_id(
                        user["id"], "etapa_registro", flow_status
                    )
                    await send_message(
                        "Digite o nome do seu bairro\nEx: Benedito Bentes",
                        number_formated,
                    )
                    return Response(
                        status_code=status.HTTP_200_OK,
                        content="Mensagem enviada com sucesso",
                    )

                else:
                    reply = "Por favor, digite um cartão nacional de saúde válido"
                    await send_message(reply, number_formated)
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST, detail=reply
                    )

            elif user_flow["etapa_registro"] == 8:
                await user_entity.update_user_data(
                    user["telefone"], "bairro", message
                )
                await flow_entity.update_flow_from_user_id(
                    user["id"], "fluxo_registro", 0
                )
                await flow_entity.update_flow_from_user_id(
                    user["id"], "etapa_registro", 0
                )
                info = "Usuário cadastrado com êxito"
                log = await Logging(info).info()

                await send_message(
                    "Parabéns, seu cadastro foi concluído, agora você pode agendar consultas ou exames pelo chat!\nDigite qualquer tecla para ver as opções",
                    number_formated,
                )
                return Response(
                    status_code=status.HTTP_200_OK,
                    content="Mensagem enviada com sucesso",
                )

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
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message_log
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
        consult_entity = AgendamentosRepository()
        flow_entity = FluxoEtapaRepository()

        user_flow = await flow_entity.select_stage_from_user_id(user["id"])
        flow_status = user_flow["etapa_agendamento_consulta"] + 1
        try:
            number_formated = f"whatsapp:+" + str(user["telefone"])
            schedule_data = await consult_entity.select_data_schedule_from_user_id(user["id"])

            if user_flow["etapa_agendamento_consulta"] == 1:
                specialty_entity = EspecialidadeRepository()

                specialty_user_request = (
                    await specialty_entity.select_specialty_from_name(message)
                )
                user_flow = await flow_entity.update_flow_from_user_id(
                    user["id"], "etapa_agendamento_consulta", flow_status
                )

                consult_data = await consult_entity.update_schedule_from_id(
                    schedule_data["id"],
                    "id_especialidade",
                    specialty_user_request["id"],
                )

                await send_message(
                    "Escolha a unidade suportada mais próxima de você\nDigite o número correspondente ao da unidade desejada\nEx: 1",
                    number_formated,
                )
                unities = await unities_entity.select_all()
                sleep(0.4)  # transformar em async await

                for i in unities:
                    unities_text = f"""Unidade {i['id']}: {i['nome'].split('(')[0]}\nEndereço: {i['endereco'].replace(',','').split('s/n')[0]}\nBairro: {i['bairro']}\nHorario de funcionamento: {i['horario_funcionamento']}"""
                    sleep(0.5)
                    await send_message(unities_text, number_formated)

                return Response(
                    status_code=status.HTTP_200_OK,
                    content="Mensagem enviada com sucesso",
                )

            elif user_flow["etapa_agendamento_consulta"] == 2:
                user_flow = await flow_entity.update_flow_from_user_id(
                    user["id"], "etapa_agendamento_consulta", flow_status
                )
                consult_data = await consult_entity.update_schedule_from_id(
                    schedule_data["id"], "id_unidade", int(message)
                )
                last_time = (
                    await consult_entity.get_last_time_scheduele_from_specialty_id(
                        int(consult_data["id_especialidade"]),
                        int(consult_data["id_unidade"]),
                    )
                )
                if consult_data["id_unidade"] != None:
                    if last_time != None:
                        data = await format_date_for_user(
                            last_time[-1]["data_agendamento"]
                        )
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
                date = await validate_date_schedule(message)
                if date["value"]:
                    user_flow = await flow_entity.update_flow_from_user_id(
                        user["id"], "etapa_agendamento_consulta", flow_status
                    )
                    await consult_entity.update_schedule_from_id(
                        schedule_data["id"], "data_agendamento", date["date"]
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
                    await send_message(
                        "(Opcional) Digite uma mensagem descrevendo qual a sua necessidade para a especialidade escolhida.\nEx: Exame de rotina\nVocê pode digitar qualquer coisa para ignorar essa etapa)",
                        number_formated,
                    )
                    return Response(
                        status_code=status.HTTP_200_OK,
                        content="Mensagem enviada com sucesso",
                    )

            elif user_flow["etapa_agendamento_consulta"] == 5:
                user_flow = await flow_entity.update_flow_from_user_id(
                    user["id"], "etapa_agendamento_consulta", 0
                )
                user_flow = await flow_entity.update_flow_from_user_id(
                    user["id"], "fluxo_agendamento_consulta", 0
                )
                consult_data = await consult_entity.update_schedule_from_id(
                    schedule_data["id"], "descricao_necessidade", str(message)
                )
                all_data = await consult_entity.select_all_data_from_schedule_with_id(
                    consult_data["id"]
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
