import pygame.display
from random import randint
from Objects import *
from Population import *
from helper_functions import *


class Training:
    def __init__(self):
        pg.init()

        self.font = pg.font.SysFont('Ubuntu Mono, Bold', 24)
        self.screen = pygame.display.set_mode((window_width, window_height))
        self.board = np.zeros((board_width + 10, board_height + 10))
        self.devil_population = DevilPopulation()
        self.angel_population = AngelPopulation()
        self.opponent = self.angel_population.best
        self.robots = []
        self.bomb = Bomb()
        self.rounds_played = 0
        self.clock = pg.time.Clock()
        self.quit = False
        self.round_complete = False
        self.turns = 0
        self.devil_first = False

        for i in range(population_size):
            self.robots.append(Robot())

    def run(self):
        while not self.quit:
            if self.devil_population.generation == 50 and self.angel_population.generation == 50:
                print("Devil and Angel populations have reached 50 generations.")
                break

            self.rounds_played = 0

            while not self.quit and self.rounds_played < num_rounds_per_gen:
                self.new_round()
                self.play_round()
                self.rounds_played += 1

            if type(self.opponent) is DevilAgent:
                self.angel_population.calculate_fitnesses()
                self.angel_population.new_generation()
                self.angel_population.worlds_saved_last_gen = self.angel_population.worlds_saved_this_gen
                self.angel_population.worlds_saved_this_gen = 0
                if not self.quit:
                    self.angel_population.save_generation()
                self.angel_population.generation += 1
                self.opponent = self.angel_population.best
            else:
                self.devil_population.calculate_fitnesses()
                self.devil_population.new_generation()
                self.devil_population.bombs_last_gen = self.devil_population.bombs_this_gen
                self.devil_population.bombs_this_gen = 0
                if not self.quit:
                    self.devil_population.save_generation()
                self.devil_population.generation += 1
                self.opponent = self.devil_population.best

        pg.quit()

    def new_round(self):
        valid_map = False
        self.board = np.zeros((num_cells + 10, num_cells + 10))

        test_bomb = Bomb(randint(0, num_cells - 2), randint(0, num_cells - 2))
        attempts = 0

        while not valid_map:
            test_rob_x = randint(0, num_cells - 2)
            test_rob_y = randint(0, num_cells - 2)
            self.robots[0].x = test_rob_x
            self.robots[0].y = test_rob_y

            if self.devil_population.population[0][0].can_win(self.robots[0], test_bomb):
                valid_map = True
                self.bomb.x = test_bomb.x
                self.bomb.y = test_bomb.y
                self.board[test_bomb.x][test_bomb.y] = 1

            attempts += 1

            if attempts > 100:
                test_bomb = Bomb(randint(0, num_cells - 2), randint(0, num_cells - 2))

            for i in range(population_size):
                self.robots[i].x = test_rob_x
                self.robots[i].y = test_rob_y

            for i in range(population_size):
                self.devil_population.population[i][0].distance_updated = False
                self.angel_population.population[i][0].distance_updated = False

    def play_round(self):
        self.turns = 0

        self.round_complete = False

        self.clock.tick(FPS)

        if type(self.opponent) is AngelAgent:
            current_population = self.devil_population.population
        else:
            current_population = self.angel_population.population

        while not self.round_complete and not self.quit:
            self.round_complete = True
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit = True

            self.screen.fill(LIGHT_GRAY)
            draw_grid(self.screen)
            draw_sprite(self.screen, self.bomb.color, self.bomb.x, self.bomb.y)

            for i in range(population_size):
                if type(self.opponent) is DevilAgent:
                    devil = self.opponent
                    angel = current_population[i][0]
                    agent = angel
                else:
                    devil = current_population[i][0]
                    angel = self.opponent
                    agent = devil

                if devil.can_win(self.robots[i], self.bomb) and not self.robots[i].at_bomb(self.bomb):
                    if self.turns % 2 == 0:
                        if self.devil_first:
                            delta_x, delta_y = devil.move(get_agent_inputs(self.board, self.bomb, self.robots[i]))
                            color = devil.color
                        else:
                            delta_x, delta_y = angel.move(get_agent_inputs(self.board, self.bomb, self.robots[i]))
                            color = angel.color
                    else:
                        if self.devil_first:
                            delta_x, delta_y = angel.move(get_agent_inputs(self.board, self.bomb, self.robots[i]))
                            color = angel.color
                        else:
                            delta_x, delta_y = devil.move(get_agent_inputs(self.board, self.bomb, self.robots[i]))
                            color = devil.color

                    self.robots[i].x += delta_x
                    self.robots[i].y += delta_y
                    draw_sprite(self.screen, color, self.robots[i].x, self.robots[i].y)

                    if self.round_complete and not agent.distance_updated:
                        self.round_complete = False
                else:
                    draw_sprite(self.screen, BLACK, self.robots[i].x, self.robots[i].y)
                    if not agent.distance_updated:
                        agent.distance_updated = True
                        robot_pos = np.array((self.robots[i].x, self.robots[i].y))
                        bomb_pos = np.array((self.bomb.x, self.bomb.y))
                        agent.total_distance += np.linalg.norm(robot_pos - bomb_pos)
                        if self.robots[i].x == self.bomb.x and self.robots[i].y == self.bomb.y:
                            if type(agent) == DevilAgent:
                                self.devil_population.bombs_this_gen += 1
                                agent.bombs_detonated += 1
                        elif type(agent) == AngelAgent:
                            self.angel_population.worlds_saved_this_gen += 1

            self.turns += 1
            self.display_stats()
            pg.display.update()

    def display_stats(self):
        lines = [gen_text(self.font, "Round: " + str(self.rounds_played)),
                 gen_text(self.font, "The " + type(self.opponent).__name__[:5] + " is the static agent."),
                 gen_text(self.font, ""), gen_text(self.font, "Current Devil generation: " +
                                                   str(self.devil_population.generation)),
                 gen_text(self.font, "Times humanity destroyed this generation: " +
                          str(self.devil_population.bombs_this_gen)),
                 gen_text(self.font, "Times humanity destroyed last generation: " +
                          str(self.devil_population.bombs_last_gen)),
                 gen_text(self.font, "Best individual bomb detonations last generation: " +
                          str(self.devil_population.most_bombs_last_gen)), gen_text(self.font, ""),
                 gen_text(self.font, "Current Angel generation: " + str(self.angel_population.generation)),
                 gen_text(self.font, "Times humanity saved this generation: " +
                          str(self.angel_population.worlds_saved_this_gen)),
                 gen_text(self.font, "Times humanity saved last generation: " +
                          str(self.angel_population.worlds_saved_last_gen)),
                 gen_text(self.font, "Most individual worlds saved last generation: " +
                          str(self.angel_population.least_bombs_last_gen))]

        for line in range(len(lines)):
            self.screen.blit(lines[line], (100, line * 25 + 50))
