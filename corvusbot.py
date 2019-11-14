import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import *
import threading










class WorkerThread(threading.Thread):
""" Basic threads controller class. Got this imp from pyTelegramBotApi.

	str:name - Requires name of the thread to be used

"""
    def __init__(self, name):
        #self.name = name

        #threading.Thread.__init__(self, name=self.name)
        threading.Thread.__init__(self, name=name)
        self.queue = []
        self._running = True
        self.start()

    def put(self, func):
        self.queue.append(func)

    def run(self):
        while self._running:
            try:
                for x in self.queue:
                    x()
            except Exception as e:
                print(e)


class VkBot:

""" Main class.	

	str:token - requires yours group token from VK.
	str:group_id - requires yours group id, can be retrieved by yourself.

"""



    def __init__(self, token='', group_id=''):
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
            #((keyboard=keyboard) if keyboard != None else None))

    def startPolling(self, none_stop=False):
        self.__doLogin()
        polling_thread = WorkerThread('Polling')
        polling_thread.put(self.__getUpdates)





"""
Example usage:

bot = VkBot(token='YOUR_LONG_TOKEN', group_id='your_group_id')

@bot.messageHandler()
def basic_message(message):
    print("From here")
    print(message)

bot.startPolling()


By the way do not forget to enable bot's ability to receive messages in your group's settings neither your bot wouldn't receive any messages from anyone!


"""


