import math
import random
from NeuralNetwork import *


class GeneticAlgorithm:
    @staticmethod
    def cross_over(parent1, parent2):
        child1 = NeuralNetwork()
        child2 = NeuralNetwork()

        crossover_percentage = random.uniform(0.1, 0.9)
        crossover_point = math.floor(hidden_layer_size * crossover_percentage)

        child1_ih_from_first_parent = parent1.input_hidden_weights.transpose()[:crossover_point, ]
        child1_ih_from_second_parent = parent2.input_hidden_weights.transpose()[crossover_point:, ]
        child1.input_hidden_weights = np.concatenate((child1_ih_from_first_parent, child1_ih_from_second_parent),
                                                     axis=0).transpose()

        child2_ih_from_first_parent = parent2.input_hidden_weights.transpose()[:crossover_point, ]
        child2_ih_from_second_parent = parent1.input_hidden_weights.transpose()[crossover_point:, ]
        child2.input_hidden_weights = np.concatenate((child2_ih_from_first_parent, child2_ih_from_second_parent),
                                                     axis=0).transpose()

        child1_hidden_biases_from_first_parent = parent1.hidden_biases[:crossover_point]
        child1_hidden_biases_from_second_parent = parent2.hidden_biases[crossover_point:]
        child1.hidden_biases = np.concatenate((child1_hidden_biases_from_first_parent,
                                               child1_hidden_biases_from_second_parent))

        child2_hidden_biases_from_first_parent = parent1.hidden_biases[crossover_point:]
        child2_hidden_biases_from_second_parent = parent2.hidden_biases[:crossover_point]
        child2.hidden_biases = np.concatenate((child2_hidden_biases_from_first_parent,
                                               child2_hidden_biases_from_second_parent))

        if crossover_percentage > 0.75:
            child1.hidden_output_weights = parent1.hidden_output_weights.copy()
            child1.output_biases = parent1.output_biases.copy()
            child2.hidden_output_weights = parent2.hidden_output_weights.copy()
            child2.output_biases = parent2.output_biases.copy()
        elif crossover_percentage > 0.25:
            child1_ho_from_first_parent = parent1.hidden_output_weights.transpose()[:1, ]
            child1_ho_from_second_parent = parent2.hidden_output_weights.transpose()[1:, ]
            child1.output_biases = np.concatenate((parent1.output_biases[:1],
                                                   parent2.output_biases[1:]))

            child2_ho_from_first_parent = parent2.hidden_output_weights.transpose()[:1, ]
            child2_ho_from_second_parent = parent1.hidden_output_weights.transpose()[1:, ]
            child2.output_biases = np.concatenate((parent2.output_biases[:1],
                                                   parent1.output_biases[1:]))

            child1.hidden_output_weights = np.concatenate((child1_ho_from_first_parent, child1_ho_from_second_parent),
                                                          axis=0).transpose()
            child2.hidden_output_weights = np.concatenate((child2_ho_from_first_parent, child2_ho_from_second_parent),
                                                          axis=0).transpose()
        else:
            child1.hidden_output_weights = parent2.hidden_output_weights.copy()
            child1.output_biases = parent2.output_biases.copy()
            child2.hidden_output_weights = parent1.hidden_output_weights.copy()
            child2.output_biases = parent1.output_biases.copy()

        return child1, child2

    @staticmethod
    def mutate(a):
        for i in range(len(a)):
            if random.random() >= mutation_rate:
                a[i] += random.gauss(0, 0.05)

        return a
