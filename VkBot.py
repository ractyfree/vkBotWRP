import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import *

from utils.service.WorkerThread import WorkerThread


class VkBot:
    """ Main class.

        str:token - requires yours group token from VK.
        str:group_id - requires yours group id, can be retrieved by yourself.

    """

    def __init__(self, token, group_id):
        self.token = token
        self.group_id = group_id
        self.message_handlers = []

    def __notify_message_handlers(self, new_message):
        for handler in self.message_handlers:
            handler(new_message)

    def __registerHandler(self, func):
        self.message_handlers.append(func)

    def messageHandler(self):
        def decorator(handler):
            self.__registerHandler(handler)

            return handler

        return decorator

    def __processNewMessages(self, messages):
        self.__notify_message_handlers(messages)

    def __getUpdates(self):
        updates = self.bot.listen()
        for update in updates:
            self.__processUpdate(update)

    def __processUpdate(self, update):
        new_messages = []
        if update.type == VkBotEventType.MESSAGE_NEW:
            new_messages.append(update.object)

        if len(new_messages) > 0:
            self.__processNewMessages(new_messages)

    def __doLogin(self):
        vk_session = vk_api.VkApi(token=self.token)
        self.vk = vk_session.get_api()
        self.bot = VkBotLongPoll(vk_session, self.group_id)

    def send_message(self, user_id, message, keyboard=None):
        self.vk.messages.send(user_id=user_id,
                              random_id=get_random_id,
                              message=message,
                              )
        # ((keyboard=keyboard) if keyboard != None else None))

    def startPolling(self, none_stop=False):
        self.__doLogin()
        polling_thread = WorkerThread(self.__getUpdates)
