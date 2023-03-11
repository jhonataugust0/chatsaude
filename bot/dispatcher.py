from sqlalchemy.orm.exc import NoResultFound 
from bot.replies import Replies
from log.logging import Logging
from datetime import date as date_type
from datetime import time as time_type
from models.repository.user_repository import UserRepository
from models.repository.fluxo_etapa_repository import FluxoEtapaRepository
from models.repository.consulta_gendameno_repository import AgendamentosRepository
from models.repository.especialidade_repository import EspecialidadeRepository
from models.repository.unidade_repository import UnidadeRepository
from time import sleep

from utils.bot_utils import send_message
from utils.validators.validate_email import validate_email
from utils.validators.validate_times import validate_date

class BotOptions:
  REGISTER_USER = '1'
  SCHEDULE_CONSULT = '2'
  SCHEDULE_EXAM = '3'
  LIST_UNITIES = '4'
  MAKE_REPORT = '5'
  
class BotDispatcher:
  def __init__(self, lang='br') -> None:
    self.lang = lang

  def message_processor(self, message: str, cellphone: int, user_dict: dict = None):
    """
      Método que processa as inputs do usuário, identificando-as e atribuindo as 
      mesmas seus respectivos gatilhos para a continuidade do fluxo da aplicação.
        :params message: str
        :params cellphone: int
    """
    try:
      
      if 'telefone' in user_dict and user_dict['telefone'] != 'None':
        if 'id' in user_dict and user_dict['id'] != 'None':
          # consult_entity = AgendamentosRepository()
          # verify_schedule_exists = consult_entity.select_data_schedule_from_user_id(int(user_dict['id'])) 
          flow_entity = FluxoEtapaRepository()
          verify_stage_user = flow_entity.select_stage_from_user_id(user_dict['id'])

        if message == BotOptions.SCHEDULE_CONSULT:
          if 'fluxo_agendamento_consulta' in verify_stage_user and (verify_stage_user['fluxo_agendamento_consulta'] == 'None' or int(verify_stage_user['fluxo_agendamento_consulta']) < 1):
            send_message(str(Replies.SCHEDULE_CONSULT), f"whatsapp:{str(cellphone)}"), 
            return {'schedule_consult_trigger': 1}

        elif message == BotOptions.SCHEDULE_EXAM:
          if 'fluxo_agendamento_exame' in verify_stage_user and (verify_stage_user['fluxo_agendamento_exame'] == 'None' or int(verify_stage_user['fluxo_agendamento_exame'] == 0)) and (verify_stage_user['fluxo_agendamento_consulta'] == 'None' or int(verify_stage_user['fluxo_agendamento_consulta']) == 0):
            return {'message': str(Replies.SCHEDULE_EXAM), 'schedule_exam_trigger': 1}

        elif message == BotOptions.MAKE_REPORT:
          return {'message': str(Replies.REPORT), 'make_report_trigger': 1}

        else: 
          if (verify_stage_user['fluxo_agendamento_consulta'] == 'None' or int(verify_stage_user['fluxo_agendamento_consulta']) == 0) and (verify_stage_user['fluxo_agendamento_exame'] == 'None' or int(verify_stage_user['fluxo_agendamento_exame']) == 0) and (verify_stage_user['fluxo_agendamento_exame'] == 'None' or int(verify_stage_user['fluxo_agendamento_exame']) == 0):
            return {'message': str(Replies.DEFAULT)}

      if message == BotOptions.REGISTER_USER:
        if 'id' not in user_dict:
          send_message(str(Replies.INIT_REGISTER_FLOW), f"whatsapp:{str(cellphone)}")
          return {'register_user_trigger': 1}
        
      else: 
        user_entity = FluxoEtapaRepository()
        if 'id' in user_dict and user_dict['id'] != 'None':
          return {}
        else:
          return {'message': str(Replies.DEFAULT_NEW_USER)}

    except Exception as error:
      message_log = f'Erro ao processar a input do usuário {message}'
      log = Logging(message_log)
      log.warning('message_processor', None, str(error), 500, {'params': {'message': message, 'cellphone': cellphone}})

  def trigger_processing(self, bot_response: dict, number: int, user: dict = None):
    try:
      stage_entity = FluxoEtapaRepository()
      user_entity = UserRepository()

      if "register_user_trigger" in bot_response and bot_response['register_user_trigger'] == 1: 
        new_user = user_entity.insert_new_user(number)
        stage_entity.insert_new_user_flow(new_user['id'], 1, 1)
        # if 'fluxo_registro' in new_flow and 'etapa_registro' in new_flow and new_flow['fluxo_registro'] == "1":
          
      elif "schedule_consult_trigger" in bot_response and bot_response['schedule_consult_trigger'] == 1:
        consult_entity = AgendamentosRepository()
        verify_exists_flow = stage_entity.select_stage_from_user_id(int(user['id'])) 
        
        if 'fluxo_agendamento_consulta' in verify_exists_flow and (verify_exists_flow['fluxo_agendamento_consulta'] == '0' or verify_exists_flow['fluxo_agendamento_consulta'] == 'None'):
          stage_entity.update_flow_from_user_id(int(user['id']), 'fluxo_agendamento_consulta', 1)
          stage_entity.update_flow_from_user_id(int(user['id']), 'etapa_agendamento_consulta', 0)
          consult_entity.insert_new_schedule_consult(int(user['id']))

      elif "register_user_trigger" in bot_response and bot_response['register_user_trigger'] == 1:
        pass
      
      elif "register_user_trigger" in bot_response and bot_response['register_user_trigger'] == 1:
        pass
    
    except Exception as error:
      message_log = f'Erro ao processar os gatilhos {bot_response}'
      log = Logging(message_log)
      log.warning('trigger_processing', None, str(error), 500, {'params': {'number': number, 'bot_response': bot_response}})

  def data_users_update_flow(self, user: dict, message: str):
    """
      Método responsável por realizar a atualização de dados
      de um usuário durante o processo de cadastro do mesmo.
        :params user: dict
        :params message: string
    """
    user_entity = UserRepository()  
    flow_entity = FluxoEtapaRepository() 
    try:
      number_formated = f"whatsapp:+"+str(user['telefone'])
      user_flow = flow_entity.select_stage_from_user_id(int(user['id']))
      flow_status = (int(user_flow['etapa_registro']) + 1)

      if int(user_flow['etapa_registro']) == 1:
        user_entity.update_user_data(user['telefone'], 'nome', str(message)) 
        flow_entity.update_flow_from_user_id(user['id'], 'etapa_registro', flow_status)
        send_message("Digite seu melhor email\nEx:maria.fatima@gmail.com", number_formated)

      elif int(user_flow['etapa_registro']) == 2:
        if (validate_email(message)):
          user_entity.update_user_data(user['telefone'], 'email', str(message)) 
          flow_entity.update_flow_from_user_id(user['id'], 'etapa_registro', flow_status)
          send_message("Digite sua data de nascimento\nEx:01/02/2000", number_formated)            
        else:
          send_message("Por favor, digite um email válido", number_formated)
      
      elif int(user_flow['etapa_registro']) == 3: 
        nescient_date = validate_date(message) 
        if (nescient_date['value']):
          user_entity.update_user_data(user['telefone'], 'data_nascimento', nescient_date['date'])
          flow_entity.update_flow_from_user_id(user['id'], 'etapa_registro', flow_status)
          send_message("Digite seu CEP\nEx:56378-921", number_formated)            
        else:
          send_message("Por favor, digite uma data válida", number_formated)

      elif int(user_flow['etapa_registro']) == 4:
        user_entity.update_user_data(user['telefone'], 'cep', int(message.replace('-','')))
        flow_entity.update_flow_from_user_id(user['id'], 'etapa_registro', flow_status)
        send_message("Digite seu CPF\nEx:157.934.724-28", number_formated) 

      elif int(user_flow['etapa_registro']) == 5:
        user_entity.update_user_data(user['telefone'], 'cpf', int(message.replace('.','').replace('-','')))
        flow_entity.update_flow_from_user_id(user['id'], 'etapa_registro', flow_status)
        send_message("Digite o número do seu RG\nEx:4563912-9", number_formated)            

      elif int(user_flow['etapa_registro']) == 6:
        user_entity.update_user_data(user['telefone'], 'rg', int(message.replace('-','')))
        flow_entity.update_flow_from_user_id(user['id'], 'etapa_registro', flow_status)
        send_message("Digite o número do seu cartão do SUS\nEx:145.000.875.165.186", number_formated) 

      elif int(user_flow['etapa_registro']) == 7:
        user_entity.update_user_data(user['telefone'], 'c_sus', str(message))
        flow_entity.update_flow_from_user_id(user['id'], 'etapa_registro', flow_status)
        send_message("Digite o nome do seu bairro\nEx: Benedito Bentes", number_formated)    

      elif int(user_flow['etapa_registro']) == 8:
        user_entity.update_user_data(user['telefone'], 'bairro', str(message))
        flow_entity.update_flow_from_user_id(user['id'], 'fluxo_registro', 0)
        user_entity.update_user_data(user['telefone'], 'etapa_registro', 0)
        info = "Usuário cadastrado com êxito"
        log = Logging(info)
        log.info()
        send_message("Parabéns, seu cadastro foi concluído, agora você pode agendar consultas ou exames pelo chat!\nDigite qualquer tecla para ver as opções", number_formated) 

        
    except Exception as error:
      message_log = 'Erro ao atualizar os dados do usuário no banco de dados'
      log = Logging(message_log)
      log.warning('flow_registration', None, str(error), 500, {'params': {'message': message, 'user': user}})
  
  def data_schedule_consult_update_flow(self, user: dict, message: str):
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
   
    user_flow = flow_entity.select_stage_from_user_id(int(user['id']))
    flow_status = (int(user_flow['etapa_agendamento_consulta']) + 1)
    try:
      number_formated = f"whatsapp:+"+str(user['telefone'])
      
      if int(user_flow['etapa_agendamento_consulta']) == 1:
        specialty_entity = EspecialidadeRepository()
        specialty_user_request = specialty_entity.select_specialty_from_name(message)
        
        user_flow = flow_entity.update_flow_from_user_id(user['id'], 'etapa_agendamento_consulta', flow_status)
        
        consult_entity.update_schedule_from_user_id(user['id'], 'id_especialidade', specialty_user_request['id'])
        
        send_message("Escolha a unidade suportada mais próxima de você\nDigite o número correspondente ao da unidade desejada\nEx: 1", number_formated)
        unities = unities_entity.select_all()
        sleep(0.4)
        
        for i in unities:
          unities_text = f"""Unidade {i['id']}: {i['nome'].split('(')[0]}\nEndereço: {i['endereco'].replace(',','').split('s/n')[0]}\nBairro: {i['bairro']}\nHorario de funcionamento: {i['horario_funcionamento']}"""
          sleep(0.5)
          send_message(unities_text, number_formated)
      
      elif int(user_flow['etapa_agendamento_consulta']) == 2:
        user_flow = flow_entity.update_flow_from_user_id(user['id'], 'etapa_agendamento_consulta', flow_status)
        consult_data = consult_entity.update_schedule_from_user_id(user['id'], 'id_unidade', int(message))
        if consult_data['id_unidade'] != 'None':
          send_message("Digite o dia que você deseja realizar a consulta\nEx: 24/12/2023", number_formated)
      
      elif int(user_flow['etapa_agendamento_consulta']) == 3:
        date = validate_date(message) 
        if (date['value']):
          user_flow = flow_entity.update_flow_from_user_id(user['id'], 'etapa_agendamento_consulta', flow_status)
          consult_entity.update_schedule_from_user_id(user['id'], 'data_agendamento', date['date'])
          send_message("Digite o horário que deseja realizar a consulta (atente-se para o horário estar dentro do período de funcionamento da unidade escolhida)\nEx: 08:00", number_formated)
        else:
          send_message("Por favor, digite uma hora válida", number_formated)
      
      elif int(user_flow['etapa_agendamento_consulta']) == 4:
        user_flow = flow_entity.update_flow_from_user_id(user['id'], 'etapa_agendamento_consulta', flow_status)
        consult_data = consult_entity.update_schedule_from_user_id(user['id'], 'horario_inicio_agendamento', str(message))
        send_message("(Opcional) Digite uma mensagem descrevendo qual a sua necessidade para a especialidade escolhida.\nEx: Exame de rotina\nVocê pode digitar qualquer coisa para ignorar essa etapa)", number_formated)
      
      elif int(user_flow['etapa_agendamento_consulta']) == 5:
        user_flow = flow_entity.update_flow_from_user_id(user['id'], 'etapa_agendamento_consulta', 0)
        user_flow = flow_entity.update_flow_from_user_id(user['id'], 'fluxo_agendamento_consulta', 0)
        consult_data = consult_entity.update_schedule_from_user_id(user['id'], 'descricao_necessidade', str(message))
        # all_data = consult_entity.select_all_data_from_schedule_with_id(consult_data['id'])
        # send_message(f"Que ótimo, você realizou seu agendamento!\nCompareça à unidade {all_data['unity_info']['nome']} no dia {all_data['data_agendamento']} as {all_data['horario_inicio_agendamento']} horas para a sua consulta com o {all_data['specialty_info']['nome']}", number_formated)
        send_message(f"Que ótimo, você realizou seu agendamento!\nCompareça à unidade escolhida no dia {consult_data['data_agendamento']} as {consult_data['horario_inicio_agendamento']} horas.", number_formated)
        return True  

     
      if int(user_flow['etapa_agendamento_consulta']) == 0 or user_flow['etapa_agendamento_consulta'] == 'None':
        consult_flow_stage = flow_entity.update_flow_from_user_id(user['id'], 'etapa_agendamento_consulta', 1)
    
    except Exception as error:
      message_log = 'Erro ao atualizar os dados do agendamento no banco de dados'
      log = Logging(message_log)
      log.warning('data_schedule_consult_update_flow', None, str(error), 500, {'params': {'message': message, 'user': user}})