from api.services.chatbot.bot.replies import Replies
from api.services.chatbot.utils.bot_utils import send_message

class ScheduleExamTrigger:
    @classmethod
    async def schedule_exam_trigger(self, verify_stage_user, cellphone):
            if "fluxo_agendamento_exame" in verify_stage_user and (
                verify_stage_user["fluxo_agendamento_exame"] == None
                or verify_stage_user["fluxo_agendamento_exame"] < 1
            ):
                await send_message(str(Replies.SCHEDULE_EXAM), f"whatsapp:{str(cellphone)}")
                return {
                    "message": str(Replies.SCHEDULE_EXAM),
                    "schedule_exam_trigger": 1,
                }
