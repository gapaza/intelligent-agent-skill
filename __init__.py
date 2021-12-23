from mycroft import MycroftSkill, intent_file_handler


class IntelligentAgent(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('agent.intelligent.intent')
    def handle_agent_intelligent(self, message):
        self.speak_dialog('agent.intelligent')


def create_skill():
    return IntelligentAgent()

