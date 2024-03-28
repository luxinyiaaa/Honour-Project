import random


class Particle:
    def __init__(self, img_num, transferred_data, page_load_time, ram_usage, change_number):
        self.img_num = img_num
        # "Change image format", "Compress image","Asynchronous loading of non-core files" , "Move JavaScript to the bottom"
        self.position = [random.randint(0, 1) for _ in range(4)] + [random.randint(0, 1) for _ in range(img_num)]
        self.velocity = [random.random() for _ in range(4 + img_num)]
        self.best_position = list(self.position)
        self.fitness = self.evaluate_fitness(transferred_data, page_load_time, ram_usage, change_number)
        self.best_fitness = self.fitness

    def evaluate_fitness(self, transferred_data, page_load_time, ram_usage, change_number):
        actions_sum = sum(self.position[:6])
        img_actions_sum = sum(self.position[6:])
        fitness = (transferred_data * img_actions_sum + change_number) / (page_load_time + ram_usage + 1)
        return fitness


def update_velocity(particle, global_best_position, w=0.5, c1=1, c2=1):
    for i in range(len(particle.velocity)):
        r1 = random.random()
        r2 = random.random()
        cognitive_velocity = c1 * r1 * (particle.best_position[i] - particle.position[i])
        social_velocity = c2 * r2 * (global_best_position[i] - particle.position[i])
        particle.velocity[i] = w * particle.velocity[i] + cognitive_velocity + social_velocity


def update_position(particle):
    for i in range(len(particle.position)):
        particle.position[i] += particle.velocity[i]
        if particle.position[i] > 1:
            particle.position[i] = 1
        elif particle.position[i] < 0:
            particle.position[i] = 0
        particle.position[i] = round(particle.position[i])


def run_pso(population, transferred_data, page_load_time, ram_usage, change_number, iterations=50):
    global_best_fitness = float('-inf')
    global_best_position = None

    for particle in population:
        if particle.fitness > global_best_fitness:
            global_best_fitness = particle.fitness
            global_best_position = list(particle.position)

    for _ in range(iterations):
        for particle in population:
            update_velocity(particle, global_best_position)
            update_position(particle)
            particle.fitness = particle.evaluate_fitness(transferred_data, page_load_time, ram_usage, change_number)

            if particle.fitness > particle.best_fitness:
                particle.best_fitness = particle.fitness
                particle.best_position = list(particle.position)

                if particle.fitness > global_best_fitness:
                    global_best_fitness = particle.fitness
                    global_best_position = list(particle.position)

    return global_best_position, global_best_fitness


def main():
    img_num = 10
    transferred_data = 9700
    page_load_time = 85
    ram_usage = 5100
    change_number = 3

    pop_size = 20
    population = [Particle(img_num, transferred_data, page_load_time, ram_usage, change_number) for _ in
                  range(pop_size)]
    best_position, best_fitness = run_pso(population, transferred_data, page_load_time, ram_usage, change_number)

    print("Best Solution:")
    print(f"Actions: {best_position[:4]}")
    print(f"Image Actions: {best_position[6:]}")
    print(f"Fitness Score: {best_fitness}")


if __name__ == "__main__":
    main()
