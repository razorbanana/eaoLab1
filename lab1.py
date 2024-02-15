import math
import random
import time
import numpy as np
import matplotlib.pyplot as plt

LETTERS = ['A','B','D','E','G','L','N','O','R','T']
FIRST = ['D','O','N','A','L','D']
SECOND = ['G','E','R','A','L','D']
THIRD = ['R','O','B','E','R','T']

class CustomError(Exception):
    def __init__(self, message):
        self.message = message

def find_answer():
    array = ['A','B','D','E','G','L','N','O','R','T']
    while True:
        first = 0
        second = 0
        third = 0
        for i in range(len(FIRST)):
            first += array.index(FIRST[-i-1])*10**i
        for i in range(len(SECOND)):
            second += array.index(SECOND[-i-1])*10**i
        for i in range(len(THIRD)):
            third += array.index(THIRD[-i-1])*10**i  
        evaluation = math.fabs(first + second - third)
        if evaluation == 0:
            print(array)
            break
        random.shuffle(array)

def evaluation1(array):
    first = 0
    second = 0
    third = 0
    for i in range(len(FIRST)):
        first += array.index(FIRST[-i-1])*10**i
    for i in range(len(SECOND)):
        second += array.index(SECOND[-i-1])*10**i
    for i in range(len(THIRD)):
        third += array.index(THIRD[-i-1])*10**i  
    evaluation = math.fabs(first + second - third)
    return evaluation

def evaluation2(array):
    first = 0
    second = 0
    third = 0
    for i in range(len(FIRST)):
        first += array.index(FIRST[-i-1])*10**i
    for i in range(len(SECOND)):
        second += array.index(SECOND[-i-1])*10**i
    for i in range(len(THIRD)):
        third += array.index(THIRD[-i-1])*10**i  
    evaluation = 0 if array.index('T') % 2 == 0 else 1
    evaluation = evaluation if array.index('E') == 0 or 9 else evaluation + 1
    evaluation = evaluation if array.index('A') == 4 or 5 else evaluation + 1
    evaluation = evaluation if (array.index('E') == 0 and array.index('A') == 5 and array.index('L') <= 4 and array.index('N')+array.index('R')<=8) or (array.index('E') == 9 and array.index('A') == 4 and array.index('L') >= 5 and array.index('N')+array.index('R')>=10) else evaluation + 1
    evaluation = evaluation if array.index('D') != 0 else evaluation + 1
    evaluation = evaluation if array.index('G') != 0 else evaluation + 1
    evaluation = evaluation if array.index('R') != 0 else evaluation + 1
    evaluation = 0 if first + second == third else evaluation + 1
    return evaluation

def test_evaluation2():
    array = ['D', 'L', 'E', 'O', 'A', 'B', 'G', 'T', 'R', 'N']
    print(array.index('T'))
    print(array.index('E'))
    print(array.index('D'))
    print(array.index('G'))
    print(array.index('R'))
    
    print(evaluation2(array))
    pop = PopulationEntity(1, array)
    print(pop.evaluation)

class PopulationEntity:
    def __init__(self, age, array):
        self._age = age
        self._array = array
        self._evaluation = evaluation2(array)

    @property
    def evaluation(self):
        return self._evaluation

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if isinstance(value, int) and value >= 0:
            self._age = value
        else:
            raise ValueError("Age must be a non-negative integer.")

    @property
    def array(self):
        return self._array

    @array.setter
    def array(self, value):
        if len(value) == 10:
            self._array = value
        else:
            raise ValueError("Array length must be less than or equal to 10.")

    def evaluate(self):
        self._evaluation = evaluation2(self.array)

    def print(self):
        print(self._age, self._array)

    def grow_older(self):
        self.age = self.age + 1
        
def init_entity():
    shuffled = LETTERS.copy()
    random.shuffle(shuffled)
    entity = PopulationEntity(1, shuffled)
    return entity

def init_population(quantity):
    result = []
    for i in range(quantity):
        result.append(init_entity())
    return result

def cross1(couple):
    person1, person2 = couple
    result1 = person2.copy()
    result2 = person1.copy()
    for i in range(len(LETTERS)):
        if i < len(LETTERS)/2:
            index = result1.index(person1[i])
            result1[index] = result1[i]
            result1[i] = person1[i]
    for i in range(len(LETTERS)):
        if i < len(LETTERS)/2:
            index = result2.index(person2[i])
            result2[index] = result2[i]
            result2[i] = person2[i]
    return (result1, result2)

def cross2(couple):
    person1, person2 = couple
    result1 = person2.copy()
    result2 = person1.copy()
    index = 0
    while True:
        if result1[index] == person1[index]:
            break
        result1[index] = person1[index]
        index = person2.index(person1[index])
    index = 0
    while True:
        if result2[index] == person2[index]:
            break
        result2[index] = person2[index]
        index = person1.index(person2[index])

    return (result1, result2)

def mutation1(population, mutation_rate):
    for person in population:
        if random.random() < mutation_rate:
            # print(person.array)
            index1 = random.randint(0, len(LETTERS)-1)
            while True:
                index2 = random.randint(0, len(LETTERS)-1)
                if index2 != index1:
                    break
            person.array[index1], person.array[index2] = person.array[index2], person.array[index1]
            person.evaluate()
            # print(person.array)
            # print("\n")
    return population

def mutation2(population, mutation_rate):
    for person in population:
        if random.random() < mutation_rate:
            # print(person.array)
            index1 = random.randint(0, len(LETTERS)-4)
            index2 = index1 + 3
            person.array[index1:index2 + 1] = person.array[index1:index2 + 1][::-1]
            person.evaluate()
            # print(person.array)
            # print("\n")
    return population

def test_cross1():
   a = ['R', 'L', 'T', 'N', 'G', 'E', 'A', 'B', 'O', 'D']
   b = ['G', 'L', 'D', 'A', 'B', 'T', 'O', 'N', 'R', 'E']
   print(a, b)
   print(cross1((a, b)))

def test_cross2():
   a = ['R', 'L', 'T', 'N', 'G', 'E', 'A', 'B', 'O', 'D']
   b = ['G', 'L', 'D', 'A', 'B', 'T', 'O', 'N', 'R', 'E']
   print(a, b)
   print(cross2((a, b)))

def test_evaluate():
    a = ['R', 'L', 'T', 'N', 'G', 'E', 'A', 'B', 'O', 'D']
    b = ['G', 'L', 'D', 'A', 'B', 'T', 'O', 'N', 'R', 'E']
    entity1 = PopulationEntity(1, a)
    entity2 = PopulationEntity(1, b)
    print(entity1.evaluation)
    print(entity2.evaluation)

def get_children(population, cross_type, couple_number):
    if couple_number > len(population)/2:
        raise CustomError("Number of couples should not be bigger than population number divided by two")
    if cross_type == 1:
        children = []
        for i in range(couple_number):
            children_arrays = cross1((population[2*i].array, population[2*i+1].array))
            children.append(PopulationEntity(0, children_arrays[0])) 
            children.append(PopulationEntity(0, children_arrays[1]))
        return children
    elif cross_type == 2:
        children = []
        for i in range(couple_number):
            children_arrays = cross1((population[2*i].array, population[2*i+1].array))
            children.append(PopulationEntity(0, children_arrays[0])) 
            children.append(PopulationEntity(0, children_arrays[1]))
        return children
    else:
        raise CustomError("Such type of crossing over is not developed")

def generation1(population, mutation_rate, cross_type, mutation_type, couple_number):
    sorted_population = sorted(population, key=lambda x: x.evaluation)
    children = get_children(sorted_population, cross_type, couple_number)
    sorted_population[-couple_number*2:] = children
    if mutation_type == 1:
        sorted_population = mutation1(sorted_population, mutation_rate)
    elif mutation_type == 2:
        sorted_population = mutation2(sorted_population, mutation_rate)
    else:
        raise CustomError("Such type of mutation is not developed")
    return sorted_population

def generation2(population, mutation_rate, cross_type, mutation_type, couple_number):
    sorted_population = sorted(population, key=lambda x: x.evaluation)
    children = get_children(sorted_population, cross_type, couple_number)
    sorted_population = sorted(population, key=lambda x: x.age)
    sorted_population[-couple_number*2:] = children
    if mutation_type == 1:
        sorted_population = mutation1(sorted_population, mutation_rate)
    elif mutation_type == 2:
        sorted_population = mutation2(sorted_population, mutation_rate)
    else:
        raise CustomError("Such type of mutation is not developed")
    return sorted_population

def show_plot(best_results, number, mutation_rate, cross_type, mutation_type, generation_type, couple_rate):
    iterations = range(1, len(best_results) + 1)
    plt.plot(iterations, best_results, marker='o', linestyle='-')
    plt.xlabel('Iteration')
    plt.ylabel('Best Result')
    title_text = f'Best Results over Iterations with {number} population\nMutation: {mutation_type}, Crossover: {cross_type}, Generation type: {generation_type}, Couples rate: {couple_rate}, Mutation Rate: {mutation_rate}'
    plt.title(title_text)
    plt.grid(True)
    plt.show()

def run(population, mutation_rate, cross_type, mutation_type, generation_type, couple_rate, max_iter):
    couple_number = math.floor(couple_rate * len(population) / 2)
    best_results = []
    iter = 0
    while True:
        best_result = min(population, key=lambda x: x.evaluation)
        best_results.append(best_result.evaluation)
        answer = best_result
        if answer.evaluation == 0:
            break
        if iter == max_iter:
            break
        for i in population:
            i.grow_older()
        iter += 1
        if generation_type == 1:
            population = generation1(population, mutation_rate, cross_type, mutation_type, couple_number)
        elif generation_type == 2:
            population = generation2(population, mutation_rate, cross_type, mutation_type, couple_number)
        else:
            raise CustomError("Such type of generation new generation is not developed")
            
    show_plot(best_results, len(population), mutation_rate, cross_type, mutation_type, generation_type, couple_rate)
    print(iter)
    return answer

def experiment(population, mutation_rate, cross_type, mutation_type, generation_type, couple_rate, max_iter):
    start_time = time.time()
    best_result = run(population, mutation_rate, cross_type, mutation_type, generation_type, couple_rate, max_iter)
    print(best_result.array)
    print(best_result.evaluation)
    end_time = time.time()
    print(end_time-start_time)

def main():
    mutation_types = [1,2]
    cross_types = [1,2]
    generation_types = [1,2]
    population_numbers = [20, 100, 200]
    mutation_rates = [0.1, 0.25, 0.5]
    cross_rates = [0.1, 0.25, 0.5, 1]
    population = init_population(100)
    copy = population.copy()
    experiment(copy, 0.5, 1, 1, 1, 0.25, 10000)
    # copy = population.copy()
    # for i in cross_types:
    #     experiment(copy, 0.1, i, 1, 1, 0.25, 10000)
    # copy = population.copy()
    # for i in generation_types:
    #     experiment(copy, 0.1, 1, 1, i, 0.25, 10000)
    # copy = population.copy()
    # for i in mutation_rates:
    #     experiment(copy, i, 1, 1, 1, 0.25, 10000)
    # copy = population.copy()
    # for i in cross_rates:
    #     experiment(copy, 0.1, 1, 1, 1, i, 10000)
    # for i in population_numbers:
    #     population = init_population(i)
    #     experiment(population, 0.1, 1, 1, 1, 0.25, 10000)

   
if __name__ == "__main__":
   main()