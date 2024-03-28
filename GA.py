import random

class Solution:
    def __init__(self, img_num, transferred_data, page_load_time, ram_usage, change_number):
        self.img_num = img_num
        # actions: the array to show 4 actions, they are
        # "Change image format", "Compress image","Asynchronous loading of non-core files" , "Move JavaScript to the bottom"
        self.actions = [random.randint(0, 1) for _ in range(4)]\

        self.actions_img = [random.randint(0, 1) for _ in range(img_num)]
        self.fitness_transferred_data = transferred_data
        self.fitness_page_load_time = page_load_time
        self.fitness_ram = ram_usage
        self.fitness_change_number = change_number
        self.fitness = 0

    def evaluate_fitness(self):

        self.fitness = (self.fitness_transferred_data * sum(self.actions_img) + self.fitness_change_number) / \
                       (self.fitness_page_load_time + self.fitness_ram + 1)  # Add 1 to avoid dividing by 0

def create_initial_population(size, img_num, transferred_data, page_load_time, ram_usage, change_number):
    return [Solution(img_num, transferred_data, page_load_time, ram_usage, change_number) for _ in range(size)]

def tournament_selection(population, k=3):
    selected = random.sample(population, k)
    winner = max(selected, key=lambda x: x.fitness)
    return winner

def crossover(parent1, parent2):
    child = Solution(parent1.img_num, parent1.fitness_transferred_data, parent1.fitness_page_load_time,
                     parent1.fitness_ram, parent1.fitness_change_number)
    # 实现一种更混合的交叉方式
    for i in range(len(parent1.actions)):
        child.actions[i] = parent1.actions[i] if random.random() > 0.5 else parent2.actions[i]
    for i in range(parent1.img_num):
        child.actions_img[i] = parent1.actions_img[i] if random.random() > 0.5 else parent2.actions_img[i]
    child.evaluate_fitness()
    return child

def mutate(solution, mutation_rate):
    # 为每个基因位实现变异
    for i in range(len(solution.actions)):
        if random.random() < mutation_rate:
            solution.actions[i] = 1 - solution.actions[i]
    for i in range(len(solution.actions_img)):
        if random.random() < mutation_rate:
            solution.actions_img[i] = 1 - solution.actions_img[i]
    solution.evaluate_fitness()

def run_genetic_algorithm(population, generations=50, elitism_size=2, base_mutation_rate=0.05):
    for generation in range(generations):
        # 计算适应度
        for solution in population:
            solution.evaluate_fitness()

        population.sort(key=lambda x: x.fitness, reverse=True)

        next_generation = population[:elitism_size]

        while len(next_generation) < len(population):
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)
            child = crossover(parent1, parent2)

            # 根据代数动态调整变异率
            mutation_rate = base_mutation_rate + 0.02 * (generation // 10)  # 每10代提高变异率
            mutate(child, mutation_rate)

            next_generation.append(child)

        population = next_generation

    print(f"Generation {generation}: Best Fitness = {population[0].fitness}")

    return population[0]

def main():
    img_num = 8
    transferred_data = 9700
    page_load_time = 85
    ram_usage = 5100
    change_number = 3

    pop_size = 20
    population = create_initial_population(pop_size, img_num, transferred_data, page_load_time, ram_usage, change_number)
    best_solution = run_genetic_algorithm(population, generations=50, elitism_size=2, base_mutation_rate=0.05)

    print("Best Solution:")
    print(f"Actions: {best_solution.actions}")
    print(f"Image Actions: {best_solution.actions_img}")
    print(f"Fitness Score: {best_solution.fitness}")

if __name__ == "__main__":
    main()
