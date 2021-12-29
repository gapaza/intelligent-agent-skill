from mycroft import MycroftSkill, intent_file_handler

from .controller.api import NXTClient

class IntelligentAgent(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.register_entity_file('seconds.entity')
        self.register_entity_file('degrees.entity')

    @property
    def nxt_client(self):
        return NXTClient()

    @intent_file_handler('agent.purpose.intent')
    def handle_agent_intelligent(self, message):
        self.speak('I am an intelligent companion')

    @intent_file_handler('agent.move.forward.intent')
    def handle_agent_intelligent(self, message):
        self.speak('something')

    @intent_file_handler('agent.move.backward.intent')
    def handle_agent_intelligent(self, message):
        self.speak('something')

    @intent_file_handler('agent.radar.ping.intent')
    def handle_agent_distance(self, message):
        self.speak('something')

    @intent_file_handler('agent.radar.rotate.intent')
    def handle_agent_distance(self, message):
        self.speak('something')



def create_skill():
    return IntelligentAgent()


