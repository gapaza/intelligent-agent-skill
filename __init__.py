from mycroft import MycroftSkill, intent_file_handler

from .controller.api import NXTClient

class IntelligentAgent(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.warning_stop_prompt_count = 0
        # self.register_entity_file('seconds.entity')
        # self.register_entity_file('degrees.entity')

    @property
    def nxt_client(self):
        return NXTClient()

    def _move(self, direction):
        # --> 1. Let the user know to say stop when moving forward
        if self.warning_stop_prompt_count < 1:
            self.speak('Tell me when to stop', wait=True)
            self.warning_stop_prompt_count += 1

        # --> 2. Move forward
        controller = self.nxt_client.move(direction, power='low')

        # --> 3. Wait for response
        response = self.get_response(num_retries=3)
        if response is not None:
            if 'stop' in response:
                self.speak('Stopping', wait=False)
                controller.stop()
                return
        controller.stop()


    @intent_file_handler('agent.purpose.intent')
    def purpose(self, message):
        self.speak('I am an intelligent companion')




    @intent_file_handler('agent.move.forward.intent')
    def move_forward(self, message):
        self._move('f')

    @intent_file_handler('agent.move.backward.intent')
    def move_backward(self, message):
        self._move('b')

    @intent_file_handler('agent.turn.clockwise.intent')
    def turn_clockwise(self, message):
        self._move('cw')

    @intent_file_handler('agent.turn.cclockwise.intent')
    def turn_cclockwise(self, message):
        self._move('ccw')





    @intent_file_handler('agent.radar.ping.intent')
    def radar_ping(self, message):
        self.speak('something')

    @intent_file_handler('agent.radar.rotate.intent')
    def radar_rotate(self, message):
        self.speak('something')



def create_skill():
    return IntelligentAgent()


