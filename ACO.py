import random

class Ant:
    def __init__(self, num_nodes, img_num):
        # actions: the array to show 4 actions, they are
        # "Change image format", "Compress image","Asynchronous loading of non-core files" , "Move JavaScript to the bottom"
        self.actions = []
        self.actions_img = []
        self.fitness = 0

    def select_actions(self, pheromone_global, pheromone_img, alpha=1, beta=1):
        self.actions = [1 if random.random() < pheromone_global[i] ** alpha / (pheromone_global[i] ** alpha
                                + (1 - pheromone_global[i]) ** beta) else 0 for i in range(len(pheromone_global))]
        self.actions_img = [1 if random.random() < pheromone_img[i] ** alpha / (pheromone_img[i] ** alpha
                                + (1 - pheromone_img[i]) ** beta) else 0 for i in range(len(pheromone_img))]

    def evaluate_fitness(self, transferred_data, page_load_time, ram_usage, change_number):
        self.fitness = (transferred_data * sum(self.actions_img) + change_number) / (page_load_time + ram_usage + 1)

class ACO:
    def __init__(self, num_nodes, img_num, num_ants, num_iterations, decay_rate, alpha=1, beta=1):
        self.num_nodes = num_nodes
        self.img_num = img_num
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.decay_rate = decay_rate
        self.alpha = alpha
        self.beta = beta
        self.pheromone_global = [0.5 for _ in range(num_nodes)]
        self.pheromone_img = [0.5 for _ in range(img_num)]
        self.ants = [Ant(num_nodes, img_num) for _ in range(num_ants)]
        self.best_ant = Ant(num_nodes, img_num)
        self.best_ant.fitness = float('-inf')

    def update_pheromones(self):
        for i in range(self.num_nodes):
            for ant in self.ants:
                if ant.actions[i] == 1:
                    self.pheromone_global[i] = (1 - self.decay_rate) * self.pheromone_global[i] + self.decay_rate * ant.fitness
        for i in range(self.img_num):
            for ant in self.ants:
                if ant.actions_img[i] == 1:
                    self.pheromone_img[i] = (1 - self.decay_rate) * self.pheromone_img[i] + self.decay_rate * ant.fitness

    def run(self):
        for iteration in range(self.num_iterations):
            # Dynamic decay rate adjustment
            self.decay_rate = 0.1 + (0.4 - 0.1) * (iteration / self.num_iterations)
            for ant in self.ants:
                ant.select_actions(self.pheromone_global, self.pheromone_img, self.alpha, self.beta)
                ant.evaluate_fitness(9700, 85, 5100, 3)
                if ant.fitness > self.best_ant.fitness:
                    self.best_ant = ant

            self.update_pheromones()

        print("Best Solution Actions:", self.best_ant.actions)
        print("Best Image Actions:", self.best_ant.actions_img)
        print("Best Fitness:", self.best_ant.fitness)

# Configuration
num_nodes = 4
img_num = 8
num_ants = 10
num_iterations = 100
decay_rate = 0.1

# Run ACO
aco = ACO(num_nodes, img_num, num_ants, num_iterations, decay_rate)
aco.run()
