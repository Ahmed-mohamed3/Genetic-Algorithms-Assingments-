import numpy as np
#read text from file
file = open("knapsack_input.txt", "r")
# put each line into a list
lines = file.readlines()
# close the file
file.close()
#delete all empty lines
lines = [line for line in lines if line.strip() != '']
i=0
for line in lines:
    lines[i] = line.strip()
    i+=1

num_knapsacks = int(lines[0])

def create_knapsacks(num_knapsacks):
    knapsacks = []
    for i in range(num_knapsacks):
        knapsacks.append([])
    num_items_pos = 1
    for knapsack in knapsacks:
        num_items = int(lines[num_items_pos])
        max_weight = int(lines[num_items_pos+1])
        knapsack.append(num_items)
        knapsack.append(max_weight)
        num_items_pos += 2
        for i in range(num_items):
            item = lines[num_items_pos].split()
            item = [int(item[0]), int(item[1])]
            knapsack.append(item)
            num_items_pos += 1
    return knapsacks

def create_population(knapsack):
    population = []
    num_items = knapsack[0]
    num_populations = 2**num_items
    num_samples = np.ceil(int(num_populations/4))
    if num_samples > 4096:
        num_samples = 4096
    i = 0
    while i != num_samples:
        if num_items < 31:
            number = np.random.randint(0, num_populations)
            binary_string = bin(number)[2:]
            len_binary_string = len(binary_string)
            needed_zeros = num_items - len_binary_string
            if needed_zeros > 0:
                binary_string = '0' * needed_zeros + binary_string
            #add 0's to the front of the string
            if number not in population:
                population.append(binary_string)
                i += 1
        else:
            number = np.random.randint(0, 2**25)
            binary_string_1 = bin(number)[2:]
            remaining = num_items - 25
            len_binary_string_1 = len(binary_string_1)
            needed_zeros = 25 - len_binary_string_1
            if needed_zeros > 0:
                binary_string_1 = '0' * needed_zeros + binary_string_1
            number = np.random.randint(0, 2**remaining)
            binary_string_2 = bin(number)[2:]
            len_binary_string_2 = len(binary_string_2)
            needed_zeros = remaining - len_binary_string_2
            if needed_zeros > 0:
                binary_string_2 = '0' * needed_zeros + binary_string_2
            binary_string = binary_string_1 + binary_string_2
            if binary_string not in population:
                population.append(binary_string)
                i += 1
    
    return population

def fitness(knapsack, population):
    fitness = []
    for individual in population:
        weight = 0
        value = 0
        for i in range(len(individual)):
            if individual[i] == '1':
                weight += knapsack[i+2][0]
                value += knapsack[i+2][1]
        if weight > knapsack[1]:
            fitness.append(0)
        else:
            fitness.append(value)
    return fitness

def choose_parents(population, fitness):
    parents = []
    sum_fitness = sum(fitness)
    probabiities_of_parents = np.array(fitness)/sum_fitness
    i = 0
    while i != (len(population)//2):
        parent_1 = np.random.choice(population, p=probabiities_of_parents,replace=False)
        parent_2 = np.random.choice(population, p=probabiities_of_parents,replace=False)
        if [parent_1, parent_2] not in parents:
            parents.append([parent_1, parent_2])
            i += 1

    return parents

def one_point_crossover(parents):
    children = []
    probability_of_crossover = 0.6
    is_cross = np.random.choice([0,1], p=[1-probability_of_crossover, probability_of_crossover], size=len(parents))
    i = 0
    for parent in parents:
        parent_1 = parent[0]
        parent_2 = parent[1]
        if is_cross[i] == 1:
            crossover_point = np.random.randint(1, len(parent_1))
            child_1 = parent_1[:crossover_point] + parent_2[crossover_point:]
            child_2 = parent_2[:crossover_point] + parent_1[crossover_point:]
            children.append(child_1)
            children.append(child_2)
    return children

def mutation(children):
    probability_of_mutation = 0.01
    is_mutated = np.random.choice([0,1], p=[1-probability_of_mutation, probability_of_mutation], size=len(children))
    i = 0
    for child in children:
        if is_mutated[i] == 1:
            mutation_point = np.random.randint(0, len(child))
            if child[mutation_point] == '1':
                child = child[:mutation_point] + '0' + child[mutation_point+1:]
            else:
                child = child[:mutation_point] + '1' + child[mutation_point+1:]
        i += 1
    return children

def is_feasible(knapsack, children):
    is_feasible = []
    for child in children:
        weight = 0
        for i in range(len(child)):
            if child[i] == '1':
                weight += knapsack[i+2][0]
        if weight <= knapsack[1]:
            is_feasible.append(1)
        else:
            is_feasible.append(0)
    return is_feasible



# use Generational replacement:
def generational_replacement(knapsack, population, fitness_children,fitness, children, is_feasible):
    new_population = []
    new_fitness = []
    for i in range(len(children)):
        if is_feasible[i] == 1:
            new_population.append(children[i])
            new_fitness.append(fitness_children[i])
    for i in range(len(population)):
        if fitness[i] not in new_fitness:
            new_population.append(population[i])
            new_fitness.append(fitness[i])
    return new_population, new_fitness 




def replacement(knapsack, population, fitness, children, is_feasible):
    new_population = []
    new_fitness = []

    for i in range(len(children)):
        if is_feasible[i] == 1:
            new_population.append(children[i])
            new_fitness.append(fitness(children[i]))
    for i in range(len(population)):
        if population[i] not in new_population:
            new_population.append(population[i])
            new_fitness.append(fitness(population[i]))
    if len(new_population) > len(population):
        new_population = new_population[:len(population)]
        new_fitness = new_fitness[:len(population)]
    return new_population, new_fitness



knapsacks = create_knapsacks(num_knapsacks)
populations = []
x = 0
for knapsack in knapsacks:
    populations.append(create_population(knapsack))

    fitness_list = fitness(knapsack, populations[-1])
    parents = choose_parents(populations[-1], fitness_list)
    children = one_point_crossover(parents)
    children = mutation(children)
    is_feasible_list = is_feasible(knapsack, children)
    fitness_children = fitness(knapsack, children)
    populations[-1], fitness_list = generational_replacement(knapsack, populations[-1], fitness_children, fitness_list, children, is_feasible_list)
    for i in range(10):
        parents = choose_parents(populations[-1], fitness_list)
        children = one_point_crossover(parents)
        children = mutation(children)
        is_feasible_list = is_feasible(knapsack, children)
        fitness_children = fitness(knapsack, children)
        populations[-1], fitness_list = generational_replacement(knapsack, populations[-1], fitness_children, fitness_list, children, is_feasible_list)
    #print(max(fitness_list),populations[-1][np.argmax(fitness_list)])
    maximum_weight = max(fitness_list)
    answer = populations[-1][np.argmax(fitness_list)]
    num_in_answer = 0
    z = []
    f = 0
    for i in answer:
        if i == "1":
            z.append([knapsack[f+2][0],knapsack[f+2][1]])
            num_in_answer += 1
        f += 1

    

            

    output ="This is test case " + str(x+1) + "\n" + str(num_in_answer) + "\n" + str(maximum_weight) + "\n"
    for f in z:
        output += str(f[0]) + " " + str(f[1]) +"\n"
    x += 1
    print(output)  