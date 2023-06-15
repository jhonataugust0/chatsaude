from api.services.chatbot.bot.replies import Replies
from api.services.chatbot.utils.bot_utils import send_message


class RegisterUserTrigger:
    @classmethod
    async def register_user_trigger(self, user_dict, cellphone):
        if "id" not in user_dict:
            await send_message(
                str(Replies.INIT_REGISTER_FLOW), f"whatsapp:{str(cellphone)}"
            )
            return {"register_user_trigger": 1}
