import json

import numpy as np
from constants import *


class NeuralNetwork:
    def __init__(self, in_size=input_layer_size,
                 hidden_size=hidden_layer_size,
                 out_size=output_layer_size):
        self.input_layer_size = in_size
        self.hidden_layer_size = hidden_size
        self.output_layer_size = out_size

        self.hidden_layer = np.zeros(self.hidden_layer_size)
        self.output_layer = np.zeros(self.output_layer_size)

        self.input_hidden_weights = np.random.uniform(-1, 1, (self.input_layer_size, self.hidden_layer_size))
        self.hidden_output_weights = np.random.uniform(-1, 1, (self.hidden_layer_size, self.output_layer_size))

        self.hidden_biases = np.random.uniform(-1, 1, self.hidden_layer_size)
        self.output_biases = np.random.uniform(-1, 1, self.output_layer_size)

    def predict(self, inputs):
        self.hidden_layer = inputs.dot(self.input_hidden_weights) + self.hidden_biases
        self.hidden_layer = sigmoid(self.hidden_layer)
        self.output_layer = self.hidden_layer.dot(self.hidden_output_weights) + self.output_biases
        self.output_layer = softmax(self.output_layer)

    def flatten_weights(self):
        input_hidden_weights_flat = self.input_hidden_weights.flatten()
        hidden_biases_flat = self.hidden_biases.flatten()
        hidden_output_weights_flat = self.hidden_output_weights.flatten()
        output_biases_flat = self.output_biases.flatten()
        return np.concatenate([input_hidden_weights_flat,
                               hidden_biases_flat,
                               hidden_output_weights_flat,
                               output_biases_flat])

    def reshape_weights(self, flattened_weights):
        input_hidden_index = self.input_layer_size * self.hidden_layer_size
        hidden_bias_index = input_hidden_index + self.hidden_layer_size
        hidden_output_index = hidden_bias_index + self.hidden_layer_size * self.output_layer_size

        temp = np.split(flattened_weights, (input_hidden_index, hidden_bias_index, hidden_output_index, ))

        self.input_hidden_weights = np.reshape(temp[0], (self.input_layer_size, self.hidden_layer_size))
        self.hidden_biases = temp[1]
        self.hidden_output_weights = np.reshape(temp[2], (self.hidden_layer_size, self.output_layer_size))
        self.output_biases = temp[3]

    def load_nn_from_file(self, file_name):
        with open(file_name, 'r') as file:
            nn_dict = json.load(file)
            input_hidden_weights = nn_dict["ihw"]
            hidden_biases = nn_dict["hb"]
            hidden_output_weights = nn_dict["how"]
            output_biases = nn_dict["ob"]
            self.input_hidden_weights = np.array(input_hidden_weights)
            self.hidden_biases = np.array(hidden_biases)
            self.hidden_output_weights = np.array(hidden_output_weights)
            self.output_biases = np.array(output_biases)

    def save_nn_to_file(self, file_name):
        agent_dict = {"ihw": self.input_hidden_weights.tolist(),
                      "hb": self.hidden_biases.tolist(),
                      "how": self.hidden_output_weights.tolist(),
                      "ob": self.output_biases.tolist()}
        with open(file_name, 'w+') as file:
            json.dump(agent_dict, file, indent=4)


# Activation functions
def sigmoid(input_value):
    return 1 / (1 + np.exp(input_value * -1))


def softmax(arr):
    e = np.exp(arr)
    return e / e.sum()
