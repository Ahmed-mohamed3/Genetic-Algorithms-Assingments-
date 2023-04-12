import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def plot_polynomial(chromosome,points_x,points_y):
    plt.plot(points_x,points_y,'o')
    plt.plot(points_x,calculate_polynomial(chromosome,points_x))
    plt.show(block = True)

def read_file(file_name):
    file = open(file_name, "r")
    lines = file.readlines()
    file.close()
    lines = [line for line in lines if line.strip() != '']
    i=0
    for line in lines:
        lines[i] = line.strip()
        i+=1
    return lines

def parse_file(lines):
    points = {}
    degrees = {}
    first = True
    c = 0
    NUM_TESTS = int(lines[0])
    NUM_POINTS = int(lines[1].split()[0])
    DEGREE = int(lines[1].split()[1])
    counter = 2
    for i in range(NUM_TESTS):
        points_in_test = []
        degrees[i] = DEGREE
        my_list = []
        if first == True:
            c += 1
            for _ in range (NUM_POINTS):
                x = float(lines[counter].split()[0])
                y = float(lines[counter].split()[1])
                my_list.append([x,y])
                counter += 1
            first = False
        else :
            for _ in range (NUM_POINTS):
                x = float(lines[counter+c].split()[0])
                y = float(lines[counter+c].split()[1])
                my_list.append([x,y])
                counter +=1
            c += 1
        points[i] = my_list
        if i != NUM_TESTS -1 :
            NUM_POINTS = int(lines[counter+i].split()[0])
            DEGREE = int(lines[counter+i].split()[1])
    return points , degrees

def get_points_x_and_y(points):
    a = np.array(points)
    points_x = a[:,0]
    points_y = a[:,1]
    return points_x,points_y

def initialization(sample_size,degree,lower_bound= -10,upper_bound= 10):
    # Create sample_size chromosomes with degree genes in range [lower_bound,upper_bound]
    # Return a numpy array of shape (sample_size,degree+1) with random values in range [lower_bound,upper_bound]
    return np.random.uniform(lower_bound,upper_bound,(sample_size,degree+1))

def calculate_polynomial_test(chromosome, points_x):
    # Calculate the polynomial with the given chromosome and points_x
    # Chromosome shape is a 1D array of shape (degree+1,)
    # points_x shape is a 1D array of shape (num_points,)
    # Return a 1D array of shape (num_points,) with the calculated polynomial
    y_pred = np.zeros(len(points_x),dtype=float)
    for j in range(len(points_x)):
        number = points_x[j]
        sum = 0
        for i in range(len(chromosome)):
            a = chromosome[i]
            x = number
            value = a * (x**i)
            sum += value
        y_pred[j] = sum
    return y_pred

def calculate_polynomial(chromosome, points_x):
    return np.polyval(chromosome[::-1],points_x)

def mean_squared_error(y_true, y_pred):
    # Calculate the mean squared error between y_true and y_pred
    # y_true and y_pred are 1D arrays of shape (num_points,)
    # Return the mean squared error
    x = (y_pred-y_true)
    x = x**2
    ans = np.mean(x,axis=1)
    return ans

def get_fitness(chromosomes,points_x,points_y):
    # Calculate the fitness of the chromosome
    # Chromosome shape is a 1D array of shape (degree+1,)
    # points_x and points_y are 1D arrays of shape (num_points,)
    # Return the fitness
    all_y_pred = np.zeros((len(chromosomes),len(points_y)),dtype=float)
    for i in range(len(chromosomes)):
        y_pred = calculate_polynomial(chromosomes[i], points_x)
        all_y_pred[i] = y_pred
    return 1/mean_squared_error(points_y,all_y_pred)


def tournament_selection(number_of_tournament,chromosomes_per_tournament,chromosomes,points_x,points_y):
    # number_of_tournament is an integer representing the number of tournaments conducted leading to the selection of a single chromosome
    # chromosomes_per_tournament is an integer representing the number of chromosomes participating in each tournament
    # chromosomes shape is a 2D array of shape (sample_size,degree+1)
    # points_x and points_y are 1D arrays of shape (num_points,)
    # Return a 2D array of shape (number_of_tournament,degree+1) with the selected chromosomes
    selected_chromosomes = np.zeros((number_of_tournament,len(chromosomes[0])),dtype=float)
    for i in range(number_of_tournament):
        tournament_indices = np.random.randint(0,len(chromosomes),size=chromosomes_per_tournament)
        tournament = np.array(chromosomes)[tournament_indices].tolist()
        cumulative_fitness = get_fitness(tournament,points_x,points_y)
        selected_chromosomes[i] = tournament[np.argmax(cumulative_fitness)]
    return selected_chromosomes


def two_point_crossover(parent1,parent2,pc):
    # parent1 and parent2 are 1D arrays of shape (degree+1,)
    # Return 2 1D arrays of shape (degree+1,) with the children chromosomes
    probability_of_crossover = np.random.uniform()
    parent1 = parent1
    parent2 = parent2
    child_1 = parent1
    child_2 = parent2
    if probability_of_crossover > pc:
        index_1 = np.random.randint(0,len(parent1))
        index_2 = np.random.randint(0,len(parent1))
        if index_1 > index_2:
            index_1,index_2 = index_2,index_1
        if index_1 == index_2:
            if index_2 == len(parent1):
                index_1 -= np.random.randint(0,len(parent1) - 1)
            if index_2 == 0:
                index_2 += np.random.randint(0,len(parent1))
            else :
                index_1 -= np.random.randint(0,index_2)
        
        
        child_1 = np.concatenate((parent1[:index_1] , parent2[index_1:index_2] , parent1[index_2:]),axis=0) 
        child_2 = np.concatenate((parent2[:index_1] , parent1[index_1:index_2] , parent2[index_2:]),axis=0)
    return child_1,child_2

def marriage(selected_chromosomes,desired_offspring_size,pc):
    offspring = np.zeros((int(desired_offspring_size),len(selected_chromosomes[0])),dtype=float)
    for i in range(int(desired_offspring_size)-1):
        parent1 = selected_chromosomes[np.random.randint(0,len(selected_chromosomes))]
        parent2 =  selected_chromosomes[np.random.randint(0,len(selected_chromosomes))]
        child_1,child_2 = two_point_crossover(parent1,parent2,pc)
        offspring[i] = child_1
        offspring[i+1] = child_2
    return offspring

def non_uniform_mutation(chromosome,lower_bound,upper_bound,current_genration,max_generations,probability_of_mutation,b):
    for i in range(len(chromosome)):
        is_mutated = np.random.uniform()
        if probability_of_mutation > is_mutated :
            delta_L_Xi = chromosome[i] - lower_bound
            delta_U_Xi = upper_bound - chromosome[i]
            main_delta = -1
            r1 = np.random.uniform()
            if r1 <= 0.5:
                main_delta = delta_L_Xi
                r2 = np.random.uniform()
                delta_t_y = main_delta * (1 - pow(r2,pow(1-current_genration/max_generations,b)))
                chromosome[i] = chromosome[i] - delta_t_y
            else:
                main_delta = delta_U_Xi
                r2 = np.random.uniform()
                delta_t_y = main_delta * (1 - pow(r2,pow(1-current_genration/max_generations,b)))
                chromosome[i] = chromosome[i] + delta_t_y
    return chromosome
                
def elitisit_replacement_strategy(population,population_fitness,offspring,offspring_fitness):
    population_fitness = population_fitness
    offspring_fitness = offspring_fitness
    all_population = np.concatenate((population,offspring),axis=0)
    all_fitness = np.concatenate((population_fitness,offspring_fitness),axis=0)
    best_fitness = np.argsort(all_fitness)[::-1]
    best_fitness_indices = best_fitness[:len(population)]
    best_fitness = np.array(all_fitness)[best_fitness_indices]
    best_population = np.array(all_population)
    best_population = best_population[best_fitness_indices]
    best_fitness = best_fitness
    return best_population,best_fitness

def mean_squared_error_from_fitness(fitness):
    fitness = np.array(fitness)
    fitness = 1/fitness
    return fitness

def genetic_algorithim(population_size,degree,number_of_generations,lower_bound,upper_bound,number_of_tournaments,tournament_size,points,probability_of_mutation = 0.01,probability_of_crossover = 0.6,b = 2):
    population = initialization(population_size,degree,lower_bound,upper_bound)
    
    desired_offspring_size = population_size/4
    points_x, points_y = get_points_x_and_y(points)
    for current_generation in range(number_of_generations):
        population_fitness = get_fitness(population,points_x,points_y)
        selected_parents = tournament_selection(number_of_tournaments,tournament_size,population,points_x,points_y)
        offspring = marriage(selected_parents,desired_offspring_size,probability_of_crossover)
        for i in range(len(offspring)):
            offspring[i] = non_uniform_mutation(offspring[i],lower_bound,upper_bound,current_generation,number_of_generations,probability_of_mutation,b)
        offspring_fitness = get_fitness(offspring,points_x,points_y)
        population,population_fitness = elitisit_replacement_strategy(population,population_fitness,offspring,offspring_fitness)

    population_fitness = get_fitness(population,points_x,points_y)
    return population,population_fitness

def write_file(file_name,text):
    with open(file_name,"w") as f:
        f.write(text)


def create_points(points_zero_x,chromosome):
    points_zero_y_pred = []
    for x in points_zero_x:
        y_pred = 0
        for i in range(len(chromosome)):
            y_pred += chromosome[i] * pow(x,i)
        points_zero_y_pred.append(y_pred)
    return points_zero_y_pred

def runner():    
    File_NAME = "curve_fitting_input.txt"
    POPULATION_SIZE = 5000
    NUMBER_OF_GENERATIONS = 500
    LOWER_BOUND = -10
    UPPER_BOUND = 10
    NUMBER_OF_TOURNAMENTS = 100
    TOURNAMENT_SIZE = 50
    lines = read_file(File_NAME)
    points,degrees = parse_file(lines)
    NUM_TESTS = int(lines[0])
    SAVE_FILE = "Answer.txt"
    text = ""
    for i in range(NUM_TESTS):
        text += f"Sample {i+1} : \nBest Chromosome :"
        population,population_fitness = genetic_algorithim(POPULATION_SIZE,degrees[i],NUMBER_OF_GENERATIONS,LOWER_BOUND,UPPER_BOUND,NUMBER_OF_TOURNAMENTS,TOURNAMENT_SIZE,points[i])
        population_mean_squared_error = mean_squared_error_from_fitness(population_fitness)
        best_chromosome = population[np.argmax(population_fitness)]
        text += str(best_chromosome) + "\n" + "Best Mean Squared Error : " + str(population_mean_squared_error[np.argmax(population_fitness)]) + "\n"
        points_x_of_iter,points_y_of_iter = get_points_x_and_y(points[i])
        #plot_polynomial(best_chromosome,points_x_of_iter,points_y_of_iter)
    write_file(SAVE_FILE,text)

runner()

    