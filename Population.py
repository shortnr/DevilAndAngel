import copy
from GeneticAlgorithm import *
from Agents import *


class Population:
    def __init__(self, pop_type):
        self.pop_type = pop_type
        self.population = []
        self.generation = 0

        for i in range(population_size):
            nn = NeuralNetwork(input_layer_size, hidden_layer_size, output_layer_size)
            if self.pop_type == "devil":
                self.population.append([DevilAgent(nn), True, 1000])
            elif self.pop_type == "angel":
                self.population.append([AngelAgent(nn), True, 1000])

        self.best = self.population[0][0]

    def new_generation(self):
        num_parents = int(len(self.population) * 0.05)
        parents = self.population[:num_parents]
        parents_flat = []
        new_gen = []
        probabilities = []

        # Add the original parents
        for i in range(len(parents)):
            new_gen.append([parents[i][0], True, 1000])

        # Deep copy parents, mutate them, and append to new gen
        parents = copy.deepcopy(parents)

        for i in range(len(parents)):
            parents_flat.append(parents[i][0])
            probabilities.append(parents[i][2])
            parent_flat = parents[i][0].brain.flatten_weights()
            new_genome = GeneticAlgorithm.mutate(parent_flat)
            new_nn = NeuralNetwork(input_layer_size, hidden_layer_size, output_layer_size)
            new_nn.reshape_weights(new_genome)

            if self.pop_type == 'devil':
                new_child = DevilAgent(new_nn)
            else:
                new_child = AngelAgent(new_nn)
            new_gen.append([new_child, True, 1000])

        probabilities = softmax(probabilities)

        while len(new_gen) < population_size:
            different_parents = False
            chosen_parents = None
            while not different_parents:
                chosen_parents = np.random.choice(parents_flat, 2, probabilities.tolist())
                if chosen_parents[0] is not chosen_parents[1]:
                    different_parents = True

            child_one, child_two = GeneticAlgorithm.cross_over(
                chosen_parents[0].brain, chosen_parents[1].brain)

            if self.pop_type == 'devil':
                child_one_agent = DevilAgent(child_one)
                child_two_agent = DevilAgent(child_two)
            else:
                child_one_agent = AngelAgent(child_one)
                child_two_agent = AngelAgent(child_two)

            new_gen.append([child_one_agent, True, 1000])
            new_gen.append([child_two_agent, True, 1000])

        self.best = new_gen[0][0]

    def save_generation(self):
        for i in range(population_size):
            file_name = self.pop_type + '_pop/' + self.pop_type + str(i) + '.json'
            self.population[i][0].brain.save_nn_to_file(file_name)

    def load_generation(self):
        self.population = []
        for i in range(population_size):
            file_name = self.pop_type + '_pop/' + self.pop_type + str(i) + '.json'
            with open(file_name, 'r') as file:
                agent_dict = json.load(file)
                input_hidden_weights = agent_dict["ihw"]
                hidden_biases = agent_dict["hb"]
                hidden_output_weights = agent_dict["how"]
                output_biases = agent_dict["ob"]
                agent_nn = NeuralNetwork()
                agent_nn.input_hidden_weights = np.array(input_hidden_weights)
                agent_nn.hidden_biases = np.array(hidden_biases)
                agent_nn.hidden_output_weights = np.array(hidden_output_weights)
                agent_nn.output_biases = np.array(output_biases)
                self.population.append([DevilAgent(agent_nn), True, 1000])

    @staticmethod
    def population_sort(e):
        return e[2]


class DevilPopulation(Population):
    def __init__(self):
        super().__init__("devil")
        self.bombs_this_gen = 0
        self.bombs_last_gen = 0
        self.most_bombs_last_gen = 0

    def calculate_fitnesses(self):
        exp_sum = 0
        self.most_bombs_last_gen = 0

        new_population = copy.deepcopy(self.population)

        for i in range(population_size):
            if new_population[i][0].total_distance == 0:
                new_population[i][2] = 10
            else:
                new_population[i][2] = np.exp(1 / new_population[i][0].total_distance)
            exp_sum += new_population[i][2]

            if new_population[i][0].bombs_detonated > self.most_bombs_last_gen:
                self.most_bombs_last_gen = new_population[i][0].bombs_detonated
            new_population[i][0].bombs_detonated = 0

        for i in range(population_size):
            temp = new_population[i][2] / exp_sum
            new_population[i][2] = temp

        new_population.sort(key=self.population_sort, reverse=True)

        self.population[0][0].brain.save_nn_to_file("devil_pop/best_devil.json")
        print("Current best Devil saved.")

        if self.generation == 0:
            self.population[population_size - 1][0].brain.save_nn_to_file("devil_pop/bad_devil.json")
            print("Worst Devil saved.")
            temp = 0
            for i in range(population_size):
                temp += self.population[i][2]
                if temp >= 0.5:
                    self.population[i][0].brain.save_nn_to_file("devil_pop/median_devil.json")
                    print("Median Devil saved.")
                    break

        self.population = new_population


class AngelPopulation(Population):
    def __init__(self):
        super().__init__("angel")
        self.worlds_saved_this_gen = 0
        self.worlds_saved_last_gen = 0
        self.least_bombs_last_gen = 0

    def calculate_fitnesses(self):
        exp_sum = 0
        self.least_bombs_last_gen = 0
        new_population = copy.deepcopy(self.population)

        greatest_distance = 0

        for i in range(population_size):
            if new_population[i][0].total_distance > greatest_distance:
                greatest_distance = new_population[i][0].total_distance

            if new_population[i][0].bombs_detonated < self.least_bombs_last_gen:
                self.least_bombs_last_gen = new_population[i][0].bombs_detonated
            new_population[i][0].bombs_detonated = 0

        for i in range(population_size):
            new_population[i][2] = np.exp(new_population[i][0].total_distance / greatest_distance)
            exp_sum += new_population[i][2]

        for i in range(population_size):
            new_population[i][2] = new_population[i][2] / exp_sum

        new_population.sort(key=self.population_sort, reverse=True)

        self.population[0][0].brain.save_nn_to_file("angel_pop/best_angel.json")
        print("Current best Angel saved.")

        if self.generation == 0:
            self.population[population_size - 1][0].brain.save_nn_to_file("angel_pop/bad_angel.json")
            print("Worst Angel saved.")
            temp = 0
            for i in range(population_size):
                temp += self.population[i][2]
                if temp >= 0.5:
                    self.population[i][0].brain.save_nn_to_file("angel_pop/median_angel.json")
                    print("Median Angel saved.")
                    break

        self.population = new_population
