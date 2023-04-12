import numpy as np
import matplotlib.pyplot as plt 

#read text from file
file = open("curve_fitting_input.txt", "r")
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

def parsing(lines):
    num_tests = int(lines[0])
    num_points = int(lines[1].split()[0])
    counter = 2
    degree = int(lines[1].split()[1])
    points = []
    degrees = []
    first = True
    c = 0
    for i in range(num_tests):
        points_in_test = []
        degrees.append(degree)
        my_list = []
        
        if first == True:
            c+=1
            for w in range (num_points):
                my_list.append(lines[counter].split())
                counter += 1
            first = False
        else :
            for w in range (num_points):
                my_list.append(lines[counter+c].split())
                counter +=1
            c+=1

        points.append(my_list)

        if i != num_tests -1 :
            num_points = int(lines[counter+i].split()[0])
            degree = int(lines[counter+i].split()[1])
    return points , degrees

points  , degrees = parsing(lines)
for i in range(len(degrees)):
    degrees[i] += 1


def initialization(sample_size,degree,lower_bound= -10,upper_bound= 10):
    samples = []
    range_ = [lower_bound,upper_bound]
    for _ in range(sample_size):
        sample = []
        for i in range(degree):
            elem = np.random.uniform(lower_bound,upper_bound)
            sample.append(elem)
        samples.append(sample)
    return samples

def calc_equation(chromosomes,points,test):
    degree = len(chromosomes[0])
    final = []
    for counter in range (len(chromosomes)):
        results = []
        for j in range(len(points[test])):
            res = 0    
            for i in range(degree):
                x = float(points[test][j][0])
                res += chromosomes[counter][i] * pow(x,i)
            results.append(res)
        final.append(results)
    return final

def mean_squared_error(chromosomes,points,test):
    mse = []
    for i in range(len(chromosomes)):
        y_pred = calc_equation(chromosomes,points,test)
        x = points[test][:]
        y_actual = [y for w,y in x ]
        N = len(y_pred[0])
        mse.append((1/N) * np.sum(np.square(np.array(y_pred[i]) - (np.array(y_actual,dtype=float)))))
    return np.array(mse)

def fitness_fun(sample, points , test ):
    mse = mean_squared_error(chromosomes = sample , points = points , test = test )
    mse = 1/ np.array(mse)
    first  = True 
    for i in range (len(mse)):
        if first == True :
            mse[i] = mse[i]
            first = False
        else :
            mse[i] += mse[i-1]
    return mse
    


# perform tournament selection
def tournament_selection(sample,fitness,num_tournaments,tournament_size):
    selected = []
    for _ in range(num_tournaments):
        # select random indices
        indices = np.random.choice(len(sample),tournament_size,replace=False)
        # get the fitness values
        fitness_values = fitness[indices]
        # get the best index
        best_index = indices[np.argmin(fitness_values)]
        # add the best sample to the selected list
        selected.append(sample[best_index])
    return selected



#perform two points crossover
def two_points_crossover(parent1,parent2):
    # get the length of the parent
    length = len(parent1)
    # get the two points
    points = np.random.choice(length,2,replace=False)
    parent1 = list(parent1)
    parent2 = list(parent2)
        
    # sort the points
    points.sort()
    # get the start and end points
    start,end = points
    # create the children
    child1 = parent1[:start] + parent2[start:end] + parent1[end:]
    child2 = parent2[:start] + parent1[start:end] + parent2[end:]
    return child1,child2




# perform non_uniform_mutation 
def non_uniform_mutation(sample,current_generation,max_generation,lower_bound = -10 , upper_bound = 10,mutation_rate = 0.01,b=3):
    len_sample = len(sample)
    for i in range(len_sample):
        L_Xi = np.array(sample[i]) - lower_bound
        U_Xi = upper_bound - np.array(sample[i])
        if np.random.random() < mutation_rate:
            r = np.random.random()
            if r <= 0.5:
                sample[i] = np.array(sample[i]) - L_Xi * (1 - r**((1-current_generation/max_generation) ** b))
            else:
                sample[i] = np.array(sample[i]) + U_Xi * (1 - r**((1-current_generation/max_generation) ** b))
    return sample

# elitistreplacement
def elitist_replacement(sample,fitness,offspring,offspring_fitness):
    # get the indices of the best samples
    all_samples = list(sample) + list(offspring)
    all_fitness = list(fitness) + list(offspring_fitness)
    best_fitness = np.argsort(all_fitness)[:len(sample)]
    best_samples = np.array(all_samples)[best_fitness]

    return best_samples, best_fitness

points_zero = np.array(points[4], dtype = float)
points_zero_x = [x for x,y in points_zero]
points_zero_y = [y for x,y in points_zero]
#plt.plot(points_zero_x,points_zero_y,color='red',label='Points')



# apply genetic algorithm
def genetic_algorithm(sample_size,points,degree,generations,test,lower_bound=-10,upper_bound=10,mutation_rate=0.01,b=3,created_offspring = 200):
    # initialize the population
    sample = initialization(sample_size,degree,lower_bound,upper_bound)
    # calculate the fitness of the initial population
    fitness = fitness_fun(sample,points,test)
    # run the genetic algorithm
    for i in range(generations):
        # select parents
        sel = tournament_selection(sample,fitness,created_offspring,10)
        # perform crossover
        offsprings = []
        offsprings_fitness = []
        for _ in range(100):
            parents = np.random.randint(0,created_offspring,2)
            offspring = two_points_crossover(sel[parents[0]],sel[parents[1]])
            offspring_fitness = fitness_fun(offspring,points,0)
            offsprings.extend(offspring)
            offsprings_fitness.extend(offspring_fitness)
        # perform mutation
        offsprings = non_uniform_mutation(offsprings,i,generations,lower_bound,upper_bound,mutation_rate,b)
        # perform elitist replacement
        sample,fitness = elitist_replacement(sample,fitness,offsprings,offsprings_fitness)
    return sample,fitness
num_tests = len(degrees)
samples = []
for i in range(num_tests):
    degree = degrees[i]
    sample,_ = genetic_algorithm(sample_size=500,points=points,degree=degree,generations=100,test=i,lower_bound=-10,upper_bound=10,mutation_rate=0.01,b=3,created_offspring = 250)
    samples.append(sample)
    print(i)


def create_points(points_zero_x,chromosome):
    points_zero_y_pred = []
    for x in points_zero_x:
        y_pred = 0
        for i in range(len(chromosome)):
            y_pred += chromosome[i] * pow(x,i)
        points_zero_y_pred.append(y_pred)
    return points_zero_y_pred

y_pred = create_points(points_zero_x,samples[4][0])
# plot the points
#plt.plot(points_zero_x,points_zero_y,color='red',label='Points')
# plot the polynomial
plt.plot(points_zero_x,y_pred,color='blue',label='Polynomial')
plt.legend()
plt.show()
print("Hello")

