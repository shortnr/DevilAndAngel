# Simulation settings
window_height = 1200
window_width = 2100
board_height = 1100
board_width = 1100

num_cells = 50

cell_height = int(board_height / num_cells)
cell_width = int(board_width / num_cells)
sprite_height = cell_height - 1
sprite_width = cell_width - 1

FPS = 1
num_rounds_per_gen = 100
graphics = False

WHITE = (255, 255, 255)
RED = (255, 0, 0, 100)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255, 127)
BLACK = (0, 0, 0)
LIGHT_GRAY = (175, 175, 175)
MEDIUM_GRAY = (125, 125, 125)

learning_mode = False
face_off_devil = 'median'
face_off_angel = 'median'

# NN settings
input_layer_size = 16
hidden_layer_size = 12
output_layer_size = 2

# GA settings
population_size = 250
mutation_rate = 0.05
