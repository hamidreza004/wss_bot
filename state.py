class Situation:
    def __init__(self):
        self.placeStr = 1
        # my idea: _lst=[5,1] means: 5=went to sponsors page and then navigated to 1=second sponsor page...
        self.reset()

    def reset(self):
        self.placeStr = 1
        # default (start) state

    def get_state(self):
        return self.placeStr

    def move_to_nextState(self, state):
        self.placeStr = self.placeStr * 10 + state


