class Replies:
    SCHEDULE_CONSULT = "Digite a especialidade para iniciar o processo de agendamento de consulta\nEx: pediatra"
    SCHEDULE_EXAM = "Digite o exame para o iniciar o processo de agendamento de exames\nEx:Eletrocardiograma"
    INIT_REGISTER_FLOW = (
        "Precisaremos de alguns dados seus, por favor, digite seu nome\nExemplo: João"
    )
    DEFAULT_NEW_USER = "Olá, seja bem vindo ao chat saúde! Seu assistente virtual para o serviço público de saúde.\nPor favor, digite '1' para iniciar o processo de cadastro e poder utilizar dos serviços do chatbot"
    DEFAULT = "Olá, seja bem vindo ao chat saúde! Seu assistente virtual para o serviço público de saúde.\nDo que você precisa hoje?\n2 - Marcar consultas\n3 - Marcar exames\n4 - Listar unidades disponíveis\n5 - Fazer denúncia\nDigite o número correspondente ao atendimento que você deseja. Exemplo: '1'\n"
    REPORT = (
        "Por favor, descreva o ocorrido que te aborreceu, garantimos sua anonimidade"
    )
    REGISTER_FULL = "Obrigado por se cadastrar em nossa plataforma, digite algo para ver o que podemos oferecer."

    @classmethod
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

    @classmethod
    async def default_new_user_reply(self, user_dict):
        if "id" not in user_dict or user_dict["id"] == None:
            return {"message": str(Replies.DEFAULT_NEW_USER)}
        else:
            return {}

    @classmethod
    async def get_prompt(self, current_step: int, next_step: int) -> str:
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
                return f"Digite seu CPF\nEx:157.415.762-99"
        elif current_step == 5:
            if next_step == 6:
                return f"Digite seu RG\nEx:5740286-4"
        elif current_step == 6:
            if next_step == 7:
                return f"Digite seu cartão do sus\nEx:102.105.013.604.030"
        elif current_step == 7:
            if next_step == 8:
                return f"Digite seu bairro:\nEx: Eustáquio Gomes"
        return ""
