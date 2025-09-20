#Task-1
import random as rd
components= ['ALU', 'Cache', 'Control', 'Register', 'Decoder', 'Floating']
components_size= [(5, 5), (7, 4), (4, 4), (6, 6), (5, 3), (5, 5)]
chip_component_blocks= {}
for i in range (len(components)):
    chip_component_blocks[components[i]]= components_size[i]
#{'ALU': (5, 5), 'Cache': (7, 4), 'Control': (4, 4), 'Register': (6, 6), 'Decoder': (5, 3), 'Floating': (5, 5)}
wiring= [('Register', 'ALU'), ('Control', 'ALU'), ('ALU', 'Cache'), ('Register', 'Floating'), ('Cache', 'Decoder'), ('Decoder', 'Floating')]
chip_width= 25
chip_height= 25

def random_chromosome():
    chromosomes= []
    for key in components:
        blk_width, blk_height= chip_component_blocks[key]
        x= rd.randint(0, chip_width - blk_width)
        y= rd.randint(0, chip_height - blk_height)
        chromosomes.append((x, y))
    return chromosomes

init_population= []
for i in range(6):
    init_population.append(random_chromosome())

def center_dist(pos_1, pos_2, blk_1, blk_2): #distance between two center points
    x1= pos_1[0]+ blk_1[0] /2
    x2= pos_2[0]+ blk_2[0] /2
    y1= pos_1[1]+ blk_1[1] /2
    y2= pos_2[1]+ blk_2[1] /2
    return (((x1 - x2)**2 + (y1 - y2)**2)**0.5)

def chip_area(chromosome): #Chip area
    x_min, y_min= chromosome[0]
    width, height= chip_component_blocks[components[0]]
    x_max= x_min + width
    y_max= y_min + height

    for i in range(1, len(components)):
        width_x, height_y= chromosome[i]
        width, height= chip_component_blocks[components[i]]
        x_min= min(x_min, width_x)
        x_max= max(x_max, width_x + width)
        y_min= min(y_min, height_y)
        y_max= max(y_max, height_y + height)
    a= x_max - x_min
    b= y_max - y_min
    return (a*b)

def total_wiring(chromosome):
    total= 0
    dict= {}
    for i in range(6):
        dict[components[i]]= chromosome[i]
    for compo_1, compo_2 in wiring:
        total= total + center_dist(dict[compo_1], dict[compo_2], chip_component_blocks[compo_1], chip_component_blocks[compo_2])
    return total

def overlap(chromosome):
    count= 0
    for i in range(6):
        chromosome_x, chromosome_y= chromosome[i]
        component_width, component_height= chip_component_blocks[components[i]]
        for ii in range(i+1, 6):
            chromosomeii_x, chromosomeii_y = chromosome[ii]
            componentii_width, componentii_height = chip_component_blocks[components[ii]]
            if not (chromosome_x + component_width <= chromosomeii_x or chromosomeii_x + componentii_width <= chromosome_x or chromosome_y + component_height <= chromosomeii_y or chromosomeii_y + componentii_height <= chromosome_y):
                count= count+1
    return count

def fitness_calculation(chromosome):
    area= chip_area(chromosome)
    wire_length= total_wiring(chromosome)
    overlaps= overlap(chromosome)
    return (-(1000 * overlaps+ area+ wire_length))

def crossover(parent1, parent2):
    crossover_point= rd.randint(1, 5)
    child1= parent1[:crossover_point] +parent2[crossover_point:]
    child2= parent2[:crossover_point] +parent1[crossover_point:]
    return child1, child2

def mutation(chromo, bound= 0.1):
    if rd.random() < bound:
        i= rd.randint(0, 5)
        width, height= chip_component_blocks[components[i]]
        mutated_x= rd.randint(0, chip_width - width)
        mutated_y= rd.randint(0, chip_height - height)
        chromo[i]= (mutated_x, mutated_y)
    return chromo

#Genetic Algo
population_size= 6
iterations= 15
population= init_population

for Generations in range(iterations):
    assign_fitness= []
    for i_chromo in population:
        fitness_score= fitness_calculation(i_chromo)
        assign_fitness.append((fitness_score, i_chromo))

    assign_fitness.sort(reverse= True) #Sorting-  from the best fitness to the worst
    next_gen= [list(assign_fitness[0][1]), list(assign_fitness[1][1])] #Picking top 2 best generations

    Best_generations_chromosomes= []
    for chromo in assign_fitness:
        Best_generations_chromosomes.append(chromo[1])

    while len(next_gen) < population_size:
        parent1= rd.choice(Best_generations_chromosomes)
        parent2= rd.choice(Best_generations_chromosomes)

        child1, child2= crossover(parent1, parent2)
        next_gen.append(mutation(child1))
        if len(next_gen) < population_size:
            next_gen.append(mutation(child2))

    population= next_gen

Best_chromo= max(population, key= fitness_calculation)
Best_fitness= fitness_calculation(Best_chromo)
Total_wiring_length= total_wiring(Best_chromo)
Total_bounding_area= chip_area(Best_chromo)
Total_overlap_count= overlap(Best_chromo)
print("Best Fitness Value:", Best_fitness)
print("Total Wiring Length:", Total_wiring_length)
print("Total Bounding Area:", Total_bounding_area)
print("Total Overlaps:", Total_overlap_count)
print()
print("Position:")
for i in range(len(components)):
    print(f'{components[i]}: Bottom-Left at {Best_chromo[i]}')

#Task-2
print()
print()
First_Parent, Second_Parent= rd.sample(init_population, 2)
crossover_point1= rd.randint(0, len(components) -2)
crossover_point2= rd.randint(crossover_point1 +1, len(components) -1)
First_Child = First_Parent[:crossover_point1] + Second_Parent[crossover_point1:crossover_point2] + First_Parent[crossover_point2:]
Second_Child = Second_Parent[:crossover_point1] + First_Parent[crossover_point1:crossover_point2] + Second_Parent[crossover_point2:]

print("Parent 1:", First_Parent)
print("Parent 2:", Second_Parent)
print("Child 1:", First_Child)
print("Child 2:", Second_Child)