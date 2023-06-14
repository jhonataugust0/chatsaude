from api.services.chatbot.bot.replies import Replies
from api.services.chatbot.utils.bot_utils import send_message

class ScheduleConsultTrigger:
    @classmethod
    async def schedule_consult_trigger(self, verify_stage_user, cellphone):
        if "fluxo_agendamento_consulta" in verify_stage_user and (
            verify_stage_user["fluxo_agendamento_consulta"] == None
            or verify_stage_user["fluxo_agendamento_consulta"] < 1
        ):
            await send_message(
                str(Replies.SCHEDULE_CONSULT), f"whatsapp:{str(cellphone)}"
            )
            return {"schedule_consult_trigger": 1}
