from random import randint
from Objects import *
from Population import *
from helper_functions import *


class Simulation:
    def __init__(self):
        if graphics:
            pg.init()
            self.font = pg.font.SysFont('Ubuntu Mono, Bold', 24)
            self.screen = pg.display.set_mode((window_width, window_height))
            self.clock = pg.time.Clock()

        self.board = np.zeros((board_width + 10, board_height + 10))

        self.agent_levels = ['median', 'best', 'bad']
        # self.agent_levels = ['best']

        devil_nn = NeuralNetwork()
        devil_nn.load_nn_from_file("agents/bad_devil.json")
        self.devil = DevilAgent(devil_nn)

        angel_nn = NeuralNetwork()
        angel_nn.load_nn_from_file("agents/bad_angel.json")
        self.angel = AngelAgent(angel_nn)

        self.robot = Robot()
        self.bomb = Bomb()
        self.rounds_played = 0
        self.quit = False
        self.round_complete = False
        self.turns = 0
        self.devil_first = True
        self.done = False

    def run(self):
        while not self.quit and not self.done:
            self.rounds_played = 0

            results = [[], [], [],
                       [], [], [],
                       [], [], []]

            for i in range(1 if graphics else 1000):
                print("Simulation: " + str(i))
                for d in range(len(self.agent_levels)):
                    self.angel.brain.load_nn_from_file("agents/" + self.agent_levels[d] + "_angel.json")
                    for a in range(len(self.agent_levels)):
                        self.devil.brain.load_nn_from_file("agents/" + self.agent_levels[a] + "_devil.json")
                        while not self.quit and self.rounds_played < num_rounds_per_gen:
                            self.new_round()
                            self.play_round()
                            self.rounds_played += 1

                        results[3 * d + a].append(self.devil.bombs_detonated)
                        self.devil.bombs_detonated = 0
                        self.rounds_played = 0

            if not graphics:
                print("Average detonation percentage (median angel/median devil): " +
                      str(sum(results[0]) / len(results[0])) + "%")
                print("Average detonation percentage (median angel/best devil): " +
                      str(sum(results[1]) / len(results[1])) + "%")
                print("Average detonation percentage (median angel/bad devil): " +
                      str(sum(results[2]) / len(results[2])) + "%")
                print("Average detonation percentage (best angel/median devil): " +
                      str(sum(results[3]) / len(results[3])) + "%")
                print("Average detonation percentage (best angel/best devil): " +
                      str(sum(results[4]) / len(results[4])) + "%")
                print("Average detonation percentage (best angel/bad devil): " +
                      str(sum(results[5]) / len(results[5])) + "%")
                print("Average detonation percentage (bad angel/median devil): " +
                      str(sum(results[6]) / len(results[6])) + "%")
                print("Average detonation percentage (bad angel/best devil): " +
                      str(sum(results[7]) / len(results[7])) + "%")
                print("Average detonation percentage (bad angel/bad devil): " +
                      str(sum(results[8]) / len(results[8])) + "%")

            self.done = True

        pg.quit()

    def run_face_off(self):
        self.devil.brain.load_nn_from_file("agents/best_devil.json")
        self.angel.brain.load_nn_from_file("agents/best_angel.json")

        while not self.quit and not self.done:
            self.rounds_played = 0

            for i in range(100):
                print("Trial: " + str(i))
                for j in range(100):
                    self.new_round_face_off()
                    self.play_round_face_off()

    def new_round(self):
        valid_map = False
        self.board = np.zeros((num_cells + 10, num_cells + 10))

        test_bomb = Bomb(randint(0, num_cells - 2), randint(0, num_cells - 2))
        attempts = 0

        while not valid_map:
            test_rob_x = randint(0, num_cells - 2)
            test_rob_y = randint(0, num_cells - 2)
            self.robot.x = test_rob_x
            self.robot.y = test_rob_y

            if self.devil.can_win(self.robot, test_bomb):
                valid_map = True
                self.bomb.x = test_bomb.x
                self.bomb.y = test_bomb.y
                self.board[test_bomb.x][test_bomb.y] = 1

            attempts += 1

            if attempts > 100:
                test_bomb = Bomb(randint(0, num_cells - 2), randint(0, num_cells - 2))

            for i in range(population_size):
                self.robot.x = test_rob_x
                self.robot.y = test_rob_y

            for i in range(population_size):
                self.devil.distance_updated = False
                self.angel.distance_updated = False

    def new_round_face_off(self):
        self.bomb = Bomb(randint(0, num_cells), randint(0, num_cells))
        self.robot = Robot(randint(0, num_cells), randint(0, num_cells))

    def play_round(self):
        self.turns = 0

        self.round_complete = False

        if graphics:
            self.clock.tick(FPS)

        while not self.round_complete and not self.quit:
            if graphics:
                self.clock.tick(FPS)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.quit = True

                self.screen.fill(LIGHT_GRAY)
                draw_grid(self.screen)
                draw_sprite(self.screen, self.bomb.color, self.bomb.x, self.bomb.y)

            if (self.turns % 2 == 0 and self.devil_first) or (self.turns % 2 == 1 and not self.devil_first):
                agent = self.devil
            else:
                agent = self.angel

            if self.devil.can_win(self.robot, self.bomb) and not self.robot.at_bomb(self.bomb):
                delta_x, delta_y = agent.move(get_agent_inputs(self.board, self.bomb, self.robot))

                self.robot.x += delta_x
                self.robot.y += delta_y
                if graphics:
                    draw_sprite(self.screen, agent.color, self.robot.x, self.robot.y)

                if self.round_complete and not agent.distance_updated:
                    self.round_complete = False

                if self.robot.x == self.bomb.x and self.robot.y == self.bomb.y:
                    if type(agent) == DevilAgent:
                        self.devil.bombs_detonated += 1
                        self.round_complete = True
            else:
                self.round_complete = True
                if graphics:
                    draw_sprite(self.screen, BLACK, self.robot.x, self.robot.y)

            self.turns += 1
            if graphics:
                self.display_stats()
                pg.display.update()

    def play_round_face_off(self):
        pass

    def get_agent_inputs(self, robot):
        x_dist = abs(robot.x - self.bomb.x)
        y_dist = abs(robot.y - self.bomb.y)
        cell_1 = self.board[robot.x + 1][robot.y]
        cell_2 = self.board[robot.x + 1][robot.y - 1]
        cell_3 = self.board[robot.x + 2][robot.y]
        cell_4 = self.board[robot.x + 2][robot.y - 1]
        cell_5 = self.board[robot.x + 2][robot.y - 2]
        cell_6 = self.board[robot.x + 3][robot.y]
        cell_7 = self.board[robot.x + 3][robot.y - 1]
        cell_8 = self.board[robot.x + 3][robot.y - 2]
        cell_9 = self.board[robot.x + 3][robot.y - 3]
        cell_10 = self.board[robot.x + 4][robot.y]
        cell_11 = self.board[robot.x + 4][robot.y - 1]
        cell_12 = self.board[robot.x + 4][robot.y - 2]
        cell_13 = self.board[robot.x + 4][robot.y - 3]
        cell_14 = self.board[robot.x + 4][robot.y - 4]
        inputs = np.array([x_dist, y_dist, cell_1, cell_2, cell_3, cell_4,
                           cell_5, cell_6, cell_7, cell_8, cell_9, cell_10,
                           cell_11, cell_12, cell_13, cell_14])
        return inputs

    def display_stats(self):
        lines = [gen_text(self.font, "Round: " + str(self.rounds_played)),
                 gen_text(self.font, "Bombs detonated: " + str(self.devil.bombs_detonated))]

        for line in range(len(lines)):
            self.screen.blit(lines[line], (100, line * 25 + 50))
