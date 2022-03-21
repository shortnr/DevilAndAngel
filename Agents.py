from constants import *


class Agent:
    def __init__(self, neural_net):
        self.brain = neural_net
        self.bombs_detonated = 0
        self.total_distance = 0
        self.distance_updated = False

    @staticmethod
    def can_win(robot, bomb):
        winnable = True

        if robot.x >= bomb.x or robot.y < bomb.y or (robot.y - bomb.y) / (bomb.x - robot.x) > 2:
            winnable = False

        return winnable


class AngelAgent(Agent):
    def __init__(self, neural_net):
        super().__init__(neural_net)
        self.color = BLUE

    def move(self, inputs):
        self.brain.predict(inputs)
        if self.brain.output_layer[0] >= self.brain.output_layer[1]:
            return 0, -1
        else:
            return 0, 0


class DevilAgent(Agent):
    def __init__(self, neural_net):
        super().__init__(neural_net)
        self.color = RED

    def move(self, inputs):
        self.brain.predict(inputs)
        if self.brain.output_layer[0] >= self.brain.output_layer[1]:
            return 1, 0
        else:
            return 1, -1
