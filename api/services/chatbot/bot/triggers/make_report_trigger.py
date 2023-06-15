from api.services.chatbot.bot.replies import Replies
from api.services.chatbot.utils.bot_utils import send_message

class MakeReportTrigger:
    @classmethod
    async def make_report_trigger(self):
            return {"message": str(Replies.REPORT), "make_report_trigger": 1}
