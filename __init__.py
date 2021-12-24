from mycroft import MycroftSkill, intent_file_handler

from .controller.api import NXTClient

import threading


class IntelligentAgent(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        # self.nxt_client = NXTClient()
        
    

    @intent_file_handler('agent.intelligent.intent')
    def handle_agent_intelligent(self, message):
        nxt_client = NXTClient()
        # nxt_client.run_motor(motor='A', power='low', duration=3)
        print('--> finished running motor')		
        th = threading.Thread(target=nxt_client.run_motor, args=('A', 'low', 3))
        th.start()
        self.speak_dialog('agent.intelligent')
    


    @intent_file_handler('agent.distance.intent')
    def handle_agent_distance(self, message):
        nxt_client = NXTClient()
        distance = nxt_client.get_distance()
        response = 'I can see ' + distance + 'ahead of me'
        self.speak(response)


		

def create_skill():
    return IntelligentAgent()


